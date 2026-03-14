from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from core.exceptions import ValidationError, NotFoundError, ExchangeError, AuthenticationError
from models import User, Order, Trade, Position, Strategy
from schemas import (
    APIKeyRequest, UserResponse,
    OrderRequest, OrderResponse,
    PositionResponse, TradeResponse,
    StrategyRequest, StrategyResponse,
    BalanceRequest, BalanceResponse,
    LogResponse
)
from services.exchange_service import ExchangeService
from strategies.strategy_engine import StrategyEngine

router = APIRouter(prefix="/api", tags=["trading"])

# In-memory storage for simplicity
active_strategies = {}

@router.post("/api-keys", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def save_api_keys(request: APIKeyRequest):
    """Save user API keys"""
    db: Session = next(get_db())
    
    # Check if user already exists
    existing_user = db.query(User).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with API keys"
        )
    
    user = User(
        api_key=request.api_key,
        secret_key=request.secret_key,
        passphrase=request.passphrase,
        exchange=request.exchange
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return UserResponse.from_orm(user)

@router.get("/balance", response_model=BalanceResponse)
async def get_balance(request: BalanceRequest = Depends()):
    """Get account balance and positions"""
    try:
        exchange_service = ExchangeService()
        balance_data = await exchange_service.get_balance()
        return BalanceResponse(**balance_data)
    except ExchangeError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_request: OrderRequest):
    """Create a new order"""
    try:
        exchange_service = ExchangeService()
        
        order = await exchange_service.place_order(
            symbol=order_request.symbol,
            side=order_request.side,
            order_type=order_request.type,
            quantity=order_request.quantity,
            price=order_request.price,
            reduce_only=order_request.reduce_only,
            post_only=order_request.post_only
        )
        
        # Store order in database
        db: Session = next(get_db())
        db_order = Order(
            user_id=1,
            symbol=order_request.symbol,
            side=order_request.side,
            type=order_request.type,
            quantity=order_request.quantity,
            price=order_request.price,
            status="active",
            order_id=order.get('info', {}).get('data', [{}])[0].get('ordId')
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # Send WebSocket update
        from ws.server import ws_server
        await ws_server.send_order_update({
            'order_id': db_order.order_id,
            'symbol': order_request.symbol,
            'side': order_request.side,
            'type': order_request.type,
            'quantity': order_request.quantity,
            'status': 'active',
            'created_at': db_order.created_at.isoformat()
        })
        
        return OrderResponse.from_orm(db_order)
    except ExchangeError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(limit: int = 50, offset: int = 0):
    """Get list of orders"""
    try:
        db: Session = next(get_db())
        orders = db.query(Order).offset(offset).limit(limit).all()
        return [OrderResponse.from_orm(order) for order in orders]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/orders/{order_id}", response_model=Optional[OrderResponse])
async def get_order(order_id: int):
    """Get specific order"""
    try:
        db: Session = next(get_db())
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None
        
        # Refresh order status from exchange
        exchange_service = ExchangeService()
        exchange_order = await exchange_service.get_order(order.order_id, order.symbol)
        
        order.status = exchange_order.get('status', order.status)
        order.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(order)
        
        return OrderResponse.from_orm(order)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/orders/{order_id}", response_model=dict)
async def cancel_order(order_id: int):
    """Cancel an order"""
    try:
        db: Session = next(get_db())
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        exchange_service = ExchangeService()
        await exchange_service.cancel_order(order.order_id, order.symbol)
        
        order.status = "cancelled"
        order.updated_at = datetime.utcnow()
        db.commit()
        
        # Send WebSocket update
        from ws.server import ws_server
        await ws_server.send_order_update({
            'order_id': order.order_id,
            'symbol': order.symbol,
            'status': 'cancelled'
        })
        
        return {'message': 'Order cancelled successfully'}
    except ExchangeError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/positions", response_model=List[PositionResponse])
async def get_positions():
    """Get all positions"""
    try:
        exchange_service = ExchangeService()
        balance_data = await exchange_service.get_balance()
        return [
            PositionResponse(
                symbol=pos['symbol'],
                side=pos['side'],
                quantity=pos['quantity'],
                avg_price=pos['avg_price'],
                unrealized_pnl=pos['unrealized_pnl'],
                mark_price=pos['mark_price'],
                liquidation_price=pos['liquidation_price'],
                margin_type='cross'
            )
            for pos in balance_data.get('positions', [])
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/trades", response_model=List[TradeResponse])
async def get_trades(limit: int = 100):
    """Get trade history"""
    try:
        db: Session = next(get_db())
        trades = db.query(Trade).limit(limit).all()
        return [TradeResponse.from_orm(trade) for trade in trades]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/strategies", response_model=StrategyResponse, status_code=status.HTTP_201_CREATED)
async def create_strategy(strategy_request: StrategyRequest):
    """Create a new strategy"""
    try:
        db: Session = next(get_db())
        
        strategy = Strategy(
            user_id=1,
            name=strategy_request.name,
            type=strategy_request.type,
            symbol=strategy_request.symbol,
            config=strategy_request.config,
            is_active=strategy_request.is_active
        )
        
        db.add(strategy)
        db.commit()
        db.refresh(strategy)
        
        # If active, add to strategy engine
        if strategy.is_active:
            from strategies.strategy_engine import StrategyEngine
            strategy_engine = StrategyEngine()
            
            # Create strategy instance based on type
            if strategy_request.type == 'price_trigger':
                from strategies.strategy_engine import PriceTriggerStrategy
                strat_instance = PriceTriggerStrategy(
                    name=strategy.name,
                    symbol=strategy.symbol,
                    config=strategy_request.config,
                    user_id=strategy.user_id
                )
                await strategy_engine.add_strategy(strat_instance)
                active_strategies[strategy.id] = strategy_engine
        
        return StrategyResponse.from_orm(strategy)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/strategies", response_model=List[StrategyResponse])
async def get_strategies():
    """Get all strategies"""
    try:
        db: Session = next(get_db())
        strategies = db.query(Strategy).all()
        return [StrategyResponse.from_orm(strat) for strat in strategies]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/strategies/{strategy_id}", response_model=Optional[StrategyResponse])
async def get_strategy(strategy_id: int):
    """Get specific strategy"""
    try:
        db: Session = next(get_db())
        strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
        if not strategy:
            return None
        return StrategyResponse.from_orm(strategy)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/strategies/{strategy_id}/toggle", response_model=StrategyResponse)
async def toggle_strategy(strategy_id: int):
    """Toggle strategy active status"""
    try:
        db: Session = next(get_db())
        strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
        if not strategy:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")
        
        strategy.is_active = not strategy.is_active
        strategy.updated_at = datetime.utcnow()
        
        # Update strategy engine
        if strategy.is_active:
            from strategies.strategy_engine import StrategyEngine, PriceTriggerStrategy
            strategy_engine = StrategyEngine()
            
            if strategy.type == 'price_trigger':
                strat_instance = PriceTriggerStrategy(
                    name=strategy.name,
                    symbol=strategy.symbol,
                    config=strategy.config,
                    user_id=strategy.user_id
                )
                await strategy_engine.add_strategy(strat_instance)
                active_strategies[strategy.id] = strategy_engine
        else:
            if strategy.id in active_strategies:
                del active_strategies[strategy.id]
        
        db.commit()
        db.refresh(strategy)
        
        return StrategyResponse.from_orm(strategy)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/strategies/{strategy_id}/execute", response_model=dict)
async def execute_strategy(strategy_id: int):
    """Manually execute a strategy"""
    try:
        if strategy_id not in active_strategies:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not active")
        
        strategy_engine = active_strategies[strategy_id]
        result = await strategy_engine.execute_all_strategies()
        
        return {
            'message': 'Strategy executed',
            'results': result
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/strategies/check", response_model=dict)
async def check_strategies():
    """Check all strategies for trigger conditions"""
    try:
        from strategies.strategy_engine import StrategyEngine
        strategy_engine = StrategyEngine()
        check_results = await strategy_engine.check_all_strategies()
        
        return {
            'message': 'Strategy check completed',
            'check_results': check_results
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

from datetime import datetime
