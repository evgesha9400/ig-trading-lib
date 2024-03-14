from pytest import fixture

from ig_trading_lib import Tokens


@fixture
def api_key() -> str:
    return "test_api_key"


@fixture
def tokens() -> Tokens:
    return Tokens(cst_token="test_cst_token", x_security_token="test_x_security_token")