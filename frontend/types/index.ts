export interface Order {
  id: number;
  symbol: string;
  side: string;
  type: string;
  quantity: number;
  price: number | null;
  status: string;
  order_id: string | null;
  client_order_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface Position {
  id: number;
  symbol: string;
  side: string;
  quantity: number;
  avg_price: number;
  unrealized_pnl: number;
  mark_price: number;
  liquidation_price: number | null;
  margin_type: string;
}

export interface Trade {
  id: number;
  order_id: number | null;
  symbol: string;
  side: string;
  quantity: number;
  price: number;
  fee: number | null;
  fee_currency: string | null;
  tx_id: string | null;
  created_at: string;
}

export interface Strategy {
  id: number;
  user_id: number;
  name: string;
  type: string;
  symbol: string;
  config: Record<string, any>;
  is_active: boolean;
  last_triggered_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Balance {
  total_equity: number;
  available_balance: number;
  margin_balance: number;
  unrealized_pnl: number;
  positions: Position[];
}

export interface OrderRequest {
  symbol: string;
  side: 'buy' | 'sell';
  type: 'limit' | 'market';
  quantity: number;
  price?: number;
  reduce_only?: boolean;
  post_only?: boolean;
}

export interface StrategyRequest {
  name: string;
  type: 'price_trigger' | 'ema_cross' | 'simple';
  symbol: string;
  config: Record<string, any>;
  is_active?: boolean;
}

export interface LogEntry {
  level: string;
  source: string;
  message: string;
  timestamp: string;
}
