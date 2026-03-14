# Crypto Trading System - MVP Setup Guide

## Quick Start

### 1. Setup Environment Variables

Edit the `backend/.env` file and add your OKX API credentials:

```bash
OKX_API_KEY=your_okx_api_key
OKX_SECRET_KEY=your_okx_secret_key
OKX_PASSPHRASE=your_okx_passphrase
```

**Note:** Get your API keys from OKX exchange settings.

### 2. Start the System

```bash
docker compose up -d
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Project Structure Overview

```
crypto-trading-system/
├── frontend/
│   ├── app/
│   │   ├── page.tsx          # Main dashboard page
│   │   ├── layout.tsx        # Root layout
│   │   └── globals.css       # Global styles
│   ├── components/
│   │   ├── OrderForm.tsx     # Order placement form
│   │   ├── OrderTable.tsx    # Order list display
│   │   ├── PositionTable.tsx # Position display
│   │   ├── BalanceCard.tsx   # Account balance card
│   │   ├── StrategyForm.tsx  # Strategy configuration
│   │   ├── LogPanel.tsx      # Real-time logs
│   │   └── ui/               # UI component library
│   ├── lib/
│   │   ├── api.ts            # API client
│   │   ├── hooks.ts          # React Query hooks
│   │   └── utils.ts          # Utility functions
│   └── types/
│       └── index.ts          # TypeScript definitions
│
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application entry
│   │   ├── core/
│   │   │   ├── config.py     # Application settings
│   │   │   ├── database.py   # Database base model
│   │   │   ├── database_manager.py  # DB session manager
│   │   │   ├── redis_manager.py     # Redis connection manager
│   │   │   ├── exceptions.py        # Custom exceptions
│   │   │   └── celery_db.py         # Celery database config
│   │   ├── models/
│   │   │   └── __init__.py   # SQLAlchemy models
│   │   ├── schemas/
│   │   │   └── __init__.py   # Pydantic schemas
│   │   ├── services/
│   │   │   └── exchange_service.py   # Exchange operations
│   │   ├── strategies/
│   │   │   └── strategy_engine.py    # Trading strategies
│   │   ├── ws/
│   │   │   └── server.py    # WebSocket server
│   │   └── api/
│   │       └── routes.py    # REST API endpoints
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Environment variables
│   └── .env.example          # Example env file
│
├── docker/
├── docker-compose.yml        # Main docker configuration
├── docker-compose.dev.yml    # Development override
└── README.md                 # Project documentation
```

## Core Components

### Backend Services

1. **Exchange Service** (`services/exchange_service.py`)
   - Handles all OKX exchange operations using ccxt
   - Manages balance, orders, positions
   - Caches market data in Redis

2. **Strategy Engine** (`strategies/strategy_engine.py`)
   - Executes trading strategies based on market conditions
   - Example: Price trigger strategy
   - Supports multiple strategy types

3. **WebSocket Server** (`ws/server.py`)
   - Real-time updates for orders, positions, and logs
   - Broadcasts market data to connected clients

4. **API Routes** (`api/routes.py`)
   - REST endpoints for all trading operations
   - CRUD operations for strategies and orders

### Frontend Components

1. **Dashboard** (`app/page.tsx`)
   - Main interface with tabs for different operations
   - Real-time data updates via WebSocket

2. **Order Management**
   - Place market and limit orders
   - View order history
   - Cancel orders

3. **Position Management**
   - View open positions
   - Monitor unrealized PnL

4. **Strategy Configuration**
   - Create price trigger strategies
   - Toggle strategy active status
   - Manual strategy execution

## Example Usage

### Placing an Order

1. Navigate to Dashboard
2. Click "Orders" tab
3. Fill in order details:
   - Symbol: BTC/USDT
   - Side: Buy/Sell
   - Type: Market/Limit
   - Quantity: 0.001
4. Click "BUY BTC/USDT" button

### Creating a Strategy

1. Navigate to Dashboard
2. Click "Strategies" tab
3. Fill in strategy details:
   - Name: "btc_trigger"
   - Type: Price Trigger
   - Symbol: BTC/USDT
   - Trigger Price: 50000
   - Action: Buy
   - Quantity: 0.001
4. Click "Create Strategy"
5. Toggle strategy active to start execution

### Monitoring

1. Navigate to "Logs" tab
2. View real-time system logs
3. Monitor order status updates
4. Check position changes

## API Endpoints Reference

### Authentication
- `POST /api/api-keys` - Save API credentials

### Balance & Positions
- `GET /api/balance` - Get account info
- `GET /api/positions` - Get open positions

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders` - List orders
- `GET /api/orders/{id}` - Get order details
- `DELETE /api/orders/{id}` - Cancel order

### Strategies
- `POST /api/strategies` - Create strategy
- `GET /api/strategies` - List strategies
- `GET /api/strategies/{id}` - Get strategy
- `PUT /api/strategies/{id}/toggle` - Toggle active status
- `POST /api/strategies/{id}/execute` - Execute strategy
- `POST /api/strategies/check` - Check triggers

### WebSocket
- `WS /ws` - Real-time updates

## Development

### Running Backend with Live Reload

```bash
docker compose -f docker-compose.dev.yml up
```

### Accessing Backend Shell

```bash
docker compose exec backend bash
```

### Accessing Database

```bash
docker compose exec postgres psql -U trader -d crypto_trading
```

### Accessing Redis

```bash
docker compose exec redis redis-cli
```

## Testing

The system includes basic functionality for:
- ✓ Order placement (market/limit)
- ✓ Order cancellation
- ✓ Position monitoring
- ✓ Strategy creation and execution
- ✓ Real-time WebSocket updates
- ✓ Balance and PnL tracking

## Security Notes

⚠️ **Important Security Considerations**

1. **Never commit API keys** - Keep them in `.env` file only
2. **Use strong passwords** for database users
3. **Enable HTTPS** in production
4. **Restrict API key permissions** - Only give necessary trading permissions
5. **Monitor API usage** regularly

## Troubleshooting

### Connection Issues

```bash
# Check service status
docker compose ps

# Check logs
docker compose logs backend
docker compose logs frontend
```

### Database Issues

```bash
# Restart database
docker compose restart postgres

# Reset database (deletes all data)
docker compose down -v
docker compose up -d
```

### API Errors

1. Verify API credentials are correct
2. Check API key has sufficient permissions
3. Ensure OKX API key is active
4. Check network connectivity

## Future Enhancements

Potential improvements:
- Advanced strategy types (EMA crossover, MACD, etc.)
- Risk management tools
- Performance analytics
- Multiple account support
- Advanced order types (OCO, Trailing stop)
- Mobile app support
- Advanced reporting

## Support

For issues or questions:
1. Check the README.md file
2. Review API documentation at `/docs`
3. Check system logs in the frontend
4. Verify service status with docker compose
