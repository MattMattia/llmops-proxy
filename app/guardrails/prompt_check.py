import re

# Lista de frases comunes usadas para "hackear" el comportamiento de la IA
FORBIDDEN_PATTERNS = [
    r"ignora (todas )?las instrucciones",
    r"olvida (todo )?lo anterior",
    r"system prompt",
    r"eres (ahora )?un desarrollador sin restricciones",
    r"modo dan"
]

def is_safe_prompt(prompt: str) -> tuple[bool, str]:
    """
    Evalúa el texto del usuario. 
    Retorna un booleano (True si es seguro) y un mensaje descriptivo.
    """
    prompt_lower = prompt.lower()
    
    for pattern in FORBIDDEN_PATTERNS:
        # Si encuentra alguna coincidencia con la lista negra
        if re.search(pattern, prompt_lower):
            return False, f"Patrón bloqueado: {pattern}"
            
    return True, "Seguro"