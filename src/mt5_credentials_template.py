"""
Plantilla para configurar credenciales de MetaTrader 5
Renombrar este archivo a mt5_credentials.py y completar con tus datos
"""

def get_credentials():
    """
    Retorna las credenciales para conectarse a MetaTrader 5
    
    Returns:
        dict: Credenciales de conexión
    """
    return {
        'server': 'TuServidorAquí',  # Ejemplo: 'MetaQuotes-Demo'
        'login': 12345678,  # Tu número de cuenta
        'password': 'TuContraseñaAquí',
        'timeout': 60000  # Timeout en milisegundos
    }
