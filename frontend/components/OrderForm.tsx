"use client";

import { useState } from "react";
import { useCreateOrder } from "@/lib/hooks";
import { OrderRequest } from "@/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function OrderForm() {
  const [symbol, setSymbol] = useState("BTC/USDT");
  const [side, setSide] = useState<"buy" | "sell">("buy");
  const [type, setType] = useState<"limit" | "market">("market");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");
  const createOrder = useCreateOrder();
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const qty = parseFloat(quantity);
    if (qty <= 0) {
      setError("Quantity must be greater than 0");
      return;
    }

    if (type === "limit" && (!price || parseFloat(price) <= 0)) {
      setError("Price must be greater than 0 for limit orders");
      return;
    }

    const orderData: OrderRequest = {
      symbol,
      side,
      type,
      quantity: qty,
      price: type === "limit" ? parseFloat(price) : undefined,
    };

    try {
      await createOrder.mutateAsync(orderData);
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Place Order</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="symbol">Symbol</Label>
            <Input
              id="symbol"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              placeholder="BTC/USDT"
            />
          </div>

          <div>
            <Label htmlFor="side">Side</Label>
            <div className="flex gap-2">
              <Button
                type="button"
                variant={side === "buy" ? "default" : "outline"}
                onClick={() => setSide("buy")}
                className="flex-1"
              >
                Buy
              </Button>
              <Button
                type="button"
                variant={side === "sell" ? "default" : "outline"}
                onClick={() => setSide("sell")}
                className="flex-1"
              >
                Sell
              </Button>
            </div>
          </div>

          <div>
            <Label htmlFor="type">Order Type</Label>
            <div className="flex gap-2">
              <Button
                type="button"
                variant={type === "market" ? "default" : "outline"}
                onClick={() => setType("market")}
                className="flex-1"
              >
                Market
              </Button>
              <Button
                type="button"
                variant={type === "limit" ? "default" : "outline"}
                onClick={() => setType("limit")}
                className="flex-1"
              >
                Limit
              </Button>
            </div>
          </div>

          <div>
            <Label htmlFor="quantity">Quantity</Label>
            <Input
              id="quantity"
              type="number"
              step="0.00000001"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              placeholder="0.001"
            />
          </div>

          {type === "limit" && (
            <div>
              <Label htmlFor="price">Price (USDT)</Label>
              <Input
                id="price"
                type="number"
                step="0.01"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                placeholder="50000"
              />
            </div>
          )}

          {error && (
            <div className="p-3 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-md text-sm">
              {error}
            </div>
          )}

          <Button
            type="submit"
            disabled={createOrder.isPending}
            className="w-full"
            variant={side === "buy" ? "default" : "destructive"}
          >
            {createOrder.isPending ? "Placing..." : `${side.toUpperCase()} ${symbol}`}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
