"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Balance } from "@/types";

interface BalanceCardProps {
  data?: Balance;
}

export function BalanceCard({ data }: BalanceCardProps) {
  const totalEquity = data?.total_equity ?? 0;
  const availableBalance = data?.available_balance ?? 0;
  const marginBalance = data?.margin_balance ?? 0;
  const unrealizedPnl = data?.unrealized_pnl ?? 0;

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Account Balance</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
              <p className="text-sm text-gray-600 dark:text-gray-400">Total Equity</p>
              <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                ${totalEquity.toFixed(2)}
              </p>
            </div>
            <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
              <p className="text-sm text-gray-600 dark:text-gray-400">Available</p>
              <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                ${availableBalance.toFixed(2)}
              </p>
            </div>
            <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
              <p className="text-sm text-gray-600 dark:text-gray-400">Margin Balance</p>
              <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                ${marginBalance.toFixed(2)}
              </p>
            </div>
            <div className="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg">
              <p className="text-sm text-gray-600 dark:text-gray-400">Unrealized PnL</p>
              <p className={`text-2xl font-bold ${
                unrealizedPnl >= 0 ? 'text-orange-600 dark:text-orange-400' : 'text-red-600 dark:text-red-400'
              }`}>
                ${unrealizedPnl.toFixed(2)}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
