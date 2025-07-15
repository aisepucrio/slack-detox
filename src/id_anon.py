import re

_user_map = {}

def anonymize_message_id(text: str) -> str:
    """
    Substitui todas as menções @nome por @user_N,
    mantendo consistência ao longo do arquivo.
    """
    pattern = r'@(\w+)'
    def repl(m):
        nome = m.group(1)
        if nome not in _user_map:
            _user_map[nome] = f'user_{len(_user_map) + 1}'
        return '@' + _user_map[nome]
    return re.sub(pattern, repl, text)