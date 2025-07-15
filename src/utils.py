from typing import List

def load_apelidos_from_file(file_path: str) -> List[str]:
    """
    Carrega a lista de apelidos de um arquivo de texto
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            apelidos = [line.strip() for line in f if line.strip()]
        return apelidos
    except FileNotFoundError:
        print(f"⚠️  Arquivo de apelidos não encontrado: {file_path}")
        return []
