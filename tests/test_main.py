import logging
from unittest.mock import patch

import pytest

from app.server import generate_schema
from app.utils.log import getLogger
from app import __version__

@pytest.fixture
def logger():
    return getLogger()

@pytest.mark.parametrize("level", [logging.DEBUG, logging.WARNING])
def test_get_with_different_log_level(level, logger):
    logger_modified = getLogger(level=level)
    assert logger_modified.level == level

def test_get_with_existing_handlers(logger):
    logger_old = logger
    logger_new = getLogger()
    assert logger_old == logger_new

@patch('app.server.get_openapi')
@patch('app.server.logger')
@patch('app.server.app')
def test_generate_schema(mock_app, mock_logger, mock_get_openapi):
    mock_get_openapi.return_value = 'openapi'
    mock_app.title = 'title'
    mock_app.version = 'version'
    mock_app.openapi_version = 'openapi_version'
    mock_app.description = 'description'
    mock_app.routes = 'routes'
    
    result = generate_schema()

    mock_logger.info.assert_any_call(f"v{__version__}, Created By Holo Team")
    mock_logger.info.assert_any_call("Generating OpenAPI JSON...")
    mock_get_openapi.assert_called_once_with(title='title', version='version', openapi_version='openapi_version', description='description', routes='routes')
    mock_logger.info.assert_called_with("OpenAPI JSON data was successfully generated.")
    
    assert result == 'openapi'