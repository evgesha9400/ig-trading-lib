from ig_trading_lib.authentication import AuthenticationService


if __name__ == "__main__":
    auth_service = AuthenticationService(
        api_key="example_api_key",
        account_identifier="example_account",
        account_password="example_password",
        base_url="https://demo-api.ig.com",
    )
    auth_response = auth_service.authenticate()
    print(auth_response.tokens)
