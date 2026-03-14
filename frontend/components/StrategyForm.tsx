"use client";

import { useState } from "react";
import { useCreateStrategy, useToggleStrategy } from "@/lib/hooks";
import { StrategyRequest } from "@/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function StrategyForm() {
  const [name, setName] = useState("price_trigger_strategy");
  const [type, setType] = useState<"price_trigger">("price_trigger");
  const [symbol, setSymbol] = useState("BTC/USDT");
  const [triggerPrice, setTriggerPrice] = useState("");
  const [action, setAction] = useState<"buy" | "sell">("buy");
  const [quantity, setQuantity] = useState("");
  const [stopLoss, setStopLoss] = useState("");
  const [takeProfit, setTakeProfit] = useState("");
  const createStrategy = useCreateStrategy();
  const toggleStrategy = useToggleStrategy();
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const qty = parseFloat(quantity);
    if (qty <= 0) {
      setError("Quantity must be greater than 0");
      return;
    }

    const config: StrategyRequest["config"] = {
      trigger_price: parseFloat(triggerPrice),
      action,
      quantity: qty,
    };

    if (stopLoss) config.stop_loss = parseFloat(stopLoss);
    if (takeProfit) config.take_profit = parseFloat(takeProfit);

    const strategyData: StrategyRequest = {
      name,
      type,
      symbol,
      config,
      is_active: false,
    };

    try {
      await createStrategy.mutateAsync(strategyData);
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create Strategy</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="name">Strategy Name</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="price_trigger_strategy"
            />
          </div>

          <div>
            <Label htmlFor="type">Strategy Type</Label>
            <div className="flex gap-2">
              <Button
                type="button"
                variant={type === "price_trigger" ? "default" : "outline"}
                onClick={() => setType("price_trigger")}
                className="flex-1"
              >
                Price Trigger
              </Button>
            </div>
          </div>

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
            <Label htmlFor="triggerPrice">Trigger Price</Label>
            <Input
              id="triggerPrice"
              type="number"
              step="0.01"
              value={triggerPrice}
              onChange={(e) => setTriggerPrice(e.target.value)}
              placeholder="50000"
            />
          </div>

          <div>
            <Label htmlFor="action">Action</Label>
            <div className="flex gap-2">
              <Button
                type="button"
                variant={action === "buy" ? "default" : "outline"}
                onClick={() => setAction("buy")}
                className="flex-1"
              >
                Buy
              </Button>
              <Button
                type="button"
                variant={action === "sell" ? "default" : "outline"}
                onClick={() => setAction("sell")}
                className="flex-1"
              >
                Sell
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

          <div>
            <Label htmlFor="stopLoss">Stop Loss (optional)</Label>
            <Input
              id="stopLoss"
              type="number"
              step="0.01"
              value={stopLoss}
              onChange={(e) => setStopLoss(e.target.value)}
              placeholder="49500"
            />
          </div>

          <div>
            <Label htmlFor="takeProfit">Take Profit (optional)</Label>
            <Input
              id="takeProfit"
              type="number"
              step="0.01"
              value={takeProfit}
              onChange={(e) => setTakeProfit(e.target.value)}
              placeholder="50500"
            />
          </div>

          {error && (
            <div className="p-3 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-md text-sm">
              {error}
            </div>
          )}

          <div className="flex gap-2">
            <Button
              type="submit"
              disabled={createStrategy.isPending}
              className="flex-1"
            >
              {createStrategy.isPending ? "Creating..." : "Create Strategy"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
