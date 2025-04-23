"""
Detector de rangos basado en Change of Character (CHoCH) y Order Blocks
"""

import numpy as np

class RangeDetector:
    def __init__(self):
        self.min_range_size = 0.0005  # 5 pips mínimo
        self.max_range_size = 0.0050  # 50 pips máximo
        
    def detect_choch(self, high_prices, low_prices, close_prices):
        """
        Detecta Change of Character (CHoCH) en el precio
        
        Returns:
            dict: Puntos CHoCH identificados
        """
        choch_points = {
            'buy_choch': [],  # CHoCH de compra
            'sell_choch': []  # CHoCH de venta
        }
        
        # Detectar swing highs y lows
        for i in range(2, len(close_prices)-2):
            # CHoCH de compra (swing low seguido de higher low)
            if (low_prices[i] < low_prices[i-1] and 
                low_prices[i] < low_prices[i-2] and
                low_prices[i] < low_prices[i+1] and
                low_prices[i] < low_prices[i+2] and
                low_prices[i+1] > low_prices[i]):
                    
                choch_points['buy_choch'].append({
                    'price': low_prices[i],
                    'index': i,
                    'type': 'buy'
                })
                
            # CHoCH de venta (swing high seguido de lower high)
            if (high_prices[i] > high_prices[i-1] and
                high_prices[i] > high_prices[i-2] and
                high_prices[i] > high_prices[i+1] and
                high_prices[i] > high_prices[i+2] and
                high_prices[i+1] < high_prices[i]):
                    
                choch_points['sell_choch'].append({
                    'price': high_prices[i],
                    'index': i,
                    'type': 'sell'
                })
                
        return choch_points
    
    def validate_range(self, upper_bound, lower_bound):
        """
        Valida si el rango identificado cumple con los criterios de tamaño
        """
        range_size = upper_bound - lower_bound
        return self.min_range_size <= range_size <= self.max_range_size
    
    def identify_range_with_choch(self, high_prices, low_prices, close_prices):
        """
        Identifica rangos usando CHoCH y Order Blocks
        
        Returns:
            dict: Información del rango identificado
        """
        range_info = {
            'is_valid_range': False,
            'upper_bound': None,
            'lower_bound': None,
            'choch_points': None,
            'range_size': None
        }
        
        # Obtener puntos CHoCH
        choch_points = self.detect_choch(high_prices, low_prices, close_prices)
        
        # Verificar si tenemos suficientes puntos para formar un rango
        if choch_points['buy_choch'] and choch_points['sell_choch']:
            # Tomar el CHoCH de venta más reciente como límite superior
            upper_bound = choch_points['sell_choch'][-1]['price']
            
            # Tomar el CHoCH de compra más reciente como límite inferior
            lower_bound = choch_points['buy_choch'][-1]['price']
            
            # Validar el rango
            if self.validate_range(upper_bound, lower_bound):
                range_info['is_valid_range'] = True
                range_info['upper_bound'] = upper_bound
                range_info['lower_bound'] = lower_bound
                range_info['choch_points'] = choch_points
                range_info['range_size'] = upper_bound - lower_bound
                
        return range_info
