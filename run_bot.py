#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para ejecutar el bot de trading desde cualquier ubicación
"""
import os
import sys

# Obtener la ruta absoluta del directorio actual
base_dir = os.path.dirname(os.path.abspath(__file__))

# Añadir la carpeta src al path para poder importar módulos
src_dir = os.path.join(base_dir, 'src')
sys.path.append(src_dir)

# Importar y ejecutar el bot
from src.bot_trading import BotTradingSMC

if __name__ == "__main__":
    print("Iniciando Bot Trading FUSION desde script principal...\n")
    try:
        # Crear instancia del bot y ejecutar
        bot = BotTradingSMC()
        bot.run()
    except KeyboardInterrupt:
        print("\nBot detenido por el usuario.")
    except Exception as e:
        print(f"\nError al iniciar el bot: {e}")
