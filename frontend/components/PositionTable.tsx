"use client";

import { usePositions } from "@/lib/hooks";
import { Position } from "@/types";
import { Card, CardContent } from "@/components/ui/card";

export function PositionTable() {
  const { data: positions, isLoading, error } = usePositions();

  if (isLoading) {
    return (
      <Card>
        <CardContent className="py-8">
          <div className="text-center text-gray-500">Loading positions...</div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent className="py-8">
          <div className="text-center text-red-500">Error loading positions</div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent className="p-6">
        <div className="space-y-4">
          {positions && positions.length > 0 ? (
            positions.map((position: Position) => {
              const quantity = position.quantity ?? 0;
              const avgPrice = position.avg_price ?? 0;
              const markPrice = position.mark_price ?? 0;
              const unrealizedPnl = position.unrealized_pnl ?? 0;

              return (
                <div
                  key={position.id}
                  className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <span className={`font-semibold ${
                        position.side === "long" ? "text-blue-600 dark:text-blue-400" : "text-red-600 dark:text-red-400"
                      }`}>
                        {position.side.toUpperCase()}
                      </span>
                      <span className="font-medium">{position.symbol}</span>
                    </div>
                    <div className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                      Size: {quantity} {position.symbol.split('/')[0]} @ {avgPrice.toFixed(2)}
                    </div>
                    <div className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                      Mark Price: ${markPrice.toFixed(2)}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-lg font-bold ${
                      unrealizedPnl >= 0 ? "text-green-600" : "text-red-600"
                    }`}>
                      ${unrealizedPnl.toFixed(2)}
                    </div>
                    <div className="text-xs text-gray-500">
                      {unrealizedPnl >= 0 ? "+" : ""}
                      {((unrealizedPnl / (quantity * avgPrice)) * 100).toFixed(2)}%
                    </div>
                  </div>
                </div>
              );
            })
          ) : (
            <div className="text-center text-gray-500 py-8">
              No open positions
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
