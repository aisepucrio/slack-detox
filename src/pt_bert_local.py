"""
Processamento BERT 100% local para anonimização de entidades nomeadas.
Não utiliza APIs externas, apenas modelos baixados localmente.
"""
import os
import sys
from typing import List, Tuple, Optional

try:
    from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
    import torch
    BERT_AVAILABLE = True
except ImportError:
    BERT_AVAILABLE = False
    print("⚠️  Dependências BERT não encontradas. Instalando...")
    print("Execute: pip install torch transformers")

class LocalBertAnonymizer:
    """Anonimizador BERT 100% local"""
    
    def __init__(self, model_name: str = "neuralmind/bert-base-portuguese-cased"):
        """
        Inicializa o anonimizador com modelo local.
        
        Args:
            model_name: Nome do modelo HuggingFace para NER em português
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.pipe = None
        self.initialized = False
        
    def _download_model_if_needed(self) -> bool:
        """
        Baixa o modelo se não estiver disponível localmente.
        Só baixa uma vez, depois usa cache local.
        """
        try:
            print(f"🔄 Carregando modelo BERT local: {self.model_name}")
            
            # Tentar primeiro com modelo específico para NER português
            try:
                self.tokenizer = AutoTokenizer.from_pretrained("lfcc/bert-portuguese-ner")
                self.model = AutoModelForTokenClassification.from_pretrained("lfcc/bert-portuguese-ner")
                self.pipe = pipeline("token-classification", 
                                   model=self.model, 
                                   tokenizer=self.tokenizer,
                                   aggregation_strategy="simple")
                print("✅ Modelo NER português carregado com sucesso!")
                return True
            except Exception as e:
                print(f"⚠️  Modelo NER específico não disponível: {e}")
                print("🔄 Tentando modelo BERT base português...")
                
                # Fallback para modelo base português
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForTokenClassification.from_pretrained(self.model_name)
                self.pipe = pipeline("token-classification", 
                                   model=self.model, 
                                   tokenizer=self.tokenizer,
                                   aggregation_strategy="simple")
                print("✅ Modelo BERT base carregado com sucesso!")
                return True
                
        except Exception as e:
            print(f"❌ Erro ao carregar modelo BERT: {e}")
            print("💡 Dica: Execute 'pip install torch transformers' e verifique sua conexão")
            return False
    
    def initialize(self) -> bool:
        """Inicializa o modelo BERT se ainda não foi feito"""
        if self.initialized:
            return True
            
        if not BERT_AVAILABLE:
            return False
            
        success = self._download_model_if_needed()
        self.initialized = success
        return success
    
    def extract_entities(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Extrai entidades nomeadas do texto usando BERT local.
        
        Args:
            text: Texto para processar
            
        Returns:
            Lista de tuplas (start, end, label) com as entidades encontradas
        """
        if not self.initialize():
            return []
            
        try:
            # Processar com BERT
            results = self.pipe(text)
            
            # Filtrar apenas entidades PERSON
            entities = []
            for result in results:
                if result['entity_group'].upper() in ['PERSON', 'PER', 'PESSOA']:
                    entities.append((
                        result['start'],
                        result['end'], 
                        'PESSOA'
                    ))
            
            # Ordenar por posição
            entities.sort(key=lambda x: x[0])
            return entities
            
        except Exception as e:
            print(f"⚠️  Erro ao processar texto com BERT: {e}")
            return []
    
    def anonymize_text(self, text: str) -> str:
        """
        Anonimiza entidades nomeadas no texto.
        
        Args:
            text: Texto original
            
        Returns:
            Texto com entidades substituídas por [PESSOA]
        """
        entities = self.extract_entities(text)
        
        if not entities:
            return text
            
        # Reconstruir texto substituindo entidades
        result = []
        last_pos = 0
        
        for start, end, label in entities:
            # Adicionar texto antes da entidade
            result.append(text[last_pos:start])
            # Adicionar placeholder
            result.append(f"[{label}]")
            # Atualizar posição
            last_pos = end
            
        # Adicionar resto do texto
        result.append(text[last_pos:])
        
        return "".join(result)

def anonymize_chat_message_bert(msg):
    """Anonimiza uma mensagem estruturada usando BERT"""
    # Import aqui para evitar circular import
    from .chat_message import ChatMessage
    
    if not isinstance(msg, ChatMessage):
        return msg
    
    # Anonimiza apenas o conteúdo da mensagem com BERT
    # O sender já deve ter sido anonimizado em etapas anteriores
    anonymized_message = anonymize_text(msg.message)
    
    return ChatMessage(
        timestamp=msg.timestamp,
        sender=msg.sender,  # Mantém sender como está (já anonimizado)
        message=anonymized_message,
        original_sender=msg.original_sender if hasattr(msg, 'original_sender') else msg.sender,
        original_message=msg.original_message if hasattr(msg, 'original_message') else msg.message
    )

def anonymize_messages_bert(messages: list) -> list:
    """Anonimiza uma lista de mensagens usando BERT"""
    result = []
    
    for msg in messages:
        if hasattr(msg, 'timestamp'):  # É ChatMessage
            result.append(anonymize_chat_message_bert(msg))
        elif isinstance(msg, str):
            # Para compatibilidade com código legado
            result.append(anonymize_text(msg))
        else:
            result.append(msg)
    
    return result

# Instância global do anonimizador
_anonymizer = None

def get_anonymizer() -> LocalBertAnonymizer:
    """Retorna instância singleton do anonimizador"""
    global _anonymizer
    if _anonymizer is None:
        _anonymizer = LocalBertAnonymizer()
    return _anonymizer

def anonymize_text(text: str) -> str:
    """
    Função principal para anonimizar texto usando BERT local.
    
    Args:
        text: Texto para anonimizar
        
    Returns:
        Texto anonimizado
    """
    anonymizer = get_anonymizer()
    return anonymizer.anonymize_text(text)

def is_bert_available() -> bool:
    """Verifica se BERT está disponível"""
    return BERT_AVAILABLE

# Compatibilidade com versão anterior
highlight_entities = anonymize_text
