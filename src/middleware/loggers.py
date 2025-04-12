
#! a default logger, and a simple one for usage, with console and file logs, usage is defined in /config

import logging
from logging import StreamHandler, FileHandler
from datetime import datetime

from src.config import (
    BASE_LOGS_PATH,
    defaultFormatter, 
)

performanceLogger = logging.getLogger()
cookiesLogger = logging.getLogger()

perfPath: str = BASE_LOGS_PATH + 'performance.log'
cookiesPath: str = BASE_LOGS_PATH + 'cookies.log'

def initLoggers():
    #Base config
    logging.basicConfig(encoding='UTF-8', level=logging.DEBUG)

    #configuring Performance logger: file + stream
    performance_FileHandler = FileHandler(perfPath)
    performance_FileHandler.setLevel(logging.WARNING)
    performanceLogger.addHandler(performance_FileHandler)
    performanceLogger.addHandler(StreamHandler())
    
    #configuring Cookies logger: file only
    cookies_FileHandler = FileHandler(cookiesPath)
    cookies_FileHandler.setLevel(logging.INFO)
    cookiesLogger.addHandler(cookies_FileHandler)

try:
    initLoggers();
except FileNotFoundError:
    from pathlib import Path

    #create non-existant dirs and files
    Path(cookiesPath).parent.mkdir(exist_ok=True, parents=True)
    Path(perfPath).parent.mkdir(exist_ok=True, parents=True)

    Path(cookiesPath).write_text("")
    Path(perfPath).write_text("")

    initLoggers();

if __name__ == "__main__":
    cookiesLogger.INFO("testing cookie management logs")
    performanceLogger.WARNING("testing performance monitoring logs")
