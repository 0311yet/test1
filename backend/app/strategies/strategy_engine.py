from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
from datetime import datetime
from core.exceptions import ExchangeError
from core.redis_manager import redis_manager
from core.config import get_settings

settings = get_settings()

class Strategy(ABC):
    """Abstract base class for all strategies"""
    
    def __init__(self, name: str, symbol: str, config: Dict[str, Any], user_id: int):
        self.name = name
        self.symbol = symbol
        self.config = config
        self.user_id = user_id
        self.is_active = False
        self.last_triggered_at: Optional[datetime] = None
        self.execution_count = 0
    
    @abstractmethod
    async def should_trigger(self, current_price: float) -> bool:
        """Determine if strategy should trigger"""
        pass
    
    @abstractmethod
    async def execute(self):
        """Execute trading action"""
        pass
    
    async def on_trigger(self):
        """Called when strategy is triggered"""
        self.last_triggered_at = datetime.utcnow()
        self.execution_count += 1
    
    async def stop(self):
        """Stop strategy execution"""
        self.is_active = False

class PriceTriggerStrategy(Strategy):
    """Price trigger strategy example"""
    
    def __init__(self, name: str, symbol: str, config: Dict[str, Any], user_id: int):
        super().__init__(name, symbol, config, user_id)
        
        self.trigger_price = config.get('trigger_price', 0.0)
        self.action = config.get('action', 'buy')
        self.quantity = config.get('quantity', 0.0)
        self.stop_loss = config.get('stop_loss', None)
        self.take_profit = config.get('take_profit', None)
        self.price_history = []
        self.max_history = 10
    
    async def should_trigger(self, current_price: float) -> bool:
        """Check if price has reached trigger level"""
        self.price_history.append(current_price)
        if len(self.price_history) > self.max_history:
            self.price_history.pop(0)
        
        if self.action == 'buy':
            if current_price >= self.trigger_price:
                return True
        elif self.action == 'sell':
            if current_price <= self.trigger_price:
                return True
        
        return False
    
    async def execute(self):
        """Execute buy or sell order"""
        if not self.is_active:
            return
        
        try:
            from services.exchange_service import ExchangeService
            
            exchange_service = ExchangeService()
            
            order_type = 'market'
            
            if self.action == 'buy':
                order = await exchange_service.place_order(
                    symbol=self.symbol,
                    side='buy',
                    order_type=order_type,
                    quantity=self.quantity
                )
            elif self.action == 'sell':
                order = await exchange_service.place_order(
                    symbol=self.symbol,
                    side='sell',
                    order_type=order_type,
                    quantity=self.quantity
                )
            
            self.last_triggered_at = datetime.utcnow()
            self.execution_count += 1
            
            return {
                'strategy': self.name,
                'symbol': self.symbol,
                'action': self.action,
                'price': current_price if 'current_price' in locals() else None,
                'quantity': self.quantity,
                'order_id': order.get('id', 'unknown')
            }
        except Exception as e:
            raise ExchangeError(f"Failed to execute strategy {self.name}: {str(e)}")

class StrategyEngine:
    """Strategy execution engine"""
    
    _instance = None
    _strategies = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._strategies = {}
        return cls._instance
    
    async def add_strategy(self, strategy: Strategy) -> None:
        """Add a strategy to the engine"""
        self._strategies[strategy.name] = strategy
        strategy.is_active = True
    
    async def remove_strategy(self, name: str) -> None:
        """Remove a strategy from the engine"""
        if name in self._strategies:
            await self._strategies[name].stop()
            del self._strategies[name]
    
    async def execute_all_strategies(self) -> list:
        """Execute all active strategies"""
        results = []
        
        for name, strategy in self._strategies.items():
            if not strategy.is_active:
                continue
            
            try:
                # Get current price
                from services.exchange_service import ExchangeService
                
                exchange_service = ExchangeService()
                current_price = await exchange_service.get_mark_price(strategy.symbol)
                
                if current_price is None:
                    continue
                
                # Check if strategy should trigger
                if await strategy.should_trigger(current_price):
                    result = await strategy.execute()
                    if result:
                        results.append(result)
                        await strategy.on_trigger()
            except Exception as e:
                print(f"Strategy execution error {name}: {str(e)}")
        
        return results
    
    async def check_all_strategies(self) -> list:
        """Check all strategies for trigger conditions"""
        results = []
        
        for name, strategy in self._strategies.items():
            if not strategy.is_active:
                continue
            
            try:
                from services.exchange_service import ExchangeService
                
                exchange_service = ExchangeService()
                current_price = await exchange_service.get_mark_price(strategy.symbol)
                
                if current_price is not None and await strategy.should_trigger(current_price):
                    results.append({
                        'strategy': name,
                        'should_trigger': True,
                        'current_price': current_price,
                        'trigger_price': strategy.trigger_price
                    })
            except Exception as e:
                print(f"Strategy check error {name}: {str(e)}")
        
        return results
    
    async def get_strategy_status(self) -> Dict[str, Any]:
        """Get status of all strategies"""
        return {
            name: {
                'is_active': strategy.is_active,
                'last_triggered_at': strategy.last_triggered_at,
                'execution_count': strategy.execution_count,
                'config': strategy.config
            }
            for name, strategy in self._strategies.items()
        }
