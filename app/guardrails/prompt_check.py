import re

# Lista de patrones prohibidos (ej. prompt injection, jailbreaks)
FORBIDDEN_PATTERNS = [
    r"ignora (todas )?las instrucciones",
    r"olvida (todo )?lo anterior",
    r"system prompt",
    r"eres (ahora )?un desarrollador sin restricciones",
    r"modo dan"
]

# OPTIMIZACIÓN: Pre-compilamos las expresiones regulares una sola vez al iniciar la app
COMPILED_PATTERNS = [
    (pattern, re.compile(pattern, re.IGNORECASE)) 
    for pattern in FORBIDDEN_PATTERNS
]

def is_safe_prompt(prompt: str) -> tuple[bool, str]:
    """
    Evalúa el texto del usuario utilizando patrones pre-compilados para mayor velocidad.
    Retorna un booleano (True si es seguro) y un mensaje descriptivo.
    """
    # Si el prompt está vacío o no es string, lo tratamos con precaución
    if not prompt or not isinstance(prompt, str):
        return False, "Prompt inválido o vacío."

    # Iteramos sobre los patrones ya compilados (evita compilar en caliente)
    for raw_pattern, compiled_regex in COMPILED_PATTERNS:
        if compiled_regex.search(prompt):
            return False, f"Patrón bloqueado: {raw_pattern}"
            
    return True, "Seguro"