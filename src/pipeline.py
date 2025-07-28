"""
Pipeline de processamento para anonimização de chats.
Processa mensagens já estruturadas no formato genérico (timestamp, sender, message).
"""

import os
from .chat_message import load_messages_from_file, save_messages_to_file, save_messages_comparison_to_file
from .id_anon import anonymize_chat_message_id
from .regex_anon import anonymize_chat_message
from .apelidos import anonimizar_apelidos_chat_message
from .pt_bert_local import anonymize_chat_message_bert


def process_with_id(input_file, output_clean, output_all, whitelist):
    """
    Etapa 1: Anonimização de IDs e nomes de usuários.
    
    Args:
        input_file: Arquivo de entrada com mensagens
        output_clean: Arquivo de saída apenas com mensagens processadas
        output_all: Arquivo de saída com todas as transformações
        whitelist: Lista de palavras protegidas
    """
    messages = load_messages_from_file(input_file)
    clean_messages = []
    all_messages = []
    
    for message in messages:
        # Na primeira etapa, garantir que original_* são realmente originais
        if not hasattr(message, 'original_sender') or message.original_sender is None:
            message.original_sender = message.sender
        if not hasattr(message, 'original_message') or message.original_message is None:
            message.original_message = message.message
            
        processed_msg = anonymize_chat_message_id(message)
        clean_messages.append(processed_msg)
        all_messages.append(processed_msg)  # Mesmo objeto para ambos
    
    save_messages_to_file(clean_messages, output_clean)  # Apenas anonimizado
    save_messages_comparison_to_file(all_messages, output_all)  # Comparação


def process_with_regex(input_file, output_clean, output_all, whitelist):
    """
    Etapa 2: Anonimização usando regex para dados sensíveis.
    
    Args:
        input_file: Arquivo de entrada
        output_clean: Arquivo de saída apenas com mensagens processadas
        output_all: Arquivo de saída com todas as transformações
        whitelist: Lista de palavras protegidas
    """
    # Ler do arquivo _all.txt da etapa anterior se existir
    input_all_file = input_file.replace('.txt', '_all.txt')
    if os.path.exists(input_all_file):
        messages = load_messages_from_file(input_all_file)
    else:
        messages = load_messages_from_file(input_file)
    
    clean_messages = []
    all_messages = []
    
    for message in messages:
        processed_msg = anonymize_chat_message(message)
        clean_messages.append(processed_msg)
        all_messages.append(processed_msg)  # Mesmo objeto para ambos
    
    save_messages_to_file(clean_messages, output_clean)  # Apenas anonimizado
    save_messages_comparison_to_file(all_messages, output_all)  # Comparação


def process_with_apelidos(input_file, output_clean, output_all, apelidos_lista, whitelist):
    """
    Etapa 3: Anonimização usando lista de apelidos.
    
    Args:
        input_file: Arquivo de entrada
        output_clean: Arquivo de saída apenas com mensagens processadas
        output_all: Arquivo de saída com todas as transformações
        apelidos_lista: Lista de apelidos para anonimizar
        whitelist: Lista de palavras protegidas
    """
    # Ler do arquivo _all.txt da etapa anterior se existir
    input_all_file = input_file.replace('.txt', '_all.txt')
    if os.path.exists(input_all_file):
        messages = load_messages_from_file(input_all_file)
    else:
        messages = load_messages_from_file(input_file)
    
    clean_messages = []
    all_messages = []
    
    for message in messages:
        processed_msg = anonimizar_apelidos_chat_message(message, apelidos_lista)
        clean_messages.append(processed_msg)
        all_messages.append(processed_msg)  # Mesmo objeto para ambos
    
    save_messages_to_file(clean_messages, output_clean)  # Apenas anonimizado
    save_messages_comparison_to_file(all_messages, output_all)  # Comparação


def process_with_bert(input_file, output_clean, output_all, whitelist):
    """
    Etapa 4: Anonimização usando BERT para detecção de entidades.
    
    Args:
        input_file: Arquivo de entrada
        output_clean: Arquivo de saída apenas com mensagens processadas
        output_all: Arquivo de saída com todas as transformações
        whitelist: Lista de palavras protegidas
        
    Returns:
        bool: True se o processamento foi bem-sucedido, False caso contrário
    """
    try:
        messages = load_messages_from_file(input_file)
        clean_messages = []
        all_messages = []
        
        for message in messages:
            processed_msg = anonymize_chat_message_bert(message)
            clean_messages.append(processed_msg)
            all_messages.append(processed_msg)  # Mesmo objeto para ambos
        
        save_messages_to_file(clean_messages, output_clean)  # Apenas anonimizado
        save_messages_comparison_to_file(all_messages, output_all)  # Comparação
        return True
        
    except Exception as e:
        print(f"⚠️  Erro no processamento BERT: {e}")
        print("📝 Copiando arquivo da etapa anterior...")
        
        # Copiar arquivo da etapa anterior se BERT falhar
        import shutil
        shutil.copy2(input_file, output_clean)
        shutil.copy2(input_file, output_all)
        return False