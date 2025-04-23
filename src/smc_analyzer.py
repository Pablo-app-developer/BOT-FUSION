"""
Analizador de Smart Money Concepts (SMC) y Liquidity & Institutional Trading (LIT)
"""

import numpy as np

class SMCAnalyzer:
    def __init__(self):
        self.range_threshold = 0.0015  # 15 pips para EUR/USD
        self.fvg_threshold = 0.0010   # 10 pips para gaps
        
    def identify_range(self, high_prices, low_prices, volume):
        """
        Identifica rangos de acumulación/distribución
        
        Args:
            high_prices (np.array): Precios máximos
            low_prices (np.array): Precios mínimos
            volume (np.array): Volumen de trading
            
        Returns:
            dict: Información del rango identificado
        """
        range_info = {
            'is_range': False,
            'type': None,  # 'accumulation' o 'distribution'
            'upper_bound': None,
            'lower_bound': None,
            'volume_profile': None
        }
        
        # Calcular rango de precios
        price_range = np.max(high_prices) - np.min(low_prices)
        
        if price_range <= self.range_threshold:
            range_info['is_range'] = True
            range_info['upper_bound'] = np.max(high_prices)
            range_info['lower_bound'] = np.min(low_prices)
            
            # Analizar perfil de volumen
            avg_volume = np.mean(volume)
            if np.mean(volume[-3:]) > avg_volume:
                range_info['type'] = 'accumulation'
            else:
                range_info['type'] = 'distribution'
                
            range_info['volume_profile'] = self._calculate_volume_profile(high_prices, low_prices, volume)
            
        return range_info
    
    def identify_order_blocks(self, open_prices, high_prices, low_prices, close_prices):
        """
        Identifica Order Blocks alcistas y bajistas
        
        Returns:
            dict: Order blocks identificados
        """
        ob_info = {
            'bullish_obs': [],
            'bearish_obs': []
        }
        
        # Identificar Order Blocks alcistas (últimas velas antes de un movimiento hacia arriba)
        for i in range(1, len(close_prices)-1):
            if close_prices[i+1] > high_prices[i] * 1.002:  # Movimiento alcista significativo
                ob_info['bullish_obs'].append({
                    'high': high_prices[i],
                    'low': low_prices[i],
                    'index': i
                })
                
        # Identificar Order Blocks bajistas
        for i in range(1, len(close_prices)-1):
            if close_prices[i+1] < low_prices[i] * 0.998:  # Movimiento bajista significativo
                ob_info['bearish_obs'].append({
                    'high': high_prices[i],
                    'low': low_prices[i],
                    'index': i
                })
                
        return ob_info
    
    def identify_fair_value_gaps(self, high_prices, low_prices):
        """
        Identifica Fair Value Gaps (FVG)
        
        Returns:
            list: FVGs identificados
        """
        fvgs = []
        
        for i in range(1, len(high_prices)-1):
            # FVG alcista
            if low_prices[i+1] > high_prices[i-1] + self.fvg_threshold:
                fvgs.append({
                    'type': 'bullish',
                    'top': low_prices[i+1],
                    'bottom': high_prices[i-1],
                    'index': i
                })
                
            # FVG bajista
            if high_prices[i+1] < low_prices[i-1] - self.fvg_threshold:
                fvgs.append({
                    'type': 'bearish',
                    'top': low_prices[i-1],
                    'bottom': high_prices[i+1],
                    'index': i
                })
                
        return fvgs
    
    def _calculate_volume_profile(self, high_prices, low_prices, volume):
        """
        Calcula el perfil de volumen en el rango
        """
        price_levels = np.linspace(np.min(low_prices), np.max(high_prices), 10)
        volume_profile = np.zeros_like(price_levels)
        
        for i in range(len(price_levels)-1):
            mask = (low_prices >= price_levels[i]) & (high_prices < price_levels[i+1])
            volume_profile[i] = np.sum(volume[mask])
            
        return {
            'price_levels': price_levels.tolist(),
            'volume_distribution': volume_profile.tolist()
        }