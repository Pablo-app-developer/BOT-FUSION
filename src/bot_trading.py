import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime
import time
import talib

# Importar módulos propios
from smc_analyzer import SMCAnalyzer
from range_detector import RangeDetector
from signal_generator import SignalGenerator
from risk_manager import RiskManager
from config import ATR_PERIOD

class BotTradingSMC:
    def __init__(self):
        # Configuración inicial
        self.symbol = "EURUSD"
        self.timeframe = mt5.TIMEFRAME_H1
        self.lot_size = 0.1
        self.stop_loss_pips = 50
        self.take_profit_pips = 100
        
        # Inicializar componentes
        self.signal_generator = SignalGenerator()
        self.risk_manager = RiskManager()
        
        # Obtener credenciales de MT5
        from mt5_credentials import get_credentials
        credentials = get_credentials()
        
        # Inicializar conexión con MT5
        if not mt5.initialize(
            server=credentials['server'],
            login=credentials['login'],
            password=credentials['password'],
            timeout=credentials['timeout']
        ):
            error = mt5.last_error()
            print(f"Error: Inicialización de MT5 fallida - Código: {error[0]}, Descripción: {error[1]}")
            mt5.shutdown()
            raise Exception(f"No se pudo conectar a MT5: {error[1]}")
        
        # Verificar si hay posiciones abiertas
        self.check_open_positions()
    
    def check_open_positions(self):
        """Verificar posiciones abiertas"""
        positions = mt5.positions_get(symbol=self.symbol)
        if positions is None:
            print("No se pudieron obtener posiciones")
            return []
        
        if len(positions) > 0:
            print(f"Posiciones abiertas: {len(positions)}")
            for position in positions:
                print(f"Ticket: {position.ticket}, Tipo: {'COMPRA' if position.type == 0 else 'VENTA'}, Volumen: {position.volume}")
        else:
            print("No hay posiciones abiertas")
        
        return positions
    
    def get_historical_data(self, num_candles=1000):
        """Obtener datos históricos del par"""
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, num_candles)
        if rates is None:
            return None
        
        # Convertir a DataFrame y calcular indicadores
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        # Calcular ATR
        df['atr'] = talib.ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=ATR_PERIOD)
        
        return df
    
    def identify_order_blocks(self, df):
        """Identificar bloques de órdenes usando SMC"""
        from smc_analyzer import SMCAnalyzer
        
        smc = SMCAnalyzer()
        high_prices = df['high'].values
        low_prices = df['low'].values
        close_prices = df['close'].values
        
        # Identificar Order Blocks
        ob_info = smc.identify_order_blocks(high_prices, low_prices, close_prices)
        
        # Identificar rangos de acumulación/distribución
        range_info = smc.identify_range(high_prices, low_prices, df['tick_volume'].values)
        
        return {
            'order_blocks': ob_info,
            'range_info': range_info
        }
    
    def detect_fair_value_gaps(self, df):
        """Detectar Fair Value Gaps usando SMC"""
        from smc_analyzer import SMCAnalyzer
        
        smc = SMCAnalyzer()
        high_prices = df['high'].values
        low_prices = df['low'].values
        
        # Identificar FVGs
        fvgs = smc.identify_fair_value_gaps(high_prices, low_prices)
        
        return fvgs
    
    def analyze_liquidity_levels(self, df):
        """Analizar niveles de liquidez usando LIT"""
        from range_detector import RangeDetector
        
        detector = RangeDetector()
        high_prices = df['high'].values
        low_prices = df['low'].values
        close_prices = df['close'].values
        
        # Identificar CHoCH y rangos
        choch_points = detector.detect_choch(high_prices, low_prices, close_prices)
        range_info = detector.identify_range_with_choch(high_prices, low_prices, close_prices)
        
        return {
            'choch_points': choch_points,
            'range_info': range_info
        }
    
    def execute_trade(self, order_type, price, sl, tp, lot_size=None):
        """
        Ejecutar operación de trading
        
        Args:
            order_type (str): Tipo de orden ('BUY' o 'SELL')
            price (float): Precio de entrada
            sl (float): Nivel de stop loss
            tp (float): Nivel de take profit
            lot_size (float, optional): Tamaño de lote. Si es None, usa el tamaño predeterminado.
            
        Returns:
            dict: Resultado de la operación
        """
        # Validar parámetros
        if order_type not in ["BUY", "SELL"]:
            print(f"Error: Tipo de orden inválido: {order_type}")
            return None
        
        # Usar tamaño de lote predeterminado si no se especifica
        if lot_size is None:
            lot_size = self.lot_size
        
        # Obtener información de la cuenta
        account_info = mt5.account_info()
        if account_info is None:
            print("Error: No se pudo obtener información de la cuenta")
            return None
        
        # Validar que hay suficiente margen
        if account_info.margin_free < account_info.balance * 0.1:
            print("Advertencia: Margen libre insuficiente, operación cancelada")
            return None
        
        # Configurar la solicitud de trading
        if order_type == "BUY":
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": lot_size,
                "type": mt5.ORDER_TYPE_BUY,
                "price": price,
                "sl": sl,
                "tp": tp,
                "deviation": 20,
                "magic": 234000,
                "comment": "python SMC+LIT buy",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
        else:  # SELL
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": lot_size,
                "type": mt5.ORDER_TYPE_SELL,
                "price": price,
                "sl": sl,
                "tp": tp,
                "deviation": 20,
                "magic": 234000,
                "comment": "python SMC+LIT sell",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
        
        # Enviar la orden
        result = mt5.order_send(request)
        
        # Verificar resultado
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Error al ejecutar orden: {result.retcode}, {result.comment}")
            return None
        
        print(f"Orden ejecutada: {order_type}, Precio: {price}, SL: {sl}, TP: {tp}, Lote: {lot_size}")
        return result
    
    def run(self):
        """Ejecutar el bot"""
        print("Iniciando bot de trading SMC+LIT...")
        max_retries = 5
        retry_count = 0
        
        while True:
            try:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Obteniendo datos...")
                # Obtener datos actuales
                df = self.get_historical_data()
                if df is None:
                    retry_count += 1
                    print(f"Advertencia: No se obtuvieron datos, reintentando... (Intento {retry_count}/{max_retries})")
                    if retry_count >= max_retries:
                        print("Error: Máximo de reintentos alcanzado. Reiniciando conexión...")
                        mt5.shutdown()
                        time.sleep(60)
                        self.__init__()
                        retry_count = 0
                        continue
                    time.sleep(10)
                    continue
                
                # Resetear contador de reintentos si la operación fue exitosa
                retry_count = 0
                
                # Verificar posiciones abiertas
                open_positions = self.check_open_positions()
                
                # Análisis técnico
                try:
                    # Obtener precio actual
                    current_price = df['close'].iloc[-1]
                    current_atr = df['atr'].iloc[-1]
                    
                    # Realizar análisis SMC+LIT
                    order_blocks = self.identify_order_blocks(df)
                    fvgs = self.detect_fair_value_gaps(df)
                    liquidity = self.analyze_liquidity_levels(df)
                    
                    # Generar señales
                    signals = self.signal_generator.generate_signals(
                        order_blocks, fvgs, liquidity, current_price, current_atr
                    )
                    
                    # Procesar señales
                    if signals['buy_signals'] or signals['sell_signals']:
                        print(f"Señales generadas: {len(signals['buy_signals'])} compra, {len(signals['sell_signals'])} venta")
                        
                        # Obtener información de la cuenta
                        account_info = mt5.account_info()
                        if account_info is None:
                            print("Error: No se pudo obtener información de la cuenta")
                            time.sleep(60)
                            continue
                        
                        # Procesar señales de compra
                        for signal in signals['buy_signals']:
                            # Verificar si ya tenemos posiciones abiertas
                            if len(open_positions) > 0:
                                print("Ya hay posiciones abiertas, omitiendo señal de compra")
                                continue
                            
                            # Calcular tamaño de posición basado en gestión de riesgo
                            lot_size = self.risk_manager.calculate_position_size(
                                account_info.balance,
                                signal['entry_price'],
                                signal['stop_loss'],
                                current_atr
                            )
                            
                            # Ejecutar operación
                            print(f"Ejecutando señal de COMPRA: {signal['reason']}")
                            result = self.execute_trade(
                                "BUY",
                                signal['entry_price'],
                                signal['stop_loss'],
                                signal['take_profit'],
                                lot_size
                            )
                            
                            # Solo ejecutar una operación a la vez
                            if result is not None:
                                break
                        
                        # Procesar señales de venta
                        for signal in signals['sell_signals']:
                            # Verificar si ya tenemos posiciones abiertas
                            if len(open_positions) > 0:
                                print("Ya hay posiciones abiertas, omitiendo señal de venta")
                                continue
                            
                            # Calcular tamaño de posición basado en gestión de riesgo
                            lot_size = self.risk_manager.calculate_position_size(
                                account_info.balance,
                                signal['entry_price'],
                                signal['stop_loss'],
                                current_atr
                            )
                            
                            # Ejecutar operación
                            print(f"Ejecutando señal de VENTA: {signal['reason']}")
                            result = self.execute_trade(
                                "SELL",
                                signal['entry_price'],
                                signal['stop_loss'],
                                signal['take_profit'],
                                lot_size
                            )
                            
                            # Solo ejecutar una operación a la vez
                            if result is not None:
                                break
                    else:
                        print("No se generaron señales en este ciclo")
                    
                except Exception as e:
                    print(f"Error en análisis técnico: {e}")
                    time.sleep(30)
                    continue
                
                # Esperar antes del siguiente análisis
                print(f"Esperando para el próximo ciclo de análisis...")
                time.sleep(60)  # Esperar 1 minuto antes del siguiente análisis
                
            except mt5.MT5Error as e:
                print(f"Error de MT5: {e}. Reiniciando conexión...")
                mt5.shutdown()
                time.sleep(60)
                self.__init__()
            except KeyboardInterrupt:
                print("Deteniendo bot por interrupción del usuario...")
                mt5.shutdown()
                break
            except Exception as e:
                print(f"Error inesperado: {e}")
                time.sleep(30)

if __name__ == "__main__":
    bot = BotTradingSMC()
    bot.run()