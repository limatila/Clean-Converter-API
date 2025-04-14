
# loggers to be used in one of these situations: cookie validation, performance issues, (...)

import logging
from logging import StreamHandler, FileHandler, Formatter

from src.config import (
    BASE_LOGS_PATH,
    defaultFormatter, 
)
performancePath: str = BASE_LOGS_PATH + 'performance.log'
cookiesPath: str = BASE_LOGS_PATH + 'cookies.log'
fileUsagePath: str = BASE_LOGS_PATH + 'fileUsage.log'
requestsPath: str = BASE_LOGS_PATH + 'requests.log'

performanceLogger = logging.getLogger('perf_log')    # performance tracking, SlowApi
cookiesLogger = logging.getLogger('cookie_log')      # cookieValidation
fileUsageLogger = logging.getLogger('fileusage_log') # file usage management, download / compression
requestsLogger = logging.getLogger('requests_logger')  # requests related information

def _initLoggers(): #? could make this a more simple dynamic function
    #Base config
    logging.basicConfig(encoding='UTF-8', level=logging.DEBUG, format=defaultFormatter)

    for logger in [performanceLogger, cookiesLogger, fileUsageLogger, requestsLogger]:
        logger.handlers.clear()
        logger.propagate = False

    #configuring Performance logger: file + stream
    performance_FileHandler = FileHandler(performancePath)
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
    fileUsage_FileHandler = FileHandler(fileUsagePath)
    fileUsage_FileHandler.setLevel(logging.INFO)
    fileUsage_FileHandler.setFormatter(Formatter(defaultFormatter))
    fileUsage_StreamHandler = StreamHandler()
    fileUsage_StreamHandler.setLevel(logging.DEBUG)
    fileUsage_StreamHandler.setFormatter(Formatter(defaultFormatter))

    #Configuring Requests logger: file + stream
    requestsFileHandler = FileHandler(requestsPath)
    requestsFileHandler.setLevel(logging.INFO)
    requestsFileHandler.setFormatter(Formatter(defaultFormatter))
    requestsStreamHandler = StreamHandler()
    requestsStreamHandler.setLevel(logging.DEBUG)
    requestsStreamHandler.setFormatter(Formatter(defaultFormatter))

    requestsLogger.addHandler(requestsFileHandler)
    requestsLogger.addHandler(requestsStreamHandler)


#init it when imported
try:
    _initLoggers();
except FileNotFoundError:
    from pathlib import Path
    #create non-existant dirs and files
    Path(performancePath).parent.mkdir(exist_ok=True, parents=True)
    Path(cookiesPath).parent.mkdir(exist_ok=True, parents=True)
    Path(fileUsagePath).parent.mkdir(exist_ok=True, parents=True)
    Path(requestsPath).parent.mkdir(exist_ok=True, parents=True)

    Path(performancePath).write_text("")
    Path(cookiesPath).write_text("")
    Path(fileUsagePath).write_text("")
    Path(requestsPath).write_text("")

    #try again
    _initLoggers();


if __name__ == "__main__":
    performanceLogger.warning("TESTING performance monitoring logs")
    cookiesLogger.info("TESTING cookie management logs")
    fileUsageLogger.info("TESTING file usage management logs")
    requestsLogger.info("TESTING request logs")

    #* cookie limited level: DEBUG
    cookiesLogger.debug("TESTING cookie debug")
    #* performance limited level: file/INFO, stream/WARNING
    performanceLogger.debug("TESTING performance debug") #will not be logged
    performanceLogger.info("TESTING performance info")
    #* file usage limited level: file/INFO, stream/DEBUG
    fileUsageLogger.debug("TESTING file usage debug") #only to stream
    fileUsageLogger.info("TESTING file usage info")   #to file and stream
    #* requests limited level: file/INFO, stream/DEBUG
    requestsLogger.debug("TESTING requests debug") #only to stream
    requestsLogger.info("TESTING requests info")   #to file and stream

    for logger in [performanceLogger, cookiesLogger, fileUsageLogger, requestsLogger]:
        print(logger.handlers)