# 🔒 Pipeline de Anonimização de Chats - 100% LOCAL

Pipeline completo para anonimização de conversas em 4 etapas sequenciais, com proteção de whitelist e configuração externa.

## 🚀 INSTALAÇÃO RÁPIDA

### 1. Clone o Repositório
```bash
git clone https://github.com/aisepucrio/slack-detox.git
cd slack-detox
```

### 2. Instale as Dependências Locais
```bash
# Instalar dependências Python
pip install -r requirements.txt

# Instalar modelo português do spaCy (apenas uma vez)
python -m spacy download pt_core_news_sm
```

### 3. Configure seus Dados
```bash
# Coloque seu arquivo de chat em:
data/chat_original.txt

# Configure apelidos (opcional):
data/apelidos_lista.txt

# Configure whitelist (opcional):
data/whitelist.txt
```

### 4. Execute o Pipeline
```bash
python main.py
```

## 📦 O que será Baixado na Primeira Execução

- **Modelo BERT português**: ~400MB (baixado uma vez)
- **Local do cache**: `~/.cache/huggingface/transformers/`

**Execuções posteriores**: ✅ Offline completo, carregamento rápido, dados nunca saem da máquina

## 🔧 Verificação de Instalação

### Teste Básico
```bash
python -c "import transformers, torch, spacy; print('✅ Todas dependências OK')"
```

### Teste do Modelo spaCy
```bash
python -c "import spacy; nlp = spacy.load('pt_core_news_sm'); print('✅ Modelo português OK')"
```

### Teste do BERT
```bash
python -c "from src.pt_bert_local import is_bert_available; print('✅ BERT OK' if is_bert_available() else '❌ BERT falhou')"
```

### 📋 Checklist de Instalação

- [ ] Python 3.7+ instalado
- [ ] Dependências do `requirements.txt` instaladas
- [ ] Modelo spaCy português baixado
- [ ] Arquivo `data/chat_original.txt` presente
- [ ] Teste básico executado com sucesso
- [ ] Pipeline completo executado uma vez

## 🗂️ CONFIGURAÇÃO DOS DADOS

### Estrutura de Arquivos Necessária
```
projeto/
├── data/
│   ├── chat_original.txt        # SEU ARQUIVO DE CHAT (obrigatório)
│   ├── apelidos_lista.txt       # Lista de apelidos para anonimizar
│   └── whitelist.txt           # Palavras protegidas da anonimização
├── src/
│   ├── pipeline.py
│   ├── whitelist.py
│   └── utils.py
├── main.py
└── result/                     # Pasta criada automaticamente
```

### 1. Arquivo Principal: `data/chat_original.txt`
Coloque seu arquivo de chat exportado aqui. Formato esperado:
```
[DD/MM/YY, HH:MM:SS] Nome: Mensagem
[DD/MM/YY, HH:MM:SS] +55 11 99999-9999: Mensagem
```

### 2. Lista de Apelidos: `data/apelidos_lista.txt`
Um apelido por linha (palavras que serão substituídas por `PESSOA`):
```
Pereira
Fofucho
Coutinho
```

### 3. Lista de Proteção: `data/whitelist.txt`
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

## 🚀 COMO EXECUTAR

### Comando Único
```bash
python main.py
```

Este comando executará automaticamente todas as 4 etapas em sequência.

## 📊 ETAPAS DO PIPELINE

### Etapa 1: Anonimização de IDs
- **Entrada**: `data/chat_original.txt`
- **Saída**: 
  - `result/id_anon.txt` (apenas mensagens)
  - `result/id_anon_all.txt` (com metadados)
- **O que faz**: Substitui números de telefone por `user_1`, `user_2`, etc.

### Etapa 2: Processamento com Regex
- **Entrada**: `result/id_anon.txt`
- **Saída**: 
  - `result/pre_processado.txt` (apenas mensagens)
  - `result/pre_processado_all.txt` (com metadados)
- **O que faz**: Aplica padrões regex para anonimizar informações sensíveis

### Etapa 3: Substituição de Apelidos
- **Entrada**: `result/pre_processado.txt`
- **Saída**: 
  - `result/apelidos_anon.txt` (apenas mensagens)
  - `result/apelidos_anon_all.txt` (com metadados)
- **O que faz**: Substitui apelidos da lista por `PESSOA`

### Etapa 4: Processamento BERT LOCAL (Resultado Final)
- **Entrada**: `result/apelidos_anon.txt`
- **Saída**: 
  - `result/result_final.txt` ✨ **ARQUIVO PRINCIPAL**
  - `result/result_final_all.txt` (com metadados)
- **O que faz**: Usa IA local (BERT) para identificar e anonimizar entidades nomeadas
- **Segurança**: Processamento 100% local, sem envio de dados para APIs

## 🎯 ARQUIVOS DE RESULTADO

### Principais para Uso
- **`result/result_final.txt`** → Arquivo final anonimizado (apenas mensagens)
- **`result/result_final_all.txt`** → Arquivo final com timestamps e metadados

### Intermediários (para debug)
- `result/id_anon.txt` → Após etapa 1
- `result/pre_processado.txt` → Após etapa 2  
- `result/apelidos_anon.txt` → Após etapa 3

## 🛡️ SISTEMA DE WHITELIST

O sistema protege palavras específicas em **todas as etapas**:

1. **Antes de cada processamento**: Palavras da whitelist são temporariamente substituídas por placeholders únicos
2. **Após processamento**: Placeholders são restaurados às palavras originais
3. **Resultado**: Palavras protegidas permanecem intactas no resultado final

### Exemplo
```
Entrada: "Vamos usar o jira para organizar"
Com whitelist: ["jira"]
Resultado: "Vamos usar o jira para organizar" (jira protegido)
```

## 📋 EXEMPLO DE EXECUÇÃO

```bash
$ python main.py

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
✅ Carregando modelo BERT local: neuralmind/bert-base-portuguese-cased
✅ Etapa 4 concluída!
============================================================
🎉 Pipeline de anonimização finalizado com sucesso!

📊 Resumo dos arquivos gerados:
   🆔 result/id_anon.txt - Mensagens anonimizadas por ID
   🔧 result/pre_processado.txt - Mensagens anonimizadas por regex
   😎 result/apelidos_anon.txt - Mensagens com apelidos substituídos
   🎯 result/result_final.txt - Resultado final da anonimização ⭐
```

## 🛠️ RESOLUÇÃO DE PROBLEMAS

### Erro: "Arquivo não encontrado"
- Verifique se `data/chat_original.txt` existe
- Certifique-se de que está no diretório correto

### Erro: "No module named 'transformers'"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro: "Can't find model 'pt_core_news_sm'"
```bash
python -m spacy download pt_core_news_sm
```

### Erro: "Dependências BERT não disponíveis"
- Execute: `pip install -r requirements.txt`
- Execute: `python -m spacy download pt_core_news_sm`
- **Primeira execução**: Modelo BERT será baixado (~400MB) e salvo localmente

### Pipeline para sem BERT
- O pipeline continuará e gerará todos os outros arquivos
- Apenas os arquivos `result_final.*` não serão criados

### Modelo BERT não baixa
- Verifique conexão com internet (apenas na primeira vez)
- Modelo fica em cache local após download: `~/.cache/huggingface/`
- Após primeira instalação, funciona completamente offline

### Erro de Cache/Download BERT
```bash
# Limpar cache e tentar novamente
rm -rf ~/.cache/huggingface/
python main.py
```

### Problemas de Memória
- **RAM mínima recomendada**: 4GB
- **Espaço em disco**: 2GB para modelos

### Whitelist não funciona
- Verifique se `data/whitelist.txt` existe
- Uma palavra por linha, sem espaços extras
- Palavras são case-insensitive

## 📁 ESTRUTURA FINAL DE ARQUIVOS

```
projeto/
├── data/
│   ├── chat_original.txt       # Seu arquivo original
│   ├── apelidos_lista.txt      # Configuração de apelidos
│   └── whitelist.txt          # Configuração de proteção
├── result/
│   ├── result_final.txt       # ⭐ RESULTADO PRINCIPAL
│   ├── result_final_all.txt   # Resultado com metadados
│   ├── id_anon.txt           # Etapa 1
│   ├── pre_processado.txt    # Etapa 2
│   ├── apelidos_anon.txt     # Etapa 3
│   └── ...arquivos _all.txt  # Versões com metadados
├── src/                      # Código fonte
├── main.py                   # Script principal
└── README.md                 # Este arquivo
```

## 🎯 PRÓXIMOS PASSOS

Após instalação completa:
1. Configure seus arquivos em `data/`
2. Execute `python main.py`
3. Use o arquivo `result/result_final.txt` como resultado anonimizado
4. Verifique os arquivos intermediários se necessário para debug
5. Para uso futuro: funciona offline!