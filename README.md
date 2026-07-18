# IG Trading Library

A comprehensive Python library for interfacing with the IG Trading platform. This library provides a straightforward and Pythonic way to interact with the IG Trading API, enabling automation of trading tasks, account management, position management, and order handling.

## Prerequisites

- Python 3.13+
- make (for running tests)

## Installation

```bash
pip install ig-trading-lib
```

## Quick Start

```python
from ig_trading_lib.authentication import AuthenticationService
from ig_trading_lib.authentication.cache import InMemoryCache
from ig_trading_lib.trading import CreatePosition, PositionService, IGClient

# Initialize authentication
auth_service = AuthenticationService(
    api_key="your_api_key",
    account_identifier="your_account_identifier", 
    account_password="your_account_password",
    base_url="https://demo-api.ig.com",
    cache=InMemoryCache()
)

# Authenticate
auth_response = auth_service.authenticate()

# Create client and position service
client = IGClient(base_url="https://demo-api.ig.com", api_key="your_api_key", tokens=auth_response.tokens)
position_service = PositionService(client)

# Create a position
position = CreatePosition(
    currencyCode="USD",
    direction="BUY",
    epic="CS.D.GBPUSD.TODAY.IP",
    orderType="MARKET",
    size=1
)

deal_reference = position_service.create_position(position)
```

## Features

### Authentication Module
- **AuthenticationService**: Handles authentication with the IG REST API
- **Token Management**: Automatic token caching and refresh
- **Multiple Cache Options**: In-memory and encrypted file-based caching
- **Account Information**: Retrieves account details and financial information

### Trading Module

#### Positions Service
- **Create Positions**: Open new trading positions with various order types (MARKET, LIMIT, QUOTE)
- **Get Positions**: Retrieve all open positions or specific positions by deal ID
- **Update Positions**: Modify existing positions (stop levels, limit levels, trailing stops)
- **Close Positions**: Close existing positions with flexible order options
- **Risk Management**: Support for guaranteed stops, trailing stops, and stop/limit orders

#### Orders Service  
- **Working Orders**: Create, retrieve, and delete working orders
- **Order Types**: Support for LIMIT and STOP orders
- **Time in Force**: GOOD_TILL_CANCELLED and GOOD_TILL_DATE options
- **Order Management**: Full CRUD operations for working orders

### Data Models
- **Type Safety**: Full Pydantic model validation
- **Rich Validation**: Comprehensive field validation and constraints
- **Serialization**: Automatic JSON serialization/deserialization
- **Error Handling**: Detailed error messages and validation feedback

## Modules

### Authentication (`ig_trading_lib.authentication`)
- `AuthenticationService`: Main authentication service
- `AuthenticationCacheABC`: Abstract cache interface
- `DurableCache`: File-based caching with optional encryption
- `InMemoryCache`: In-memory token caching

### Trading (`ig_trading_lib.trading`)
- `PositionService`: Position management operations
- `OrderService`: Working order management operations

### Models (via `ig_trading_lib.trading` facade)
- `CreatePosition`: Position creation model
- `ClosePosition`: Position closing model  
- `UpdatePosition`: Position update model
- `OpenPosition`: Open position data model
- `Market`: Market information model

### Orders Models (via `ig_trading_lib.trading` facade)
- `CreateWorkingOrder`: Working order creation model
- `WorkingOrder`: Working order data model
- `MarketData`: Market data for orders

## Running Tests

The project includes comprehensive unit and integration tests:

```bash
# Run all tests
make test

# Run unit tests only
pytest tests/unit

# Run integration tests (requires API credentials)
pytest tests/integration
```

## API Reference

### Authentication Service

```python
from ig_trading_lib.authentication import AuthenticationService
from ig_trading_lib.authentication.cache import DurableCache, InMemoryCache

# Basic usage
auth_service = AuthenticationService(
    api_key="your_api_key",
    account_identifier="your_account_identifier",
    account_password="your_account_password", 
    base_url="https://demo-api.ig.com"  # or https://api.ig.com for live
)

# With caching
auth_service = AuthenticationService(
    api_key="your_api_key",
    account_identifier="your_account_identifier",
    account_password="your_account_password",
    base_url="https://demo-api.ig.com",
    cache=DurableCache("tokens.json", encryption_key=b"your_key")  # Optional
)

auth_response = auth_service.authenticate()
```

### Position Service

```python
from ig_trading_lib.trading import PositionService, CreatePosition, IGClient

client = IGClient(base_url="https://demo-api.ig.com", api_key="your_api_key", tokens=auth_response.tokens)
position_service = PositionService(client)

# Create a market position
position = CreatePosition(
    currencyCode="USD",
    direction="BUY", 
    epic="CS.D.GBPUSD.TODAY.IP",
    orderType="MARKET",
    size=1
)
deal_ref = position_service.create_position(position)

# Get all open positions
positions = position_service.get_open_positions()

# Get specific position
position = position_service.get_open_position_by_deal_id("deal_id")

# Close position
from ig_trading_lib.trading.positions import ClosePosition
close_pos = ClosePosition.from_create(position)
position_service.close_position(close_pos)
```

### Order Service

```python
from ig_trading_lib.trading import OrderService, CreateWorkingOrder, IGClient

client = IGClient(base_url="https://demo-api.ig.com", api_key="your_api_key", tokens=auth_response.tokens)
order_service = OrderService(client)

# Create a working order
order = CreateWorkingOrder(
    currencyCode="USD",
    direction="BUY",
    epic="CS.D.GBPUSD.TODAY.IP", 
    level=1.2500,
    size=1,
    type="LIMIT"
)
deal_ref = order_service.create_order(order)

# Get all working orders
orders = order_service.get_orders()

# Delete working order
order_service.delete_order("deal_id")
```

## Environment Variables

For testing and development, you can set these environment variables:

```bash
export IG_API_KEY="your_api_key"
export IG_ACCOUNT_IDENTIFIER="your_account_identifier" 
export IG_ACCOUNT_PASSWORD="your_account_password"
export IG_BASE_URL="https://demo-api.ig.com"  # or https://api.ig.com for live
```

## Contributing

Contributions are welcome! Please feel free to fork the repository and create a pull request.

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd ig-trading-lib

# Install dependencies
poetry install

# Run tests
make test

# Run linting
make lint
```

## License

This project is licensed under the MIT License.

## Contact

If you have any questions, feel free to reach out to me on GitHub.

## Disclaimer

This library is not affiliated with, authorized, endorsed, or in any way officially connected with IG Markets Ltd. Use at your own risk.