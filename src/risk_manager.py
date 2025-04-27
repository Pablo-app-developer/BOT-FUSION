"""
Gestor de riesgo adaptativo basado en rangos y volatilidad
"""

import numpy as np
from config import MAX_RISK_PER_TRADE, MAX_DAILY_DRAWDOWN

class RiskManager:
    def __init__(self):
        self.max_risk_per_trade = MAX_RISK_PER_TRADE
        self.max_daily_drawdown = MAX_DAILY_DRAWDOWN
        self.current_daily_drawdown = 0
        self.volatility_multiplier = 1.0
        
    def calculate_position_size(self, account_balance, entry_price, stop_loss, volatility_atr):
        """
        Calcula el tamaño de la posición basado en el riesgo y volatilidad
        
        Args:
            account_balance (float): Balance de la cuenta
            entry_price (float): Precio de entrada
            stop_loss (float): Nivel de stop loss
            volatility_atr (float): ATR actual del mercado
            
        Returns:
            float: Tamaño de la posición en lotes
        """
        # Ajustar riesgo basado en drawdown actual
        adjusted_risk = self._adjust_risk_by_drawdown()
        
        # Ajustar por volatilidad
        self._adjust_volatility_multiplier(volatility_atr)
        
        # Calcular riesgo monetario
        risk_amount = account_balance * adjusted_risk * self.volatility_multiplier
        
        # Calcular distancia al stop loss
        stop_distance = abs(entry_price - stop_loss)
        
        # Calcular tamaño de posición (para EUR/USD, 1 pip = 0.0001)
        pip_value = 10  # Valor aproximado de 1 pip en USD para 1 lote estándar
        position_size = risk_amount / (stop_distance * pip_value * 10000)
        
        return round(position_size, 2)  # Redondear a 2 decimales
    
    def _adjust_risk_by_drawdown(self):
        """
        Ajusta el riesgo basado en el drawdown actual
        """
        if self.current_daily_drawdown >= self.max_daily_drawdown:
            return 0  # No más trades por hoy
            
        drawdown_factor = 1 - (self.current_daily_drawdown / self.max_daily_drawdown)
        return self.max_risk_per_trade * drawdown_factor
    
    def _adjust_volatility_multiplier(self, current_atr):
        """
        Ajusta el multiplicador de volatilidad basado en ATR
        """
        # Reducir tamaño en mercados más volátiles
        if current_atr > 0.001:  # ATR > 10 pips
            self.volatility_multiplier = 0.8
        elif current_atr > 0.0005:  # ATR > 5 pips
            self.volatility_multiplier = 0.9
        else:
            self.volatility_multiplier = 1.0
            
    def update_daily_drawdown(self, pnl):
        """
        Actualiza el drawdown diario
        
        Args:
            pnl (float): Profit/Loss del último trade
        """
        if pnl < 0:
            self.current_daily_drawdown += abs(pnl)
            
    def reset_daily_metrics(self):
        """
        Reinicia las métricas diarias
        """
        self.current_daily_drawdown = 0
        self.volatility_multiplier = 1.0