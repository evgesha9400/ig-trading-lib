import logging
import os

import pytest
from dotenv import load_dotenv

from ig_trading_lib.authentication.service import AuthenticationService
from ig_trading_lib.trading import IGClient, OrderService, PositionService

dotenv_path = os.path.join(os.path.dirname(__file__), ".env.test")

logging.basicConfig(level=logging.INFO)


@pytest.fixture
def auth_service() -> AuthenticationService:
    load_dotenv(dotenv_path)
    api_key = os.getenv("IG_API_KEY")
    account_identifier = os.getenv("IG_ACCOUNT_IDENTIFIER")
    account_password = os.getenv("IG_ACCOUNT_PASSWORD")
    base_url = os.getenv("IG_BASE_URL")

    service = AuthenticationService(
        api_key=api_key,
        account_identifier=account_identifier,
        account_password=account_password,
        base_url=base_url,
    )
    return service


@pytest.fixture
def ig_client(auth_service) -> IGClient:
    auth_response = auth_service.authenticate()
    return IGClient(
        base_url=auth_service.base_url,
        api_key=auth_service.api_key,
        tokens=auth_response.tokens,
    )


@pytest.fixture
def position_service(ig_client) -> PositionService:
    return PositionService(ig_client)


@pytest.fixture
def order_service(ig_client) -> OrderService:
    return OrderService(ig_client)
