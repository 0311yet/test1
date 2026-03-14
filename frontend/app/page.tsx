"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { OrderTable } from "@/components/OrderTable";
import { PositionTable } from "@/components/PositionTable";
import { BalanceCard } from "@/components/BalanceCard";
import { StrategyForm } from "@/components/StrategyForm";
import { LogPanel } from "@/components/LogPanel";
import { OrderForm } from "@/components/OrderForm";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("dashboard");

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col gap-6">
          <header className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Crypto Trading System
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-1">
                OKX Trading Platform MVP
              </p>
            </div>
            <div className="flex gap-2">
              <div className="flex items-center gap-2 px-4 py-2 bg-green-100 text-green-800 rounded-lg">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span className="text-sm font-medium">Connected</span>
              </div>
            </div>
          </header>

          <nav className="flex gap-1 bg-white dark:bg-gray-800 p-1 rounded-lg shadow-sm">
            {[
              { id: "dashboard", label: "Dashboard" },
              { id: "orders", label: "Orders" },
              { id: "positions", label: "Positions" },
              { id: "strategies", label: "Strategies" },
              { id: "logs", label: "Logs" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? "bg-gray-900 text-white"
                    : "text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>

          <main>
            {activeTab === "dashboard" && (
              <div className="grid gap-6 lg:grid-cols-3">
                <div className="lg:col-span-2">
                  <BalanceCard />
                </div>
                <div>
                  <OrderForm />
                </div>
              </div>
            )}

            {activeTab === "orders" && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                <OrderTable />
              </div>
            )}

            {activeTab === "positions" && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                <PositionTable />
              </div>
            )}

            {activeTab === "strategies" && (
              <div className="grid gap-6 lg:grid-cols-2">
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                  <StrategyForm />
                </div>
              </div>
            )}

            {activeTab === "logs" && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                <LogPanel />
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
