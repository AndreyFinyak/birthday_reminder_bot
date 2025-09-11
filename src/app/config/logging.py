import logging

LOG_LEVEL_DICT = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def configure_logging(level: str) -> None:
    """Конфигурация логирования для всего приложения."""
    logging.basicConfig(
        level=LOG_LEVEL_DICT[level.upper()],
        format=(
            "[%(asctime)s.%(msecs)03d] %(module)-20s:%(lineno)3d "
            "%(levelname)-7s - %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )
