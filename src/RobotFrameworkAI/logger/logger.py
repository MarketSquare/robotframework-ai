import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from RobotFrameworkAI.logger.ascii.ascii import string_to_ascii

class UnicodeSafeFormatter(logging.Formatter):
    """
    A logging formatter that ensures safe handling of Unicode characters.

    This formatter extends the base logging.Formatter to ensure that log messages
    are correctly encoded as Unicode. It handles cases where the log message is
    provided as bytes and decodes them into a proper string using UTF-8 encoding.
    Additionally, it converts non-string log messages to strings.

    This formatter allows the logging of characters such as à, ê, etc.
    """
    def format(self, record):
        if isinstance(record.msg, bytes):
            record.msg = record.msg.decode('utf-8', 'replace')
        elif not isinstance(record.msg, str):
            record.msg = str(record.msg)
        
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        return s

class UnicodeSafeHandler(logging.StreamHandler):
    """
    A logging stream handler that ensures safe handling of Unicode characters.

    This handler extends the base logging.StreamHandler to ensure that log messages
    containing Unicode characters are correctly handled and written to the stream.
    It ensures that messages are properly formatted as strings and handles
    exceptions that occur during logging.

    This handler allows the logging of characters such as à, ê, etc.
    """
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            if isinstance(msg, str):
                msg = msg + '\n'
            stream.write(msg)
            self.flush()
        except Exception:
            self.handleError(record)

def create_handlers(log_folder = "logs"):
    """
    Creates the handlers for logging to the console and a file.

    Will log to the logs folder where it creates a log file with the date of creation as its name.
    It uses the UnicodeSafeFormatter and -Handler to handle all unicode characters correctly.
    """
    
    os.makedirs(log_folder, exist_ok=True)
    log_filename = os.path.join(log_folder, datetime.now().strftime("%Y-%m-%d.log"))

    # Creating the file handler with Unicode safe formatter
    formatter = UnicodeSafeFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, encoding='utf-8')
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setFormatter(formatter)

    # Creating the console handler with Unicode safe formatter
    console_handler = UnicodeSafeHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if os.path.getsize(log_filename) == 0:
        write_ascii_to_file(log_filename)
    return console_handler, file_handler

def setup_logging(enabled=True, for_tests=False, console_logging=False, file_logging=True):
    """
    Sets up the necessary evironment to allow logging.

    This will create a logs folder and a log file with the date of creation as its name.

    Has 4 argument flags.

    enabled: default True, if set to False this keyword does nothing (setting it to false after enabling logging doesn't turn it off yet).
    for_tests: default False, if set to True logs the logs to the logs_test folder instead of the logs folder.
    console_logging: default True, set to False to disable the logs being printed to the console.
    file_logging: default True, set to False to disable the logs being logged to a file.
    """
    if not enabled:
        return

    log_folder = "logs_test" if for_tests else "logs"
    console_handler, file_handler = create_handlers(log_folder)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if not any(isinstance(handler, UnicodeSafeHandler) for handler in root_logger.handlers):
        if console_logging:
            root_logger.addHandler(console_handler)
    if not any(isinstance(handler, TimedRotatingFileHandler) for handler in root_logger.handlers):
        if file_logging:
            root_logger.addHandler(file_handler)

    logging.getLogger(__name__).debug(f"Calling keyword: Setup Logging with arguments: (enabled: {enabled}), (for_tests: {for_tests}), (console_logging: {console_logging}), (file_logging: {file_logging})")

def write_ascii_to_file(file_path):
    """
    Create ascii art on top of the file showing the word --LOGS-- followed by the current date.
    """
    ascii_text = []
    ascii_text.extend(string_to_ascii("--LOGS--", 28))
    ascii_text.extend(string_to_ascii(datetime.now().strftime("%Y-%m-%d"), 14))
    with open(file_path, 'w') as f:
        f.write('\n' + '\n'.join(ascii_text) + '\n')
