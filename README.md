# 🔐 Pipeline de Anonimização de Chats - 100% LOCAL

Pipeline completo em 4 etapas para anonimizar conversas de chat, com suporte a whitelist e lista de apelidos, funcionando totalmente offline após a primeira execução.

## 📊 Requisitos

* Python 3.7+
* \~2GB de espaço em disco (cache e arquivos)
* \~4GB de RAM

## 🚀 Instalação Rápida

### 1. Clone o Repositório

```bash
git clone https://github.com/aisepucrio/slack-detox.git
cd slack-detox
```

### 2. Instale as Dependências

```bash
# Dependências Python
pip install -r requirements.txt

# Baixar modelo spaCy para português (executar apenas uma vez)
python -m spacy download pt_core_news_sm
```

### 3. Prepare seus Dados

```bash
# Arquivo do chat:
data/chat_original.txt

# Lista de apelidos (opcional):
data/apelidos_lista.txt

# Whitelist de palavras protegidas (opcional):
data/whitelist.txt
```

#### Formatos esperados:

### - Arquivo Principal: `data/chat_original.txt`

Coloque seu arquivo de chat exportado aqui. Formato esperado:

```
[timestamp] sender: message
[23/07/2025 19:56] vide: oi, johny!
[23/07/2025 19:56] johny: Oi Theo
```

**Nota**: O sistema assume que os dados já vêm estruturados neste formato genérico `(timestamp, sender, message)`.

### - Lista de Apelidos: `data/apelidos_lista.txt`

Um apelido por linha (palavras que serão substituídas por `PESSOA`):

```
Pereira
Fofucho
Coutinho
```

### - Lista de Proteção: `data/whitelist.txt`

Uma palavra por linha (palavras que NÃO serão anonimizadas):

```
jira
github
zoom
overleaf
figma
stone
google
slides
```

### 4. Execute o Pipeline

```bash
python main.py
```

### Usando dados de exemplo

```bash
python main.py --example
```

---

## 📦 Download Automático (Primeira Execução)

* Modelo BERT em português (\~400MB)
* Cache salvo em: `~/.cache/huggingface/transformers/`
* Execuções futuras: 100% offline

---

## 🔧 Verificando Instalação

### Teste das dependências

```bash
python -c "import transformers, torch, spacy; print('✅ Todas dependências OK')"
```

### Teste do spaCy

```bash
python -c "import spacy; spacy.load('pt_core_news_sm'); print('✅ Modelo spaCy OK')"
```

### Teste do BERT local

```bash
python -c "from src.pt_bert_local import is_bert_available; print('✅ BERT OK' if is_bert_available() else '❌ BERT falhou')"
```

---

## 👜 Estrutura de Arquivos Esperada

```
projeto/
├── data/
│   ├── chat_original.txt        # Arquivo de chat (obrigatório)
│   ├── apelidos_lista.txt       # Lista de apelidos
│   └── whitelist.txt            # Palavras protegidas
├── example/                     # Pasta com dados de exemplo
│   ├── data/                    # Dados mock para teste
│   └── result/                  # Resultados da pipeline de exemplo
├── result/                      # Gerado automaticamente
├── src/                         # Código-fonte da pipeline
├── main.py                      # Script principal
└── README.md
```

---

## 📁 Exemplo Prático

Para facilitar o entendimento, incluímos uma pasta `example/` com dados mock e os resultados completos da pipeline de anonimização:

### Dados de Exemplo (`example/data/`)

* **`chat_original.txt`**: Conversa de exemplo entre "vide", "johny" e menções ao "coutinho"
* **`apelidos_lista.txt`**: Contém "Coutinho" como apelido a ser anonimizado
* **`whitelist.txt`**: Protege a palavra "Jira" da anonimização

### Resultados da Pipeline (`example/result/`)

Todos os arquivos gerados pelas 4 etapas da pipeline, mostrando como:
* Nomes de usuários são substituídos por `[PESSOA]`
* E-mails são anonimizados para `[EMAIL]`
* A palavra "Jira" é preservada (whitelist)
* Apelidos como "coutinho" são corretamente identificados

**Dica**: Examine os arquivos em `example/result/` para entender como cada etapa transforma o texto original.

---

## 🏗️ Arquitetura Modular

### Estrutura de Dados Unificada

O sistema utiliza uma estrutura padronizada `(timestamp, sender, message)` e assume que os dados já vêm neste formato genérico:

```python
@dataclass
class ChatMessage:
    timestamp: str    # Data/hora da mensagem  
    sender: str       # Nome do remetente
    message: str      # Conteúdo da mensagem
```

### Pipeline de Anonimização

O sistema processa mensagens já estruturadas através de 4 etapas:

1. **ID Anonymizer** → Anonimiza senders e menções `@user`
2. **Regex Anonymizer** → Remove dados sensíveis (CPF, email, etc.)
3. **Apelidos** → Substitui apelidos por `[PESSOA]`
4. **BERT Local** → IA para detecção de entidades nomeadas

**Entrada esperada**: Dados já no formato `[timestamp] sender: message`  
**Saída**: Mensagens totalmente anonimizadas

---

## 🎲 Estrutura Simplificada

### Formato de Entrada Esperado

O sistema foi projetado para trabalhar com dados **já estruturados** no formato genérico:

```
[timestamp] sender: message
```

**Exemplos válidos:**
```
[23/07/2025 19:56] vide: oi, johny!
[2025-07-23 19:56:30] user123: mensagem de teste
[23/07 19:56] João: como vai?
```

### Arquivos Principais

```
src/
├── chat_message.py          # Estrutura ChatMessage simplificada
├── pipeline.py              # Pipeline de 4 etapas
├── id_anon.py               # Anonimização de IDs/senders
├── regex_anon.py            # Regex para dados sensíveis
├── apelidos.py              # Substituição de apelidos
├── pt_bert_local.py         # BERT para entidades nomeadas
├── utils.py                 # Utilitários
└── whitelist.py             # Sistema de proteção
```

---

## 🚀 Etapas da Pipeline

### Etapa 1: Anonimizador de IDs

* Entrada: `data/chat_original.txt`
* Saída:
  * `result/id_anon.txt`
  * `result/id_anon_all.txt`
* Substitui senders e menções por `[PESSOA]`

### Etapa 2: Regex Anonymizer

* Entrada: `result/id_anon.txt`
* Saída:
  * `result/pre_processado.txt`
  * `result/pre_processado_all.txt`
* Usa padrões regex para anonimizar dados sensíveis (CPF, email, telefone, etc.)

### Etapa 3: Substituição de Apelidos

* Entrada: `result/pre_processado.txt`
* Saída:
  * `result/apelidos_anon.txt`
  * `result/apelidos_anon_all.txt`
* Troca apelidos da lista por `[PESSOA]`

### Etapa 4: BERT Local

* Entrada: `result/apelidos_anon.txt`
* Saída:
  * `result/result_final.txt` ⭐
  * `result/result_final_all.txt`
* Usa IA local para detecção e anonimização de entidades nomeadas

---

## 📉 Resultados

| Arquivo                       | Descrição                   |
| ----------------------------- | --------------------------- |
| `result/result_final.txt`     | Resultado final anonimizado |
| `result/result_final_all.txt` | Final + metadados do chat   |
| `result/id_anon.txt`          | Após etapa 1                |
| `result/pre_processado.txt`   | Após etapa 2                |
| `result/apelidos_anon.txt`    | Após etapa 3                |

---

## 🛡️ Sistema de Whitelist

Palavras protegidas não são anonimizadas:

1. Substituídas temporariamente por placeholders
2. Texto é anonimizado normalmente
3. Placeholders são restaurados ao final

**Exemplo:**

```
Entrada: "Vamos usar o jira para organizar"
Com whitelist: ["jira"]
Resultado: "Vamos usar o jira para organizar"
```

---

## 🔍 Solução de Problemas

### Arquivo não encontrado

* Verifique se `data/chat_original.txt` existe
* Certifique-se que o formato está correto: `[timestamp] sender: message`

### Formato de dados incorreto

* O sistema espera dados já estruturados no formato genérico
* Converta manualmente dados de WhatsApp/Slack/Discord antes de processar
* Verifique se cada linha segue o padrão: `[timestamp] sender: message`

### Módulos não encontrados

```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
```

### Modelo spaCy não baixado

```bash
python -m spacy download pt_core_news_sm
```

### BERT falha ou não inicia

* Verifique se internet está ativa na primeira execução
* Modelo é cacheado em `~/.cache/huggingface/`
* Reinstale com:

```bash
rm -rf ~/.cache/huggingface/
python main.py
```

### Sem BERT?

* A pipeline roda normalmente até a etapa 3
* Arquivos `result_final.*` não serão criados

---

## 🚀 Executando Tudo

```bash
python main.py
```

---

## 🌟 Exemplo de Saída

```
🚀 Iniciando pipeline de anonimização...
📝 Apelidos carregados: Coutinho
🛡️  Palavras protegidas: Jira
============================================================
📁 Etapa 1: data/chat_original.txt -> result/id_anon.txt + result/id_anon_all.txt
✅ Etapa 1 concluída! Arquivos gerados:
   - result/id_anon.txt
   - result/id_anon_all.txt
============================================================
📁 Etapa 2: result/id_anon.txt -> result/pre_processado.txt + result/pre_processado_all.txt
✅ Etapa 2 concluída! Arquivos gerados:
   - result/pre_processado.txt
   - result/pre_processado_all.txt
============================================================
📁 Etapa 3: result/pre_processado.txt -> result/apelidos_anon.txt + result/apelidos_anon_all.txt
✅ Etapa 3 concluída! Arquivos gerados:
   - result/apelidos_anon.txt
   - result/apelidos_anon_all.txt
============================================================
📁 Etapa 4: result/apelidos_anon.txt -> result/result_final.txt + result/result_final_all.txt
✅ Etapa 4 concluída! Arquivos gerados:
   - result/result_final.txt
   - result/result_final_all.txt
============================================================
🎉 Pipeline de anonimização finalizado com sucesso!
📊 Resumo dos arquivos gerados:
   🆔 result/id_anon.txt - Mensagens anonimizadas por ID
   🔧 result/pre_processado.txt - Mensagens anonimizadas por regex
   😎 result/apelidos_anon.txt - Mensagens com apelidos substituídos
   🎯 result/result_final.txt - Resultado final da anonimização ⭐
```

---

## 🔄 Atualização e Reuso

* Totalmente offline após primeira execução
* Use `result_final.txt` para exportar ou integrar
* Edite `data/` para novos testes ou datasets

---