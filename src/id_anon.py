import re
from .chat_message import ChatMessage

_user_map = {}
_sender_map = {}

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

def anonymize_sender_id(sender: str) -> str:
    """
    Substitui nomes de senders por user_N de forma consistente
    """
    if sender not in _sender_map:
        _sender_map[sender] = f'user_{len(_sender_map) + 1}'
    return _sender_map[sender]

def anonymize_chat_message_id(msg: ChatMessage) -> ChatMessage:
    """Anonimiza uma mensagem estruturada substituindo IDs"""
    # Anonimiza o sender
    anonymized_sender = anonymize_sender_id(msg.sender)
    
    # Anonimiza menções no conteúdo da mensagem
    anonymized_message = anonymize_message_id(msg.message)
    
    return ChatMessage(
        timestamp=msg.timestamp,  # Mantém timestamp original
        sender=anonymized_sender,
        message=anonymized_message,
        original_sender=msg.original_sender if hasattr(msg, 'original_sender') else msg.sender,
        original_message=msg.original_message if hasattr(msg, 'original_message') else msg.message
    )

def anonymize_messages_id(messages: list) -> list:
    """Anonimiza uma lista de mensagens (ChatMessage ou strings)"""
    result = []
    
    for msg in messages:
        if isinstance(msg, ChatMessage):
            result.append(anonymize_chat_message_id(msg))
        elif isinstance(msg, str):
            # Para compatibilidade com código legado
            result.append(anonymize_message_id(msg))
        else:
            result.append(msg)
    
    return result

def reset_mappings():
    """Reset dos mapeamentos para novo processamento"""
    global _user_map, _sender_map
    _user_map = {}
    _sender_map = {}