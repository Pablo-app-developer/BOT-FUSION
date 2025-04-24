"""
Archivo de configuración para el bot de trading
"""

# Configuración de riesgo
MAX_RISK_PER_TRADE = 0.02  # 2% máximo por operación
MAX_DAILY_DRAWDOWN = 0.05  # 5% máximo de drawdown diario

# Configuración de trading
DEFAULT_TIMEFRAME = 'H1'  # Timeframe por defecto
DEFAULT_SYMBOL = 'EURUSD'  # Par por defecto

# Configuración de análisis técnico
ATR_PERIOD = 14  # Período para ATR
OB_LOOKBACK = 20  # Períodos para buscar Order Blocks
FVG_MIN_SIZE = 0.0010  # Tamaño mínimo para FVG (10 pips)

# Configuración de señales
MIN_CONFLUENCE_SCORE = 3  # Puntuación mínima de confluencia para entrar

# Configuración de sesiones
SESSION_TIMES = {
    'london_open': '08:00',
    'london_close': '16:30',
    'ny_open': '13:30',
    'ny_close': '22:00',
    'tokyo_open': '00:00',
    'tokyo_close': '08:00'
}

# Configuración de logging
LOG_LEVEL = 'INFO'  # Nivel de logging
LOG_FILE = 'bot_trading.log'  # Archivo de log