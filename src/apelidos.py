import re
from typing import List
from .chat_message import ChatMessage

def anonimizar_apelidos(texto: str, apelidos: List[str]) -> str:
    """Anonimiza apelidos em um texto"""
    for apelido in apelidos:
        texto = re.sub(rf"\b{re.escape(apelido)}\b", "[PESSOA]", texto, flags=re.IGNORECASE)
    return texto

def anonimizar_apelidos_chat_message(msg: ChatMessage, apelidos: List[str]) -> ChatMessage:
    """Anonimiza apelidos em uma mensagem estruturada"""
    # Anonimiza apelidos no sender
    anonymized_sender = anonimizar_apelidos(msg.sender, apelidos)
    
    # Anonimiza apelidos no conteúdo da mensagem
    anonymized_message = anonimizar_apelidos(msg.message, apelidos)
    
    return ChatMessage(
        timestamp=msg.timestamp,
        sender=anonymized_sender,
        message=anonymized_message,
        original_sender=msg.original_sender if hasattr(msg, 'original_sender') else msg.sender,
        original_message=msg.original_message if hasattr(msg, 'original_message') else msg.message
    )

def anonimizar_apelidos_messages(messages: list, apelidos: List[str]) -> list:
    """Anonimiza apelidos em uma lista de mensagens"""
    result = []
    
    for msg in messages:
        if isinstance(msg, ChatMessage):
            result.append(anonimizar_apelidos_chat_message(msg, apelidos))
        elif isinstance(msg, str):
            # Para compatibilidade com código legado
            result.append(anonimizar_apelidos(msg, apelidos))
        else:
            result.append(msg)
    
    return result
