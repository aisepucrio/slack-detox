from dataclasses import dataclass
from typing import List

@dataclass
class ChatMessage:
    timestamp: str
    sender: str
    message: str
    original_message: str = None  # Para guardar a mensagem original
    original_sender: str = None   # Para guardar o sender original
    
    def __post_init__(self):
        # Se não foi especificado, original é igual ao atual
        if self.original_message is None:
            self.original_message = self.message
        if self.original_sender is None:
            self.original_sender = self.sender
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'sender': self.sender,
            'message': self.message,
            'original_sender': self.original_sender,
            'original_message': self.original_message
        }
    
    @classmethod
    def from_line(cls, line: str):
        # Assume formato: [timestamp] sender: message
        # Ou apenas retorna como mensagem simples se não conseguir parsear
        line = line.strip()
        if not line:
            return None
            
        # Tentativa simples de extrair timestamp, sender e message
        if line.startswith('[') and '] ' in line and ': ' in line:
            try:
                # [timestamp] sender: message
                timestamp_end = line.find('] ')
                timestamp = line[1:timestamp_end]
                
                remaining = line[timestamp_end + 2:]
                sender_end = remaining.find(': ')
                sender = remaining[:sender_end]
                message = remaining[sender_end + 2:]
                
                return cls(timestamp=timestamp, sender=sender, message=message)
            except:
                pass
        
        # Se não conseguir parsear, trata como mensagem genérica
        return cls(timestamp="", sender="unknown", message=line)
    
    def format_message(self) -> str:
        """Formato apenas com mensagem anonimizada"""
        if self.timestamp:
            return f"[{self.timestamp}] {self.sender}: {self.message}"
        else:
            return f"{self.sender}: {self.message}"
    
    def format_comparison(self) -> str:
        """Formato com comparação original vs anonimizado"""
        if self.timestamp:
            original = f"[{self.timestamp}] {self.original_sender}: {self.original_message}"
            anonymized = f"[{self.timestamp}] {self.sender}: {self.message}"
        else:
            original = f"{self.original_sender}: {self.original_message}"
            anonymized = f"{self.sender}: {self.message}"
        
        return f"ORIGINAL: {original}\nANONIMIZADO: {anonymized}\n" + "="*50

def load_messages_from_file(file_path: str) -> List[ChatMessage]:
    """Carrega mensagens de um arquivo assumindo formato genérico"""
    messages = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            i = 0
            lines = f.readlines()
            while i < len(lines):
                line = lines[i].strip()
                
                # Verificar se é um arquivo de comparação (formato ORIGINAL/ANONIMIZADO)
                if line.startswith("ORIGINAL: ") and i + 1 < len(lines) and lines[i + 1].strip().startswith("ANONIMIZADO: "):
                    # Extrair dados do formato de comparação
                    original_line = line[10:]  # Remove "ORIGINAL: "
                    anonymized_line = lines[i + 1].strip()[12:]  # Remove "ANONIMIZADO: "
                    
                    # Parsear linha original
                    original_msg = ChatMessage.from_line(original_line)
                    # Parsear linha anonimizada
                    anonymized_msg = ChatMessage.from_line(anonymized_line)
                    
                    if original_msg and anonymized_msg:
                        # Criar mensagem com dados originais preservados
                        msg = ChatMessage(
                            timestamp=anonymized_msg.timestamp,
                            sender=anonymized_msg.sender,
                            message=anonymized_msg.message,
                            original_sender=original_msg.sender,
                            original_message=original_msg.message
                        )
                        messages.append(msg)
                    
                    # Pular as próximas 2 linhas (linha anonimizada e separador)
                    i += 3
                else:
                    # Formato normal
                    msg = ChatMessage.from_line(line)
                    if msg and msg.message:  # Ignora linhas vazias
                        messages.append(msg)
                    i += 1
                    
    except FileNotFoundError:
        print(f"Erro: Arquivo {file_path} não encontrado")
    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}")
    
    return messages

def save_messages_to_file(messages: List[ChatMessage], file_path: str):
    """Salva apenas mensagens anonimizadas"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for msg in messages:
                f.write(msg.format_message() + '\n')
    except Exception as e:
        print(f"Erro ao salvar arquivo {file_path}: {e}")

def save_messages_comparison_to_file(messages: List[ChatMessage], file_path: str):
    """Salva comparação original vs anonimizado"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for msg in messages:
                f.write(msg.format_comparison() + '\n')
    except Exception as e:
        print(f"Erro ao salvar arquivo {file_path}: {e}")
