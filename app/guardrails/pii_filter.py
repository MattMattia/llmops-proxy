import re

def mask_sensitive_data(text: str) -> str:
    """
    Busca y censura información sensible en el texto antes de enviarlo a la IA.
    """
    # 1. Censurar correos electrónicos
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    text_masked = re.sub(email_pattern, "[EMAIL_PROTEGIDO]", text)
    
    # 2. Censurar posibles números de tarjeta de crédito o teléfonos (simplificado)
    # Busca patrones de 13 a 16 números juntos o separados por guiones
    phone_cc_pattern = r'\b(?:\d[ -]*?){13,16}\b'
    text_masked = re.sub(phone_cc_pattern, "[NUMERO_PROTEGIDO]", text_masked)
    
    return text_masked