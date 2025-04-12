
# loggers to be used in one of these situations: cookie validation, performance issues, (...)

import logging
from logging import StreamHandler, FileHandler, Formatter

from src.config import (
    BASE_LOGS_PATH,
    defaultFormatter, 
)
perfPath: str = BASE_LOGS_PATH + 'performance.log'
cookiesPath: str = BASE_LOGS_PATH + 'cookies.log'
fileUsagePath: str = BASE_LOGS_PATH + 'fileUsage.log'

performanceLogger = logging.getLogger('perf_log')    # performance tracking, SlowApi
cookiesLogger = logging.getLogger('cookie_log')      # cookieValidation
fileUsageLogger = logging.getLogger('fileusage_log') # file usage management, download / compression

def _initLoggers(): #? could make this a more simple dynamic function
    #Base config
    logging.basicConfig(encoding='UTF-8', level=logging.DEBUG, format=defaultFormatter)

    for logger in [performanceLogger, cookiesLogger, fileUsageLogger]:
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

    #configuring File Usage logger: file + stream
    fileUsage_FileHandler = FileHandler(perfPath)
    fileUsage_FileHandler.setLevel(logging.INFO)
    fileUsage_FileHandler.setFormatter(Formatter(defaultFormatter))
    fileUsage_StreamHandler = StreamHandler()
    fileUsage_StreamHandler.setLevel(logging.DEBUG)
    fileUsage_StreamHandler.setFormatter(Formatter(defaultFormatter))

    fileUsageLogger.addHandler(fileUsage_FileHandler)
    fileUsageLogger.addHandler(fileUsage_StreamHandler)


#init it when imported
try:
    _initLoggers();
except FileNotFoundError:
    from pathlib import Path
    #create non-existant dirs and files
    Path(perfPath).parent.mkdir(exist_ok=True, parents=True)
    Path(cookiesPath).parent.mkdir(exist_ok=True, parents=True)
    Path(fileUsagePath).parent.mkdir(exist_ok=True, parents=True)

    Path(perfPath).write_text("")
    Path(cookiesPath).write_text("")
    Path(fileUsagePath).write_text("")

    #try again
    _initLoggers();


if __name__ == "__main__":
    performanceLogger.warning("TESTING performance monitoring logs")
    cookiesLogger.info("TESTING cookie management logs")
    fileUsageLogger.info("TESTING file usage management logs")

    #* cookie limited level: DEBUG
    cookiesLogger.debug("TESTING cookie debug")
    #* performance limited level: file/INFO, stream/WARNING
    performanceLogger.debug("TESTING performance debug") #will not be logged
    performanceLogger.info("TESTING performance info")
    #* file usage limited level: file/INFO, stream/DEBUG
    performanceLogger.debug("TESTING file usage debug") #only to stream
    performanceLogger.info("TESTING file usage info")   #to file and stream