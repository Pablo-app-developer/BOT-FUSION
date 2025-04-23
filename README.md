# Bot Trading FUSION

Bot de trading automático para EUR/USD que implementa estrategias SMC (Smart Money Concepts) y análisis técnico avanzado.

## Características

- Análisis técnico avanzado
- Integración con MetaTrader 5
- Estrategias SMC implementadas
- Gestión de riesgos automatizada
- Procesamiento de señales en tiempo real

## Estructura del Proyecto

```
├── src/
│   ├── bot_trading.py       # Clase principal del bot
│   ├── technical_analysis.py # Análisis técnico
│   ├── signal_generator.py   # Generador de señales
│   ├── risk_manager.py      # Gestión de riesgos
│   └── config.py            # Configuraciones generales
```

## Requisitos

- Python 3.8+
- MetaTrader 5
- Dependencias listadas en requirements.txt

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

1. Configurar parámetros en `config.py`
2. Ejecutar el bot:
```bash
python src/bot_trading.py
```

## Seguridad

- Las credenciales de MT5 se manejan de forma segura
- Archivo .gitignore configurado para proteger datos sensibles
- Implementación de manejo de errores robusto

## Contribución

Si deseas contribuir al proyecto:

1. Haz un Fork del repositorio
2. Crea una rama para tu feature
3. Envía un Pull Request

## Licencia

MIT License