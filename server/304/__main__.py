"""
main
"""

import argparse
import logging
import logging.config
import time

from argparse import ArgumentParser
from logging.handlers import TimedRotatingFileHandler

from .app import App


def _add_arguments(parser: ArgumentParser):
    parser.description = "304-The-Game"
    parser.add_argument("--host", default="127.0.0.1", help="Bind to this address")
    parser.add_argument("--port", type=int, default=3040, help="Bind to this port")
    parser.add_argument("--version", default="SNAPSHOT", help="Version of the project")
    parser.add_argument("--log-level", default="info", help="Log Level")
    parser.add_argument("--log-file", default="game.log")


LOG_FORMAT = f"%(asctime)s {time.localtime().tm_zone} - %(levelname)s - %(name)s - %(message)s"



def _configure_logger(log_level: str, log_file: str):
    formatter = logging.Formatter(LOG_FORMAT)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(formatter)

    # file_handler = logging.FileHandler(filename=log_file, encoding="utf-8")
    file_handler = TimedRotatingFileHandler(
        filename=log_file, encoding="utf-8", when="d", backupCount=10, interval=1
    )

    processing_logger = logging.getLogger("processing")

    if log_level.upper() == "TRACE":
        level = logging.NOTSET
    elif log_level.upper() == "WARN":
        level = logging.WARNING
    elif log_level.upper() == "DEBUG":
        level = logging.DEBUG
    else:
        level = logging.INFO

    processing_logger.addHandler(log_handler)
    processing_logger.addHandler(file_handler)
    processing_logger.setLevel(level)


def main():
    """
    main
    """
    parser = argparse.ArgumentParser()
    _add_arguments(parser=parser)
    args = parser.parse_args()
    _configure_logger(args.log_level, args.log_file)

    # runs indefinitively untill stopped.
    App(args.host, args.port, args.version, args.log_level)


if __name__ == "__main__":
    main()
