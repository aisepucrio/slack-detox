import os
import sys
from src.pipeline import process_with_id, process_with_regex, process_with_apelidos, process_with_bert
from src.whitelist import load_whitelist_from_file
from src.utils import load_apelidos_from_file

def main():
    # Detectar se é para usar os arquivos de exemplo ou da pasta data
    use_example = len(sys.argv) > 1 and sys.argv[1] == "--example"
    
    if use_example:
        print("🧪 Usando dados de exemplo...")
        base_path = "example"
    else:
        print("📁 Usando dados da pasta data...")
        base_path = "data"
    
    # Criar diretórios se não existirem
    os.makedirs(f"{base_path}/result", exist_ok=True)
    
    # Arquivos de entrada e saída
    input_file = f"{base_path}/data/chat_original.txt"
    
    # Etapa 1: Processamento com ID
    id_clean = f"{base_path}/result/id_anon.txt"
    id_all = f"{base_path}/result/id_anon_all.txt"
    
    # Etapa 2: Processamento com Regex
    regex_clean = f"{base_path}/result/pre_processado.txt"
    regex_all = f"{base_path}/result/pre_processado_all.txt"
    
    # Etapa 3: Processamento com Apelidos
    apelidos_clean = f"{base_path}/result/apelidos_anon.txt"
    apelidos_all = f"{base_path}/result/apelidos_anon_all.txt"
    
    # Etapa 4: Processamento com BERT (resultado final)
    bert_clean = f"{base_path}/result/result_final.txt"
    bert_all = f"{base_path}/result/result_final_all.txt"
    
    # Carregar listas dos arquivos
    apelidos_lista = load_apelidos_from_file(f"{base_path}/data/apelidos_lista.txt")
    whitelist = load_whitelist_from_file(f"{base_path}/data/whitelist.txt")

    print("🚀 Iniciando pipeline de anonimização...")
    print(f"📝 Apelidos carregados: {', '.join(apelidos_lista) if apelidos_lista else 'Nenhum'}")
    print(f"🛡️  Palavras protegidas: {', '.join(whitelist) if whitelist else 'Nenhuma'}")
    print("=" * 60)
    
    # Verificar se o arquivo de entrada existe
    if not os.path.exists(input_file):
        print(f"❌ Erro: Arquivo {input_file} não encontrado!")
        print("💡 Uso:")
        print("   python main.py                    # Usa dados da pasta data/")
        print("   python main.py --example          # Usa dados de exemplo")
        return
    
    # Etapa 1: Processamento com ID
    print(f"📁 Etapa 1: {input_file} -> {id_clean} + {id_all}")
    process_with_id(input_file, id_clean, id_all, whitelist)
    print(f"✅ Etapa 1 concluída! Arquivos gerados:")
    print(f"   - {id_clean}")
    print(f"   - {id_all}")
    print("=" * 60)
    
    # Etapa 2: Processamento com Regex
    print(f"📁 Etapa 2: {id_clean} -> {regex_clean} + {regex_all}")
    process_with_regex(id_clean, regex_clean, regex_all, whitelist)
    print(f"✅ Etapa 2 concluída! Arquivos gerados:")
    print(f"   - {regex_clean}")
    print(f"   - {regex_all}")
    print("=" * 60)
    
    # Etapa 3: Processamento com Apelidos
    print(f"📁 Etapa 3: {regex_clean} -> {apelidos_clean} + {apelidos_all}")
    process_with_apelidos(regex_clean, apelidos_clean, apelidos_all, apelidos_lista, whitelist)
    print(f"✅ Etapa 3 concluída! Arquivos gerados:")
    print(f"   - {apelidos_clean}")
    print(f"   - {apelidos_all}")
    print("=" * 60)
    
    # Etapa 4: Processamento com BERT LOCAL
    print(f"📁 Etapa 4: {apelidos_clean} -> {bert_clean} + {bert_all}")
    bert_success = process_with_bert(apelidos_clean, bert_clean, bert_all, whitelist)
    
    if bert_success:
        print(f"✅ Etapa 4 concluída! Arquivos gerados:")
        print(f"   - {bert_clean}")
        print(f"   - {bert_all}")
    else:
        print("⚠️  Etapa 4 pulada (BERT LOCAL não disponível)")
    
    print("=" * 60)
    
    print("🎉 Pipeline de anonimização finalizado com sucesso!")
    print("\n📊 Resumo dos arquivos gerados:")
    print(f"   🆔 {id_clean} - Mensagens anonimizadas por ID")
    print(f"   🆔 {id_all} - Formato completo com ID")
    print(f"   🔧 {regex_clean} - Mensagens anonimizadas por regex")
    print(f"   🔧 {regex_all} - Formato completo com regex")
    print(f"   😎 {apelidos_clean} - Mensagens com apelidos substituídos")
    print(f"   😎 {apelidos_all} - Formato completo com apelidos")
    
    if bert_success:
        print(f"   🎯 {bert_clean} - Resultado final da anonimização ⭐")
        print(f"   🎯 {bert_all} - Formato completo final")
    else:
        print("   ⚠️  Arquivos finais não gerados (dependências BERT não disponíveis)")
    
    print("\n💡 Dica: Para testar com dados de exemplo, use:")
    print("   python main.py --example")

if __name__ == "__main__":
    main()
