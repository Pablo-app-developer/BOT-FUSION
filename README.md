# Bot Trading FUSION

## Descripción
Bot de trading automático para el par EUR/USD basado en estrategias Smart Money Concepts (SMC) y Liquidity & Institutional Trading (LIT). El bot analiza datos históricos, identifica patrones SMC+LIT y ejecuta operaciones en MetaTrader 5.

## Características principales
- Identificación de Order Blocks (OB) alcistas y bajistas
- Detección de Fair Value Gaps (FVG)
- Análisis de niveles de liquidez y Change of Character (CHoCH)
- Gestión adaptativa de riesgo basada en volatilidad
- Generación de señales con sistema de puntuación por confluencia
- Integración completa con MetaTrader 5

## Estructura del proyecto
```
├── data/            # Datos históricos y resultados
├── models/          # Modelos entrenados
├── src/             # Código fuente
│   ├── bot_trading.py         # Clase principal del bot
│   ├── smc_analyzer.py        # Análisis de Smart Money Concepts
│   ├── range_detector.py      # Detector de rangos y CHoCH
│   ├── signal_generator.py    # Generador de señales
│   ├── risk_manager.py        # Gestor de riesgo adaptativo
│   ├── config.py              # Configuración del bot
│   └── mt5_credentials.py     # Credenciales de MetaTrader 5
├── news/           # Análisis de noticias económicas
└── tests/          # Pruebas unitarias
```

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Pablo-app-developer/BOT-FUSION.git
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar credenciales:
   - Crear archivo `mt5_credentials.py` basado en la plantilla proporcionada
   - Agregar credenciales de MetaTrader 5

## Uso

1. Ejecutar el bot:
```bash
python src/bot_trading.py
```

2. Monitorear operaciones:
   - El bot imprimirá información sobre análisis y operaciones en la consola
   - Las operaciones se ejecutarán automáticamente en MetaTrader 5

## Estrategia SMC+LIT

El bot utiliza una combinación de estrategias Smart Money Concepts (SMC) y Liquidity & Institutional Trading (LIT):

1. **Order Blocks (OB)**: Identifica bloques de órdenes institucionales que pueden actuar como soporte/resistencia.

2. **Fair Value Gaps (FVG)**: Detecta gaps en el precio que tienden a rellenarse.

3. **Change of Character (CHoCH)**: Identifica cambios en la estructura del mercado que indican posibles reversiones.

4. **Niveles de liquidez**: Analiza zonas donde se acumula liquidez para posibles cazas de stops.

5. **Sistema de confluencia**: Genera señales solo cuando múltiples factores coinciden, aumentando la probabilidad de éxito.

## Gestión de riesgo

El bot implementa una gestión de riesgo adaptativa que:

- Limita el riesgo por operación a un porcentaje del balance
- Ajusta el tamaño de posición según la volatilidad del mercado
- Implementa un límite de drawdown diario
- Calcula automáticamente niveles de stop loss y take profit

## Requisitos

- Python 3.8+
- MetaTrader 5
- Cuenta de trading (demo o real)
- Dependencias listadas en requirements.txt

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios importantes antes de enviar un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
