from autopr.actions.base import ActionBase
from autopr.services.publish_service import PublishService


class ActionService:
    def __init__(
        self,
        publish_service: PublishService,
    ):
        self.publish_service = publish_service

    def generate_rail_spec(
        self,
        actions: list[ActionBase],
    ):
        output_spec = f"""<choice
            name="action"
            on-fail-choice="reask"
        >"""
        for action in actions:
            output_spec += f"""<case
                name="{action.id}"
            >
            <object
                name="{action.id}"
            >
            {action.output_spec}
            </object>
            </case>"""
        output_spec += f"""<case
            name="finished"
        >
        </case>
        </choice>"""
