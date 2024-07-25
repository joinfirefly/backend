

import pytest
from unittest.mock import patch
from main import get, generate_schema
import logging

@pytest.fixture
def logger():
    return get()

@pytest.mark.parametrize("level", [logging.DEBUG, logging.WARNING])
def test_get_with_different_log_level(level, logger):
    logger_modified = get(level)
    assert logger_modified.level == level

def test_get_with_existing_handlers(logger):
    logger_old = logger
    logger_new = get()
    assert logger_old == logger_new

@patch('main.get_openapi')
@patch('main.logger')
@patch('main.app')
def test_generate_schema(mock_app, mock_logger, mock_get_openapi):
    mock_get_openapi.return_value = 'openapi'
    mock_app.title = 'title'
    mock_app.version = 'version'
    mock_app.openapi_version = 'openapi_version'
    mock_app.description = 'description'
    mock_app.routes = 'routes'
    
    result = generate_schema()

    mock_logger.info.assert_any_call("v0.1.0, Created By AmaseCocoa")
    mock_logger.info.assert_any_call("Generating OpenAPI JSON...")
    mock_get_openapi.assert_called_once_with(title='title', version='version', openapi_version='openapi_version', description='description', routes='routes')
    mock_logger.info.assert_called_with("OpenAPI JSON data was successfully generated.")
    
    assert result == 'openapi'


