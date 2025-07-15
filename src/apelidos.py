import re
from typing import List

def anonimizar_apelidos(texto: str, apelidos: List[str]) -> str:
    for apelido in apelidos:
        texto = re.sub(rf"\b{re.escape(apelido)}\b", "PESSOA", texto, flags=re.IGNORECASE)
    return texto
