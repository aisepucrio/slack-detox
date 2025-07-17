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
[DD/MM/YY, HH:MM:SS] Nome: Mensagem
[DD/MM/YY, HH:MM:SS] +55 11 99999-9999: Mensagem
```

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
├── result/                      # Gerado automaticamente
├── src/                         # Código-fonte da pipeline
├── main.py                      # Script principal
└── README.md
```

---

## 🚀 Etapas da Pipeline

### Etapa 1: Anonimizador de IDs

* Entrada: `data/chat_original.txt`
* Saída:

  * `result/id_anon.txt`
  * `result/id_anon_all.txt`
* Substitui números por `user_1`, `user_2`, etc.

### Etapa 2: Regex Anonymizer

* Entrada: `result/id_anon.txt`
* Saída:

  * `result/pre_processado.txt`
  * `result/pre_processado_all.txt`
* Usa padrões regex para anonimizar dados sensíveis

### Etapa 3: Substituição de Apelidos

* Entrada: `result/pre_processado.txt`
* Saída:

  * `result/apelidos_anon.txt`
  * `result/apelidos_anon_all.txt`
* Troca apelidos da lista por `PESSOA`

### Etapa 4: BERT Local

* Entrada: `result/apelidos_anon.txt`
* Saída:

  * `result/result_final.txt` ⭐
  * `result/result_final_all.txt`
* Usa IA local para anonimização final de entidades

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

* Verifique `data/chat_original.txt`

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
📝 Apelidos carregados: Pereira, bolota, coutinho
🛡️  Palavras protegidas: jira, github, eduardo, zoom, overleaf, figma, stone, google, slides
============================================================
📁 Etapa 1: data/chat_original.txt -> result/id_anon.txt + result/id_anon_all.txt
✅ Etapa 1 concluída!
============================================================
📁 Etapa 2: result/id_anon.txt -> result/pre_processado.txt + result/pre_processado_all.txt
✅ Etapa 2 concluída!
============================================================
📁 Etapa 3: result/pre_processado.txt -> result/apelidos_anon.txt + result/apelidos_anon_all.txt
✅ Etapa 3 concluída!
============================================================
📁 Etapa 4: result/apelidos_anon.txt -> result/result_final.txt + result/result_final_all.txt
🤖 Processando com BERT LOCAL...
✅ Etapa 4 concluída!
============================================================
🎉 Pipeline de anonimização finalizado com sucesso!

📊 Resumo:
   🆔 result/id_anon.txt - Mensagens anonimizadas por ID
   🔧 result/pre_processado.txt - Anonimizadas por regex
   😎 result/apelidos_anon.txt - Apelidos substituídos
   🎯 result/result_final.txt - Resultado final ⭐
```

---

## 🔄 Atualização e Reuso

* Totalmente offline após primeira execução
* Use `result_final.txt` para exportar ou integrar
* Edite `data/` para novos testes ou datasets

---