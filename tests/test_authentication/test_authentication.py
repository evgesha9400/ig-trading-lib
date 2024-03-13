from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import requests
from cryptography.fernet import Fernet

from ig_trading_lib.authentication import AuthenticationService
from ig_trading_lib.authentication.cache import InMemoryCache, DurableCache
from ig_trading_lib.authentication.models import AccountInfo, AuthenticationResponse


def test_authentication_no_cache(mocker, test_account_info):
    mock_post = mocker.patch(
        "ig_trading_lib.authentication.authentication.requests.post"
    )
    test_service = AuthenticationService(
        api_key="test_api_key",
        account_identifier="test_account",
        account_password="test_password",
        base_url="https://api.example.com",
        cache=None,
    )

    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.headers = {
        "CST": "valid_cst_token",
        "X-SECURITY-TOKEN": "valid_x_security_token",
    }
    response.json.return_value = test_account_info
    mock_post.return_value = response

    auth_response = test_service.authenticate()
    assert auth_response.cst_token == "valid_cst_token"
    assert auth_response.x_security_token == "valid_x_security_token"
    assert auth_response.account_info.model_dump() == test_account_info


def test_authentication_in_memory_cache_hit(mocker, test_account_info):
    mock_post = mocker.patch(
        "ig_trading_lib.authentication.authentication.requests.post"
    )
    test_cache = InMemoryCache()
    test_service = AuthenticationService(
        api_key="test_api_key",
        account_identifier="test_account",
        account_password="test_password",
        base_url="https://api.example.com",
        cache=test_cache,
    )

    test_response = MagicMock(spec=AuthenticationResponse)
    test_response.cst_token = "valid_cst_token"
    test_response.x_security_token = "valid_x_security_token"
    test_response.expiry = int(datetime.now().timestamp() + 6 * 3600)
    test_response.account_info = AccountInfo.model_validate(test_account_info)
    test_cache.response = test_response

    auth_response = test_service.authenticate()

    assert auth_response.cst_token == "valid_cst_token"
    assert auth_response.x_security_token == "valid_x_security_token"
    assert auth_response.account_info.model_dump() == test_account_info
    mock_post.assert_not_called()


def test_authentication_in_memory_cache_miss(mocker, test_account_info):
    mock_post = mocker.patch(
        "ig_trading_lib.authentication.authentication.requests.post"
    )
    test_cache = InMemoryCache()
    test_service = AuthenticationService(
        api_key="test_api_key",
        account_identifier="test_account",
        account_password="test_password",
        base_url="https://api.example.com",
        cache=test_cache,
    )

    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.headers = {
        "CST": "valid_cst_token",
        "X-SECURITY-TOKEN": "valid_x_security_token",
    }
    response.json.return_value = test_account_info
    mock_post.return_value = response

    auth_response = test_service.authenticate()

    assert auth_response.cst_token == "valid_cst_token"
    assert auth_response.x_security_token == "valid_x_security_token"
    assert auth_response.account_info.model_dump() == test_account_info
    mock_post.assert_called_once()
    assert test_cache.response == auth_response


@pytest.mark.parametrize(
    "encryption_key",
    [None, Fernet.generate_key()],
)
def test_authentication_durable_cache_hit(mocker, encryption_key, test_account_info):
    mock_post = mocker.patch(
        "ig_trading_lib.authentication.authentication.requests.post"
    )
    # Create a durable cache and save a valid authentication response to it
    current = Path(__file__).parent.absolute()
    path = f"{current}/test_cache.json"
    test_cache = DurableCache(path=path, encryption_key=encryption_key)
    test_response = AuthenticationResponse(
        cst_token="valid_cst_token",
        x_security_token="valid_x_security_token",
        expiry=int(datetime.now().timestamp() + 6 * 3600),
        account_info=AccountInfo.model_validate(test_account_info),
    )
    test_cache.save_authentication_response(test_response)

    # Create an authentication service with the durable cache
    test_service = AuthenticationService(
        api_key="test_api_key",
        account_identifier="test_account",
        account_password="test_password",
        base_url="https://api.example.com",
        cache=test_cache,
    )

    # Call the authenticate method
    auth_response = test_service.authenticate()

    # Check that the returned authentication response is the same as the one saved in the cache
    assert auth_response.cst_token == "valid_cst_token"
    assert auth_response.x_security_token == "valid_x_security_token"
    assert auth_response.account_info.model_dump() == test_account_info

    # Check that the POST request was not made
    mock_post.assert_not_called()

    # Check that the cache was not updated
    assert test_cache.load_authentication_response() == test_response

    # Delete the durable cache file
    Path(path).unlink()


@pytest.mark.parametrize(
    "encryption_key",
    [None, Fernet.generate_key()],
)
def test_authentication_durable_cache_miss(mocker, encryption_key, test_account_info):
    mock_post = mocker.patch(
        "ig_trading_lib.authentication.authentication.requests.post"
    )
    # Create a durable cache
    current = Path(__file__).parent.absolute()
    path = f"{current}/test_cache.json"
    test_cache = DurableCache(path=path, encryption_key=encryption_key)

    # Create an authentication service with the durable cache
    test_service = AuthenticationService(
        api_key="test_api_key",
        account_identifier="test_account",
        account_password="test_password",
        base_url="https://api.example.com",
        cache=test_cache,
    )

    # Mock the POST request response
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.headers = {
        "CST": "valid_cst_token",
        "X-SECURITY-TOKEN": "valid_x_security_token",
    }
    response.json.return_value = test_account_info
    mock_post.return_value = response

    # Call the authenticate method
    auth_response = test_service.authenticate()

    # Check that the returned authentication response is the same as the one returned by the POST request
    assert auth_response.cst_token == "valid_cst_token"
    assert auth_response.x_security_token == "valid_x_security_token"
    assert auth_response.account_info.model_dump() == test_account_info

    # Check that the POST request was made
    mock_post.assert_called_once()

    # Check that the cache was created and contains the returned authentication response
    assert test_cache.load_authentication_response() == auth_response

    # Delete the durable cache file
    Path(path).unlink()
