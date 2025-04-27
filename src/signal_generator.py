"""
Generador de señales basado en SMC+LIT
"""

import numpy as np
from config import MIN_CONFLUENCE_SCORE

class SignalGenerator:
    def __init__(self):
        self.min_confluence_score = MIN_CONFLUENCE_SCORE
        
    def generate_signals(self, order_blocks, fvgs, liquidity, current_price, atr):
        """
        Genera señales de trading basadas en la confluencia de SMC+LIT
        
        Args:
            order_blocks (dict): Información de Order Blocks
            fvgs (list): Fair Value Gaps identificados
            liquidity (dict): Niveles de liquidez
            current_price (float): Precio actual
            atr (float): ATR actual
            
        Returns:
            dict: Señales generadas con puntuación de confluencia
        """
        signals = {
            'buy_signals': [],
            'sell_signals': []
        }
        
        # Analizar Order Blocks
        bullish_obs = order_blocks['order_blocks']['bullish_obs']
        bearish_obs = order_blocks['order_blocks']['bearish_obs']
        
        # Analizar FVGs
        bullish_fvgs = [fvg for fvg in fvgs if fvg['type'] == 'bullish']
        bearish_fvgs = [fvg for fvg in fvgs if fvg['type'] == 'bearish']
        
        # Analizar niveles de liquidez
        choch_points = liquidity['choch_points']
        range_info = liquidity['range_info']
        
        # Generar señales de compra
        for ob in bullish_obs:
            # Verificar si el precio está cerca del OB alcista
            if abs(current_price - ob['low']) < atr * 0.5:
                # Iniciar evaluación de confluencia
                confluence_score = 1  # Comienza con 1 por el OB
                entry_price = ob['low']
                stop_loss = ob['low'] - atr * 1.5  # SL debajo del OB
                take_profit = current_price + (current_price - stop_loss) * 2  # RR 1:2
                
                # Verificar confluencia con FVGs alcistas
                for fvg in bullish_fvgs:
                    if abs(ob['low'] - fvg['bottom']) < atr * 0.7:
                        confluence_score += 1
                        break
                
                # Verificar confluencia con CHoCH de compra
                for choch in choch_points['buy_choch']:
                    if abs(ob['low'] - choch['price']) < atr * 0.7:
                        confluence_score += 1
                        # Ajustar SL al nivel del CHoCH
                        stop_loss = choch['price'] - atr * 0.5
                        break
                
                # Verificar si estamos en un rango de acumulación
                if order_blocks['range_info']['is_range'] and order_blocks['range_info']['type'] == 'accumulation':
                    confluence_score += 1
                
                # Si la puntuación de confluencia es suficiente, generar señal
                if confluence_score >= self.min_confluence_score:
                    signals['buy_signals'].append({
                        'entry_price': entry_price,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'confluence_score': confluence_score,
                        'reason': f'OB alcista + {confluence_score-1} factores adicionales'
                    })
        
        # Generar señales de venta
        for ob in bearish_obs:
            # Verificar si el precio está cerca del OB bajista
            if abs(current_price - ob['high']) < atr * 0.5:
                # Iniciar evaluación de confluencia
                confluence_score = 1  # Comienza con 1 por el OB
                entry_price = ob['high']
                stop_loss = ob['high'] + atr * 1.5  # SL encima del OB
                take_profit = current_price - (stop_loss - current_price) * 2  # RR 1:2
                
                # Verificar confluencia con FVGs bajistas
                for fvg in bearish_fvgs:
                    if abs(ob['high'] - fvg['top']) < atr * 0.7:
                        confluence_score += 1
                        break
                
                # Verificar confluencia con CHoCH de venta
                for choch in choch_points['sell_choch']:
                    if abs(ob['high'] - choch['price']) < atr * 0.7:
                        confluence_score += 1
                        # Ajustar SL al nivel del CHoCH
                        stop_loss = choch['price'] + atr * 0.5
                        break
                
                # Verificar si estamos en un rango de distribución
                if order_blocks['range_info']['is_range'] and order_blocks['range_info']['type'] == 'distribution':
                    confluence_score += 1
                
                # Si la puntuación de confluencia es suficiente, generar señal
                if confluence_score >= self.min_confluence_score:
                    signals['sell_signals'].append({
                        'entry_price': entry_price,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'confluence_score': confluence_score,
                        'reason': f'OB bajista + {confluence_score-1} factores adicionales'
                    })
        
        return signals