import logging
import os
import pytest

@pytest.fixture
def config_path() -> str:
    return os.path.join(os.path.dirname(__file__), "data/test_config.yaml")

@pytest.fixture()
def logger() -> logging.Logger:
    logger = logging.getLogger("plugin-logger")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
