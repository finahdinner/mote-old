import logging

# MyLogger class, which can be instantiated for each file that needs logging abilities.
class MyLogger:
    """ Usage: MyLogger.logger.[LEVEL]('[LOG MESSAGE]') """

    def __init__(self, file_name, log_file_path):
        self.file_name = file_name
        self.log_file_path = log_file_path # log file path

        # logger
        self.logger = logging.getLogger(self.file_name)
        self.logger.setLevel(logging.DEBUG) # unless a handler is specified otherwise, will log DEBUG and above

        # logger handler for the log file
        self.file_handler = logging.FileHandler(self.log_file_path)
        self.file_handler.setLevel(logging.ERROR) # only log to file for ERRORS and above
        self.file_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s') # format of log lines
        self.file_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(self.file_handler)

        # logger handler for the to console - will log all things (debug and above)
        self.stream_handler = logging.StreamHandler()
        self.stream_formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        self.stream_handler.setFormatter(self.stream_formatter)
        self.logger.addHandler( self.stream_handler)