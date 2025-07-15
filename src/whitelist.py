import re
from typing import List, Dict, Tuple

def protect_whitelist_words(text: str, whitelist: List[str]) -> Tuple[str, Dict[str, str]]:
    """
    Protege palavras da whitelist substituindo-as por placeholders únicos
    Retorna o texto protegido e um dicionário de mapeamentos
    """
    if not whitelist:
        return text, {}
    
    placeholders = {}
    protected_text = text
    
    for i, word in enumerate(whitelist):
        # Criar placeholder único
        placeholder = f"__PROTECTED_WORD_{i}__"
        # Substituir a palavra (case-insensitive) pelo placeholder
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        matches = pattern.findall(protected_text)
        
        if matches:
            # Guardar o mapeamento original (mantém a capitalização original)
            for match in matches:
                if placeholder not in placeholders:
                    placeholders[placeholder] = match
                    break
            
            # Substituir no texto
            protected_text = pattern.sub(placeholder, protected_text)
    
    return protected_text, placeholders

def restore_whitelist_words(text: str, placeholders: Dict[str, str]) -> str:
    """
    Restaura as palavras protegidas substituindo os placeholders pelas palavras originais
    """
    restored_text = text
    for placeholder, original_word in placeholders.items():
        restored_text = restored_text.replace(placeholder, original_word)
    return restored_text

def load_whitelist_from_file(file_path: str) -> List[str]:
    """
    Carrega a whitelist de um arquivo de texto
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            whitelist = [line.strip() for line in f if line.strip()]
        return whitelist
    except FileNotFoundError:
        print(f"⚠️  Arquivo de whitelist não encontrado: {file_path}")
        return []
