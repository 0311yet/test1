"use client";

import { useState, useEffect } from "react";
import { LogEntry } from "@/types";
import { Card, CardContent } from "@/components/ui/card";

interface LogPanelProps {
  logs?: LogEntry[];
  refreshInterval?: number;
}

export function LogPanel({ logs: initialLogs, refreshInterval = 10000 }: LogPanelProps) {
  const [logs, setLogs] = useState<LogEntry[]>(initialLogs || []);
  const [filterLevel, setFilterLevel] = useState<string>("all");

  useEffect(() => {
    if (refreshInterval > 0 && !initialLogs) {
      const interval = setInterval(() => {
        // In a real app, fetch logs from API
        setLogs(prev => prev.slice(-100));
      }, refreshInterval);

      return () => clearInterval(interval);
    }
  }, [refreshInterval, initialLogs]);

  const filteredLogs = filterLevel === "all"
    ? logs
    : logs.filter(log => log.level === filterLevel);

  const getLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'info':
        return 'bg-blue-100 text-blue-800';
      case 'warning':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      case 'success':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

   return (
     <Card>
       <CardContent className="p-6">
         <div className="flex items-center justify-between mb-4">
           <h3 className="text-lg font-semibold">System Logs</h3>
           <div className="flex gap-2">
             {['all', 'info', 'warning', 'error', 'success'].map((level: string) => (
               <button
                 key={level}
                 onClick={() => setFilterLevel(level)}
                 className={`px-3 py-1 rounded text-sm font-medium ${
                   filterLevel === level
                     ? 'bg-gray-900 text-white'
                     : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                 }`}
               >
                 {level}
               </button>
             ))}
           </div>
         </div>

         <div className="space-y-2 max-h-96 overflow-y-auto">
           {filteredLogs.length > 0 ? (
             filteredLogs.map((log: LogEntry, index: number) => (
               <div
                 key={index}
                 className="flex items-start gap-3 p-2 hover:bg-gray-50 dark:hover:bg-gray-700 rounded"
               >
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${getLevelColor(log.level)}`}>
                  {log.level.toUpperCase()}
                </span>
                <span className="text-sm text-gray-600 dark:text-gray-400 flex-1">
                  {log.message}
                </span>
                <span className="text-xs text-gray-400 whitespace-nowrap">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))
          ) : (
            <div className="text-center text-gray-500 py-4">
              No logs available
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
