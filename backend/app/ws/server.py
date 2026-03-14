import asyncio
import json
from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
import logging
from core.redis_manager import redis_manager

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.queues: Dict[str, asyncio.Queue] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int) -> None:
        """Accept and store connection"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
            self.queues[user_id] = asyncio.Queue()
        
        self.active_connections[user_id].add(websocket)
    
    async def disconnect(self, websocket: WebSocket, user_id: int) -> None:
        """Remove connection"""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                del self.queues[user_id]
    
    async def broadcast_to_user(self, user_id: int, message: dict) -> None:
        """Send message to specific user"""
        if user_id in self.queues:
            await self.queues[user_id].put(message)
    
    async def send_message(self, websocket: WebSocket, message: dict) -> None:
        """Send message to specific connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def update_queue(self, user_id: int) -> None:
        """Process pending messages in queue"""
        if user_id not in self.queues:
            return
        
        while not self.queues[user_id].empty():
            message = await self.queues[user_id].get()
            for connection in self.active_connections.get(user_id, set()):
                await self.send_message(connection, message)
    
    async def broadcast(self, message: dict) -> None:
        """Broadcast message to all connected clients"""
        for user_id, connections in self.active_connections.items():
            await self.broadcast_to_user(user_id, message)

class WebSocketServer:
    """WebSocket server for real-time updates"""
    
    def __init__(self):
        self.manager = ConnectionManager()
        self.heartbeat_task = None
        self._running = False
    
    async def on_connect(self, websocket: WebSocket, user_id: int) -> None:
        """Handle new connection"""
        await self.manager.connect(websocket, user_id)
        logger.info(f"User {user_id} connected")
    
    async def on_disconnect(self, websocket: WebSocket, user_id: int) -> None:
        """Handle disconnection"""
        await self.manager.disconnect(websocket, user_id)
        logger.info(f"User {user_id} disconnected")
    
    async def on_message(self, websocket: WebSocket, message: dict) -> None:
        """Handle incoming message"""
        try:
            msg_type = message.get('type')
            user_id = websocket.user_id if hasattr(websocket, 'user_id') else None
            
            if msg_type == 'subscribe':
                symbols = message.get('symbols', [])
                await self.handle_subscribe(user_id, symbols)
            elif msg_type == 'unsubscribe':
                symbols = message.get('symbols', [])
                await self.handle_unsubscribe(user_id, symbols)
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self.manager.send_message(websocket, {
                'type': 'error',
                'data': {'message': str(e)}
            })
    
    async def handle_subscribe(self, user_id: int, symbols: list) -> None:
        """Handle subscription request"""
        # Store subscription information
        if user_id not in self.manager.queues:
            self.manager.queues[user_id] = asyncio.Queue()
        
        await self.manager.broadcast_to_user(user_id, {
            'type': 'subscription',
            'data': {'status': 'subscribed', 'symbols': symbols}
        })
    
    async def handle_unsubscribe(self, user_id: int, symbols: list) -> None:
        """Handle unsubscription request"""
        await self.manager.broadcast_to_user(user_id, {
            'type': 'subscription',
            'data': {'status': 'unsubscribed', 'symbols': symbols}
        })
    
    async def send_order_update(self, order_data: dict) -> None:
        """Send order update to all connected clients"""
        await self.manager.broadcast({
            'type': 'order_update',
            'data': order_data
        })
    
    async def send_trade_update(self, trade_data: dict) -> None:
        """Send trade update to all connected clients"""
        await self.manager.broadcast({
            'type': 'trade',
            'data': trade_data
        })
    
    async def send_position_update(self, position_data: dict) -> None:
        """Send position update to all connected clients"""
        await self.manager.broadcast({
            'type': 'position_update',
            'data': position_data
        })
    
    async def send_log_update(self, log_data: dict) -> None:
        """Send log update to all connected clients"""
        await self.manager.broadcast({
            'type': 'log',
            'data': log_data
        })
    
    async def start_heartbeat(self, interval: int = 30) -> None:
        """Start heartbeat task"""
        if self._running:
            return
        
        self._running = True
        
        while self._running:
            try:
                now = asyncio.get_event_loop().time()
                await self.manager.broadcast({
                    'type': 'heartbeat',
                    'data': {'timestamp': now}
                })
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                await asyncio.sleep(interval)
    
    async def stop(self) -> None:
        """Stop server"""
        self._running = False
    
    def start(self) -> None:
        """Start the WebSocket server"""
        from core.config import get_settings
        settings = get_settings()
        asyncio.create_task(self.start_heartbeat(settings.WS_HEARTBEAT_INTERVAL))

# Global WebSocket server instance
ws_server = WebSocketServer()
