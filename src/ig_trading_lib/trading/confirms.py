from ig_trading_lib.trading.client import TradingClient
from ig_trading_lib.trading.models import DealConfirmation, DealReference


def get_deal_confirmation(client: TradingClient, deal_reference: DealReference) -> DealConfirmation:
    resp = client.get(
        f"/gateway/deal/confirms/{deal_reference.dealReference}",
        headers={"Version": "1"},
    )
    if resp.status_code == 200:
        return DealConfirmation.model_validate(resp.json())
    raise RuntimeError(f"Deal confirmation request failed with status code {resp.status_code}: {resp.text}")
