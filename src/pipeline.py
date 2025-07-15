import os
from typing import List, Optional
from src.regex_anon import anonymize_message
from src.id_anon import anonymize_message_id
from src.apelidos import anonimizar_apelidos
from src.whitelist import protect_whitelist_words, restore_whitelist_words

# Importação condicional do BERT LOCAL
try:
    from src.pt_bert_local import anonymize_text as bert_anonymize, is_bert_available
    BERT_AVAILABLE = is_bert_available()
    if BERT_AVAILABLE:
        print("✅ BERT local disponível")
    else:
        print("⚠️  BERT local não disponível (dependências não instaladas)")
except ImportError as e:
    print(f"⚠️  Aviso: BERT local não disponível - {e}")
    print("💡 Execute 'pip install transformers torch' para usar BERT local")
    BERT_AVAILABLE = False
    
    def bert_anonymize(text):
        """Fallback: retorna o texto original se BERT não estiver disponível"""
        return text

def process_with_id(input_path: str, output_clean_path: str, output_all_path: str, whitelist: Optional[List[str]] = None):
    """
    Processa chat_original.txt com id_anon.py
    Gera id_anon.txt (apenas anonimizadas) e id_anon_all.txt (originais + anonimizadas)
    """
    print("🆔 Processando com ID Anonymizer...")
    
    with open(input_path, "r", encoding="utf-8") as fin, \
         open(output_clean_path, "w", encoding="utf-8") as fout_clean, \
         open(output_all_path, "w", encoding="utf-8") as fout_all:
        
        for line in fin:
            line = line.strip()
            if line:
                # Proteger palavras da whitelist
                protected_line, placeholders = protect_whitelist_words(line, whitelist or [])
                
                # Aplicar anonimização
                anonymized = anonymize_message_id(protected_line)
                
                # Restaurar palavras protegidas
                anonymized = restore_whitelist_words(anonymized, placeholders)

                # Arquivo apenas com mensagens anonimizadas
                fout_clean.write(anonymized + "\n")

                # Arquivo com formato completo (original + anonimizada)
                fout_all.write("📨 Original:\n")
                fout_all.write(line + "\n")
                fout_all.write("🔒 Anonimizada:\n")
                fout_all.write(anonymized + "\n")
                fout_all.write("-" * 50 + "\n")

                # Print no console
                print("📨 Original:")
                print(line)
                print("🔒 Anonimizada:")
                print(anonymized)
                print("-" * 50)

def process_with_regex(input_path: str, output_clean_path: str, output_all_path: str, whitelist: Optional[List[str]] = None):
    """
    Processa id_anon.txt com regex_anon.py
    Gera pre_processado.txt (apenas anonimizadas) e pre_processado_all.txt (originais + anonimizadas)
    """
    print("🔧 Processando com Regex...")
    
    with open(input_path, "r", encoding="utf-8") as fin, \
         open(output_clean_path, "w", encoding="utf-8") as fout_clean, \
         open(output_all_path, "w", encoding="utf-8") as fout_all:
        
        for line in fin:
            line = line.strip()
            if line:
                # Proteger palavras da whitelist
                protected_line, placeholders = protect_whitelist_words(line, whitelist or [])
                
                # Aplicar anonimização
                anonymized = anonymize_message(protected_line)
                
                # Restaurar palavras protegidas
                anonymized = restore_whitelist_words(anonymized, placeholders)

                # Arquivo apenas com mensagens anonimizadas
                fout_clean.write(anonymized + "\n")

                # Arquivo com formato completo (original + anonimizada)
                fout_all.write("📨 Original:\n")
                fout_all.write(line + "\n")
                fout_all.write("🔒 Anonimizada:\n")
                fout_all.write(anonymized + "\n")
                fout_all.write("-" * 50 + "\n")

                # Print no console
                print("📨 Original:")
                print(line)
                print("🔒 Anonimizada:")
                print(anonymized)
                print("-" * 50)

def process_with_apelidos(input_path: str, output_clean_path: str, output_all_path: str, apelidos: List[str], whitelist: Optional[List[str]] = None):
    """
    Processa com anonimização de apelidos
    """
    print("😎 Processando com Apelidos...")
    
    with open(input_path, "r", encoding="utf-8") as fin, \
         open(output_clean_path, "w", encoding="utf-8") as fout_clean, \
         open(output_all_path, "w", encoding="utf-8") as fout_all:
        
        for line in fin:
            line = line.strip()
            if line:
                # Proteger palavras da whitelist
                protected_line, placeholders = protect_whitelist_words(line, whitelist or [])
                
                # Aplicar anonimização de apelidos
                final = anonimizar_apelidos(protected_line, apelidos)
                
                # Restaurar palavras protegidas
                final = restore_whitelist_words(final, placeholders)
                
                fout_clean.write(final + "\n")
                fout_all.write("📨 Original:\n")
                fout_all.write(line + "\n")
                fout_all.write("🔒 Anonimizada:\n")
                fout_all.write(final + "\n")
                fout_all.write("-" * 50 + "\n")
                print("📨 Original:")
                print(line)
                print("🔒 Anonimizada:")
                print(final)
                print("-" * 50)

def process_with_bert(input_path: str, output_clean_path: str, output_all_path: str, whitelist: Optional[List[str]] = None):
    """
    Processa com BERT local (pt_bert_local.py)
    Gera result_final.txt (apenas anonimizadas) e result_final_all.txt (originais + anonimizadas)
    """
    if not BERT_AVAILABLE:
        print("⚠️  BERT local não disponível. Pulando etapa do BERT...")
        return False
        
    print("🤖 Processando com BERT LOCAL...")
    
    with open(input_path, "r", encoding="utf-8") as fin, \
         open(output_clean_path, "w", encoding="utf-8") as fout_clean, \
         open(output_all_path, "w", encoding="utf-8") as fout_all:
        
        for line in fin:
            line = line.strip()
            if line:
                # Proteger palavras da whitelist
                protected_line, placeholders = protect_whitelist_words(line, whitelist or [])
                
                # Aplicar anonimização BERT local
                bert_result = bert_anonymize(protected_line)
                
                # Restaurar palavras protegidas
                bert_result = restore_whitelist_words(bert_result, placeholders)

                # Arquivo apenas com mensagens anonimizadas pelo BERT
                fout_clean.write(bert_result + "\n")

                # Arquivo com formato completo (original + anonimizada pelo BERT)
                fout_all.write("📨 Original:\n")
                fout_all.write(line + "\n")
                fout_all.write("🔒 Anonimizada:\n")
                fout_all.write(bert_result + "\n")
                fout_all.write("-" * 50 + "\n")
            
                # Print no console
                print("📨 Original:")
                print(line)
                print("🔒 Anonimizada:")
                print(bert_result)
                print("-" * 50)
    
    return True
