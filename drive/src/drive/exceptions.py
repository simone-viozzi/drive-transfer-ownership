


class DriveException(Exception):
    def __init__(self, message=None):
        super(DriveException, self).__init__(message)


class FolderNotFound(DriveException):
    def __init__(self, message):
        super(FolderNotFound, self).__init__(f'Folder "{message}" not found')


class FolderAlreadyExist(DriveException):
    def __init__(self, message):
        super(FolderAlreadyExist, self).__init__(f'Folder "{message}" already exist')


class FolderNotEmpty(DriveException):
    def __init__(self, message):
        super(FolderNotEmpty, self).__init__(f'Folder "{message}" is not empty')