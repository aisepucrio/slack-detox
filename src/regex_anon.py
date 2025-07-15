import re

patterns = {
    "CPF": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
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

sender_pattern = r"\[\d{1,2}/\d{1,2}/\d{2,4}, .*?\] ([^:]+):"

def anonymize_message(msg):
    msg = msg.strip()
    anonymized = msg

    sender_match = re.search(sender_pattern, anonymized)
    if sender_match:
        nome = sender_match.group(1)
        anonymized = anonymized.replace(nome, "[PESSOA]")

    for label, pattern in patterns.items():
        matches = re.findall(pattern, anonymized, flags=re.IGNORECASE)
        for match in matches:
            anonymized = anonymized.replace(match, f"[{label.upper()}]")

    return anonymized

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