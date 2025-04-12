
# loggers to be used in one of these situations: cookie validation, performance issues, (...)

import logging
from logging import StreamHandler, FileHandler, Formatter

from src.config import (
    BASE_LOGS_PATH,
    defaultFormatter, 
)

perfPath: str = BASE_LOGS_PATH + 'performance.log'
cookiesPath: str = BASE_LOGS_PATH + 'cookies.log'

performanceLogger = logging.getLogger('perflog')
cookiesLogger = logging.getLogger('cookielog')

def initLoggers():
    #Base config
    logging.basicConfig(encoding='UTF-8', level=logging.DEBUG, format=defaultFormatter)

    for logger in [performanceLogger, cookiesLogger]:
        logger.handlers.clear()

    #configuring Performance logger: file + stream
    performance_FileHandler = FileHandler(perfPath)
    performance_FileHandler.setLevel(logging.INFO)
    performance_FileHandler.setFormatter(Formatter(defaultFormatter))
    performance_StreamHandler = StreamHandler()
    performance_StreamHandler.setLevel(logging.WARNING)
    performance_StreamHandler.setFormatter(Formatter(defaultFormatter))

    performanceLogger.addHandler(performance_FileHandler)
    performanceLogger.addHandler(performance_StreamHandler)
    
    #configuring Cookies logger: file only
    cookies_FileHandler = FileHandler(cookiesPath)
    cookies_FileHandler.setLevel(logging.DEBUG)
    cookies_FileHandler.setFormatter(Formatter(defaultFormatter))

    cookiesLogger.addHandler(cookies_FileHandler)


#init it when imported
try:
    initLoggers();
except FileNotFoundError:
    from pathlib import Path
    #create non-existant dirs and files
    Path(perfPath).parent.mkdir(exist_ok=True, parents=True)
    Path(cookiesPath).parent.mkdir(exist_ok=True, parents=True)

    Path(perfPath).write_text("")
    Path(cookiesPath).write_text("")

    #try again
    initLoggers();


if __name__ == "__main__":
    performanceLogger.warning("TESTING performance monitoring logs")
    cookiesLogger.info("TESTING cookie management logs")

    #* cookie limited level: DEBUG
    cookiesLogger.debug("TESTING cookie debug")
    #* performance limited level: file/INFO, stream/WARNING
    performanceLogger.debug("TESTING performance debug") #will not be logged
    performanceLogger.info("TESTING performance info")
