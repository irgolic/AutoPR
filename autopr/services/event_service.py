class EventHandler:
    def register_handler_decorator(self,
        # a sprinkle of magic
        self.handle_method_name_for_event_type = {}
        for method in dir(self):
            if method.startswith('_handle_'):
                event_type = method.removeprefix('_handle_')
                self.handle_method_name_for_event_type[event_type] = method

    def handle_json_event(self, event_json: str):
        event = EventUnion.parse_raw(event_json)
        self.handle_event(event)

    def handle_event(self, event: EventUnion):
        logger.info(f'Handle event: {event}')

        # if event is not defined
        if event.event_type not in self.handle_method_name_for_event_type:
            # check if event type exists in EventUnion, for the sake of a more informative error
            # TODO compare strings, but this isn't exactly how you get the literal of the pydantic cls
            #   if event.event_type not in [e.event_type for e in typing.get_args(EventUnion)]:
            raise ValueError(f'Event type {event.event_type} does not exist')

        method_name = self.handle_method_name_for_event_type[event.event_type]

        # check if method was overriden
        impl_method = getattr(type(self), method_name)
        base_method = getattr(EventHandler, method_name)
        if impl_method == base_method:
            return

        return impl_method(self, event)

    @register_handler_decorator('node_added'
    def _handle_node_added_event(self, event: NodeAddedEvent):
        ...

