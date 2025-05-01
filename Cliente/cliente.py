import socket
import sys
import os

def enviar_arquivo(ip, arquivo):
    if not os.path.exists(arquivo):
        print(f"Arquivo {arquivo} não encontrado.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((ip, 12345))  # Conecta ao servidor na porta 12345
        with open(arquivo, 'rb') as f:
            dados = f.read()
            cliente.sendall(arquivo.encode() + b'||' + dados)  # Nome do arquivo e conteúdo
        print("Arquivo enviado com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 Cliente.py <ip-do-servidor> <arquivo>")
        sys.exit(1)

    ip = sys.argv[1]
    arquivo = sys.argv[2]
    enviar_arquivo(ip, arquivo)
