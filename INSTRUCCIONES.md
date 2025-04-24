# Instrucciones para ejecutar el Bot Trading FUSION

## Problema detectado
Se identificó un error al intentar ejecutar el bot desde la carpeta `src` con el comando:
```
python src/bot_trading.py
```

Este error ocurre porque se está duplicando la ruta `src` en el comando, lo que resulta en que Python busque el archivo en `src/src/bot_trading.py` que no existe.

## Solución implementada
Se han creado dos scripts de ejecución que solucionan este problema:

1. **ejecutar_bot.py** - Para ejecución local en tu máquina
2. **run_bot.py** - Para ejecución en el repositorio GitHub

Estos scripts configuran correctamente las rutas de Python para que puedas ejecutar el bot desde cualquier ubicación.

## Cómo ejecutar el bot

### Opción 1: Usando el script de ejecución local
Este es el método recomendado para ejecutar el bot en tu máquina local:

```bash
python ejecutar_bot.py
```

### Opción 2: Ejecutando directamente desde la carpeta raíz
Si prefieres ejecutar el script original, hazlo desde la carpeta raíz del proyecto:

```bash
python -m src.bot_trading
```

### Opción 3: Ejecutando desde la carpeta src
Si estás dentro de la carpeta `src`, ejecuta:

```bash
python bot_trading.py
```

## Configuración previa
Antes de ejecutar el bot, asegúrate de:

1. Tener instaladas todas las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Crear el archivo `mt5_credentials.py` en la carpeta `src` basado en la plantilla proporcionada.

3. Tener MetaTrader 5 instalado y configurado en tu sistema.

## Solución de problemas comunes

- **Error de importación de módulos**: Asegúrate de ejecutar el bot usando uno de los métodos descritos anteriormente para evitar problemas de rutas de importación.

- **Error de conexión con MT5**: Verifica que MetaTrader 5 esté abierto y que las credenciales en `mt5_credentials.py` sean correctas.

- **Módulos no encontrados**: Ejecuta `pip install -r requirements.txt` para instalar todas las dependencias necesarias.
