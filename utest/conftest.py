import pytest
import logging
from src.RobotFrameworkAI.logger.logger import setup_logging

logger = logging.getLogger(__name__)

# Configure logging for the entire test session
@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    setup_logging(enabled=True)

# Log the name of each test before execution
@pytest.fixture(autouse=True)
def log_test_name(request):
    logger.info(f"Running test: {request.node.name}")

# Log before running tests in each test file
def pytest_runtest_setup(item):
    print(item)
    if item.parent is None:
        logger.info(f"Starting tests in file: {item.module.__name__}")

# Log after running all tests in each test file
def pytest_runtest_teardown(item, nextitem):
    print(item)
    if nextitem is None:
        logger.info(f"Finishing tests in file: {item.module.__name__}")

# Log before running tests
def pytest_configure(config):
    logger.info("Starting pytests")

# Log after finishing all tests
def pytest_unconfigure(config):
    logger.info("Finishing pytests")
