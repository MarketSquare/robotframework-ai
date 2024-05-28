from RobotFrameworkAI.logger.logger_config import setup_logging
import logging


setup_logging(enabled=True, for_tests=True, console_logging=False)
logger = logging.getLogger(__name__)


class LoggerListener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.ROBOT_LISTENER_API_VERSION = 2

    def start_test(self, name, attributes):
        logger.info(f"Running test: {name}")

    def start_keyword(self, name, attributes):
        if name == 'BuiltIn.Run Keyword And Expect Error':
            expected_error = attributes['args'][0]
            logger.info(f"Expecting error: {expected_error}")

    def start_suite(self, name, attributes):
        logger.info(f"Starting suite: {name}")

    def end_suite(self, name, attributes):
        logger.info(f"Ending suite: {name}")
