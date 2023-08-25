import logging
import structlog


def configure_logging(pretty=True):
    logging.basicConfig(
        level=logging.DEBUG,
    )
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )

    if pretty:
        processors = [
            structlog.stdlib.add_log_level,  # add log level
            structlog.dev.set_exc_info,  # add exception info
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    else:
        processors = []

    structlog.configure(
        processors=processors,
        cache_logger_on_first_use=True,
    )


# Configure logging on module import
configure_logging()


def get_logger(*args, **kwargs):
    return structlog.get_logger(*args, **kwargs)
