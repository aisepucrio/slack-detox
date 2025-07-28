import re
from .chat_message import ChatMessage

patterns = {
    "CPF": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-.]+",
    "telefone": r"@?(?:\+?55)?\d{10,11}\b",
    "endereco": r"\b(rua|av\.?|avenida|travessa|estrada)\s+[^\d\n,]+[\d,]{0,10}",
    "chave_api": r"(?<!\S)[A-Za-z0-9_=-]{20,}(?!\S)",
    "codigo": (
        r"(?ms)"
        r"(?:```(?:\w+\n)?[\s\S]+?```"
        r"|`[^`\n]+?`"
        r"|^(?:[ \t]{4}[^\n]+\n?)+)"
    ),
}

def anonymize_message_content(message_content: str) -> str:
    """Anonimiza apenas o conteúdo da mensagem usando regex"""
    anonymized = message_content

    for label, pattern in patterns.items():
        matches = re.findall(pattern, anonymized, flags=re.IGNORECASE)
        for match in matches:
            anonymized = anonymized.replace(match, f"[{label.upper()}]")

    return anonymized

def anonymize_chat_message(msg: ChatMessage) -> ChatMessage:
    
    # Anonimiza o conteúdo da mensagem
    anonymized_message = anonymize_message_content(msg.message)
    
    return ChatMessage(
        timestamp=msg.timestamp,  # Mantém timestamp original
        sender=msg.sender,  # Mantém sender atual (já pode estar anonimizado)
        message=anonymized_message,
        original_sender=msg.original_sender if hasattr(msg, 'original_sender') else msg.sender,
        original_message=msg.original_message if hasattr(msg, 'original_message') else msg.message
    )

def anonymize_message(msg_line: str) -> str:
    """Função legada para compatibilidade - ainda funciona com linhas de texto"""
    # Para compatibilidade com código existente
    parsed = ChatMessage.from_line(msg_line)
    
    if parsed:
        anonymized = anonymize_chat_message(parsed)
        return anonymized.format_message()
    else:
        # Se não conseguir parsear, aplica regex diretamente
        return anonymize_message_content(msg_line)

def anonymize_messages(messages: list) -> list:
    """Anonimiza uma lista de mensagens (ChatMessage ou strings)"""
    result = []
    
    for msg in messages:
        if isinstance(msg, ChatMessage):
            result.append(anonymize_chat_message(msg))
        elif isinstance(msg, str):
            result.append(anonymize_message(msg))
        else:
            result.append(msg)
    
    return result

# Manter função original para compatibilidade
def anonymize_lines(lines):
    return [anonymize_message(line) for line in lines]

# if __name__ == "__main__":
#     input_path = "data/chat_original.txt"
#     output_path = "result/regex_results.txt"
    
#     with open(input_path, encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
#         for line in fin:
#             line = line.strip()
#             if line:
#                 original = line
#                 result = anonymize_message(line)
                
#                 # Print no console (mesmo formato do limpeza.py)
#                 print("📨 Original:")
#                 print(original)
#                 print("🔒 Anonimizada:")
#                 print(result)
#                 print("-" * 50)
                
#                 # Escrita no arquivo (mesmo formato do limpeza.py)
#                 fout.write("📨 Original:\n")
#                 fout.write(original + "\n")
#                 fout.write("🔒 Anonimizada:\n")
#                 fout.write(result + "\n")
#                 fout.write("-" * 50 + "\n")