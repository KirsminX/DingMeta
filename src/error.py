class DownloadError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InputError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)