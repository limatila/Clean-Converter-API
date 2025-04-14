#Custom exceptions (mainly just nomenclatures) for this project
#The point of creating them is that they should be Raised troughout the project

class FileUsageManagementError(Exception):
    def __init__(self, message):
        super().__init__(message)

class CookieNotFound(Exception): 
    def __init__(self, message: str):
        super().__init__(message)