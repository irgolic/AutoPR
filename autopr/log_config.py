def configure_logging(pretty=True):
    import logging
    import structlog

    logging.basicConfig(
        level=logging.INFO
    )

    if pretty:
        processors = [
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    else:
        processors = []

    structlog.configure(
        processors=processors,
        cache_logger_on_first_use=True,
    )
