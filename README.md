# Crypto Trading System - MVP

A production-ready minimal MVP crypto trading system for OKX built with clean architecture principles.

## Tech Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- TailwindCSS
- React Query (TanStack Query)
- WebSocket client

### Backend
- FastAPI (Python 3.11+)
- Pydantic
- SQLAlchemy 2.0
- PostgreSQL
- Redis

### Trading
- ccxt library for exchange integration
- OKX WebSocket for market data

### Infrastructure
- Docker
- Docker Compose

## Features

1. **User Management**: Store and manage OKX API keys
2. **Balance & Positions**: Fetch account balance and positions
3. **Order Management**: Place and cancel orders
4. **Real-time Updates**: WebSocket streaming for order status and market data
5. **Strategy Engine**: Support for custom trading strategies
6. **Real-time Logs**: Monitor system activities and trading operations
7. **Database Persistence**: PostgreSQL for orders, trades, and strategy configs
8. **Caching**: Redis for market data and temporary states

## Project Structure

```
root/
  frontend/
    app/
    components/
    hooks/
    lib/
    services/
    types/

  backend/
    app/
      api/
      core/
      models/
      schemas/
      services/
      exchange/
      strategies/
      ws/
      tasks/

  docker/
  docker-compose.yml
```

## Installation & Setup

### Prerequisites

- Docker Desktop
- Docker Compose
- OKX API credentials (obtain from OKX exchange)

### Setup Steps

1. **Clone and navigate to project directory**

```bash
cd crypto-trading-system
```

2. **Configure environment variables**

Edit `backend/.env` file with your OKX API credentials:

```bash
OKX_API_KEY=your_actual_api_key
OKX_SECRET_KEY=your_actual_secret_key
OKX_PASSPHRASE=your_actual_passphrase
```

3. **Start the system**

```bash
docker compose up -d
```

4. **Access the application**

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

5. **Stop the system**

```bash
docker compose down
```

## API Endpoints

### Authentication
- `POST /api/api-keys` - Save API keys

### Trading Operations
- `GET /api/balance` - Get account balance and positions
- `POST /api/orders` - Create new order
- `GET /api/orders` - Get list of orders
- `GET /api/orders/{order_id}` - Get specific order
- `DELETE /api/orders/{order_id}` - Cancel order
- `GET /api/positions` - Get all positions
- `GET /api/trades` - Get trade history

### Strategy Management
- `POST /api/strategies` - Create new strategy
- `GET /api/strategies` - Get all strategies
- `GET /api/strategies/{strategy_id}` - Get specific strategy
- `PUT /api/strategies/{strategy_id}/toggle` - Toggle strategy active status
- `POST /api/strategies/{strategy_id}/execute` - Manually execute strategy
- `POST /api/strategies/check` - Check all strategies for trigger conditions

### WebSocket
- `WS /ws` - Real-time updates for orders, positions, and logs

## Example Strategies

### Price Trigger Strategy

The system includes a price trigger strategy that automatically executes trades when price reaches a specified level.

**Configuration:**

- `name`: Strategy name (e.g., "price_trigger_strategy")
- `type`: "price_trigger"
- `symbol`: Trading pair (e.g., "BTC/USDT")
- `trigger_price`: Price level to trigger the action
- `action`: "buy" or "sell"
- `quantity`: Number of units to trade
- `stop_loss`: Optional stop loss price
- `take_profit`: Optional take profit price

**Usage:**

1. Create a strategy with the form on the dashboard
2. Toggle the strategy active
3. The strategy will automatically execute when price reaches the trigger level

## Architecture

### Clean Architecture Principles

1. **Separation of Concerns**: Business logic separated from API routes
2. **Service Layer Architecture**: Exchange service handles all trading operations
3. **Repository Pattern**: Database operations through models and schemas
4. **Dependency Injection**: Core components injected where needed

### Key Components

#### Backend

- **Exchange Service**: Handles all exchange operations using ccxt
- **Strategy Engine**: Executes trading strategies based on market conditions
- **WebSocket Server**: Streams real-time updates to clients
- **Database Layer**: PostgreSQL persistence with SQLAlchemy
- **Cache Layer**: Redis for performance optimization

#### Frontend

- **React Query**: Manages server state and caching
- **Components**: Modular UI components for different trading operations
- **API Client**: Abstraction for REST and WebSocket communication

## Security Considerations

1. **API Keys**: Stored securely in environment variables
2. **HTTPS**: Production deployment should use HTTPS
3. **Rate Limiting**: Configured in exchange service
4. **Input Validation**: All inputs validated through Pydantic schemas

## Development

### Backend Development

```bash
cd backend
docker compose exec backend bash
```

### Frontend Development

```bash
cd frontend
docker compose exec frontend bash
npm run dev
```

### Running Tests

Tests can be run after implementing them based on the project structure.

## Monitoring

The system includes real-time logging through the WebSocket interface and UI log panel.

## Troubleshooting

### Common Issues

1. **Connection Issues**: Check API credentials and network connectivity
2. **Database Issues**: Verify PostgreSQL container is healthy
3. **Redis Issues**: Check Redis container logs
4. **Exchange Errors**: Ensure API credentials have sufficient permissions

## License

MIT

## Contributing

Contributions are welcome! Please follow the existing code structure and architecture patterns.
