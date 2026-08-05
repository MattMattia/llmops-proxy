from prometheus_client import Counter

# Contador de intentos maliciosos bloqueados por el Guardrail
SECURITY_BLOCKED_COUNTER = Counter(
    "llmops_security_blocked_total",
    "Total de prompts bloqueados por intentos de inyección o políticas de seguridad"
)

# Contador de veces que el filtro DLP censuró PII
DLP_MASKED_COUNTER = Counter(
    "llmops_dlp_masked_total",
    "Total de veces que el filtro DLP detectó y enmascaró datos sensibles"
)