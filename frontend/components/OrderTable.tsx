"use client";

import { useOrders } from "@/lib/hooks";
import { Order } from "@/types";
import { Card, CardContent } from "@/components/ui/card";

export function OrderTable() {
  const { data: orders, isLoading, error } = useOrders();

  if (isLoading) {
    return (
      <Card>
        <CardContent className="py-8">
          <div className="text-center text-gray-500">Loading orders...</div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent className="py-8">
          <div className="text-center text-red-500">Error loading orders</div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent className="p-6">
        <div className="space-y-4">
          {orders && orders.length > 0 ? (
            orders.map((order) => (
              <div
                key={order.id}
                className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <span className={`font-semibold ${
                      order.side === "buy" ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"
                    }`}>
                      {order.side.toUpperCase()}
                    </span>
                    <span className="font-medium">{order.symbol}</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                      order.status === "active" ? "bg-blue-100 text-blue-800" : 
                      order.status === "filled" ? "bg-green-100 text-green-800" :
                      order.status === "cancelled" ? "bg-red-100 text-red-800" : 
                      "bg-gray-100 text-gray-800"
                    }`}>
                      {order.status}
                    </span>
                  </div>
                  <div className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                    {order.type.toUpperCase()} • {order.quantity} {order.symbol.split('/')[0]}
                  </div>
                  {order.price && (
                    <div className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                      Price: ${order.price.toFixed(2)}
                    </div>
                  )}
                  <div className="mt-1 text-sm text-gray-500">
                    {new Date(order.created_at).toLocaleString()}
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center text-gray-500 py-8">
              No orders yet
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
