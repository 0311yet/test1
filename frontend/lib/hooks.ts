import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { OrderRequest, StrategyRequest } from '@/types';

export const queryKeys = {
  orders: ['orders'],
  positions: ['positions'],
  trades: ['trades'],
  strategies: ['strategies'],
  balance: ['balance'],
};

export const useOrders = () => {
  return useQuery({
    queryKey: queryKeys.orders,
    queryFn: () => api.get('/orders'),
  });
};

export const usePositions = () => {
  return useQuery({
    queryKey: queryKeys.positions,
    queryFn: () => api.get('/positions'),
  });
};

export const useTrades = () => {
  return useQuery({
    queryKey: queryKeys.trades,
    queryFn: () => api.get('/trades'),
  });
};

export const useStrategies = () => {
  return useQuery({
    queryKey: queryKeys.strategies,
    queryFn: () => api.get('/strategies'),
  });
};

export const useBalance = () => {
  return useQuery({
    queryKey: queryKeys.balance,
    queryFn: () => api.get('/balance'),
    refetchInterval: 5000,
  });
};

export const useCreateOrder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: OrderRequest) => api.post('/orders', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.orders });
      queryClient.invalidateQueries({ queryKey: queryKeys.positions });
    },
  });
};

export const useCancelOrder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (orderId: number) => api.delete(`/orders/${orderId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.orders });
    },
  });
};

export const useCreateStrategy = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: StrategyRequest) => api.post('/strategies', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.strategies });
    },
  });
};

export const useToggleStrategy = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (strategyId: number) =>
      api.put(`/strategies/${strategyId}/toggle`, {}),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.strategies });
    },
  });
};

export const useExecuteStrategy = () => {
  return useMutation({
    mutationFn: (strategyId: number) =>
      api.post(`/strategies/${strategyId}/execute`, {}),
  });
};

export const useCheckStrategies = () => {
  return useMutation({
    mutationFn: () => api.post('/strategies/check', {}),
  });
};
