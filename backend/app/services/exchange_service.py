import ccxt.async_support as ccxt
import asyncio
from typing import Optional, Dict, Any
from core.exceptions import ExchangeError, AuthenticationError
from core.redis_manager import redis_manager
from core.config import get_settings

settings = get_settings()

class ExchangeService:
    """Exchange service using ccxt"""
    
    _instance = None
    _exchange = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._exchange = None
        return cls._instance
    
    async def _initialize_exchange(self) -> ccxt.Exchange:
        """Initialize and cache exchange instance"""
        if self._exchange is None:
            try:
                exchange_config = {
                    "apiKey": settings.OKX_API_KEY,
                    "secret": settings.OKX_SECRET_KEY,
                    "password": settings.OKX_PASSPHRASE,
                    "enableRateLimit": True,
                    "options": {
                        "defaultType": "spot"
                    }
                }
                self._exchange = ccxt.okx(exchange_config)
                await self._exchange.load_markets()
            except Exception as e:
                raise AuthenticationError(f"Failed to initialize exchange: {str(e)}")
        return self._exchange
    
    async def get_balance(self) -> Dict[str, Any]:
        """Get account balance"""
        try:
            exchange = await self._initialize_exchange()
            
            # Get accounts
            accounts = await exchange.fetch_balance()
            
            # Process balance
            total_equity = 0.0
            available_balance = 0.0
            margin_balance = 0.0
            unrealized_pnl = 0.0
            positions = []
            
            # Calculate total equity and available balance
            for currency, balance in accounts.get('total', {}).items():
                if float(balance['free']) > 0:
                    available_balance += float(balance['free'])
                    total_equity += float(balance['total'])
            
            # Get positions
            positions_data = await exchange.fetch_positions()
            for position in positions_data:
                if position and float(position.get('contracts', 0)) != 0:
                    positions.append({
                        'symbol': position.get('symbol'),
                        'side': position.get('side', ''),
                        'quantity': float(position.get('contracts', 0)),
                        'avg_price': float(position.get('averagePrice', 0)),
                        'mark_price': float(position.get('markPrice', 0)),
                        'unrealized_pnl': float(position.get('unrealizedPnl', 0)),
                        'liquidation_price': position.get('liquidationPrice')
                    })
                    margin_balance += float(position.get('notional', 0))
                    unrealized_pnl += float(position.get('unrealizedPnl', 0))
            
            return {
                'total_equity': total_equity,
                'available_balance': available_balance,
                'margin_balance': margin_balance,
                'unrealized_pnl': unrealized_pnl,
                'positions': positions
            }
        except Exception as e:
            raise ExchangeError(f"Failed to get balance: {str(e)}")
    
    async def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        reduce_only: bool = False,
        post_only: bool = False
    ) -> Dict[str, Any]:
        """Place a new order"""
        try:
            exchange = await self._initialize_exchange()
            
            order_params = {
                'type': order_type,
                'side': side,
                'amount': quantity,
                'reduceOnly': reduce_only,
                'postOnly': post_only
            }
            
            if price:
                order_params['price'] = price
            
            order = await exchange.create_order(symbol, **order_params)
            
            # Cache market data for 5 minutes
            if 'info' in order:
                if 'result' in order['info']:
                    result = order['info']['result']
                    order_data = result.get('data', [{}])[0]
                    symbol_info = order_data.get('ordId', '')
                    
                    market_data = await exchange.fetch_order(symbol, order_data.get('ordId', ''), symbol_info)
                    
                    if market_data and 'info' in market_data:
                        cache_key = f"market:{symbol}"
                        await redis_manager.get_client().setex(
                            cache_key,
                            300,
                            str(market_data['info'])
                        )
            
            return order
        except Exception as e:
            raise ExchangeError(f"Failed to place order: {str(e)}")
    
    async def cancel_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """Cancel an existing order"""
        try:
            exchange = await self._initialize_exchange()
            return await exchange.cancel_order(order_id, symbol)
        except Exception as e:
            raise ExchangeError(f"Failed to cancel order: {str(e)}")
    
    async def get_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """Get order status"""
        try:
            exchange = await self._initialize_exchange()
            return await exchange.fetch_order(order_id, symbol)
        except Exception as e:
            raise ExchangeError(f"Failed to get order: {str(e)}")
    
    async def get_mark_price(self, symbol: str) -> Optional[float]:
        """Get current market price"""
        try:
            exchange = await self._initialize_exchange()
            
            # Check cache first
            cache_key = f"market:{symbol}"
            cached_data = await redis_manager.get_client().get(cache_key)
            
            if cached_data:
                import json
                market_info = json.loads(cached_data)
                if 'markPx' in market_info:
                    return float(market_info['markPx'])
            
            # Fetch fresh data if not cached
            ticker = await exchange.fetch_ticker(symbol)
            return float(ticker.get('last', 0))
        except Exception as e:
            return None
    
    async def get_all_open_orders(self, symbol: Optional[str] = None) -> list:
        """Get all open orders"""
        try:
            exchange = await self._initialize_exchange()
            if symbol:
                return await exchange.fetch_orders(symbol)
            return await exchange.fetch_open_orders()
        except Exception as e:
            raise ExchangeError(f"Failed to get open orders: {str(e)}")
    
    async def close(self) -> None:
        """Close exchange connection"""
        if self._exchange:
            await self._exchange.close()
            self._exchange = None
