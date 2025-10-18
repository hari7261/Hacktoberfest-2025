"""Project-wide logger configuration.

Provides get_logger() to get a configured logger with a concise format.
"""
import logging
import sys


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger with stream handler and a simple formatter.

    Parameters
    ----------
    name: Optional logger name. Use module __name__ by default.
    """
    logger = logging.getLogger(name or __name__)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
