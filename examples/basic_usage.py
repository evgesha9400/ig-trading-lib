import os
from ig_trading_lib.authentication import AuthenticationService
from ig_trading_lib.trading import get_open_positions


if __name__ == "__main__":
    api_key = os.environ.get("IG_API_KEY") or "your_api_key"
    account_identifier = os.environ.get("IG_ACCOUNT_IDENTIFIER") or "your_account_identifier"
    account_password = os.environ.get("IG_ACCOUNT_PASSWORD") or "your_account_password"
    base_url = os.environ.get("IG_BASE_URL") or "https://demo-api.ig.com"

    auth_service = AuthenticationService(
        api_key=api_key,
        account_identifier=account_identifier,
        account_password=account_password,
        base_url=base_url,
    )
    auth_response = auth_service.authenticate()

    open_positions = get_open_positions(tokens=auth_response.tokens, base_url=base_url)




