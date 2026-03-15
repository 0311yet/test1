"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Balance } from "@/types";

interface BalanceCardProps {
  data?: Balance;
}

export function BalanceCard({ data }: BalanceCardProps) {
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
                ${data?.total_equity?.toFixed(2) || '0.00'}
              </p>
            </div>
            <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
              <p className="text-sm text-gray-600 dark:text-gray-400">Available</p>
              <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                ${data?.available_balance?.toFixed(2) || '0.00'}
              </p>
            </div>
            <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
              <p className="text-sm text-gray-600 dark:text-gray-400">Margin Balance</p>
              <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                ${data?.margin_balance?.toFixed(2) || '0.00'}
              </p>
            </div>
            <div className="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg">
              <p className="text-sm text-gray-600 dark:text-gray-400">Unrealized PnL</p>
              <p className={`text-2xl font-bold ${
                data?.unrealized_pnl >= 0 ? 'text-orange-600 dark:text-orange-400' : 'text-red-600 dark:text-red-400'
              }`}>
                ${data?.unrealized_pnl?.toFixed(2) || '0.00'}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
