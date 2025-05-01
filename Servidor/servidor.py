import socket
import os

def iniciar_servidor():
    host = '0.0.0.0'
    porta = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((host, porta))
        servidor.listen(1)
        print("Aguardando conexão...")

        conexao, endereco = servidor.accept()
        with conexao:
            print(f"Conectado por {endereco}")
            dados = conexao.recv(1024 * 1024)  # até 1MB
            if b'||' in dados:
                nome_arquivo, conteudo = dados.split(b'||', 1)
                nome_arquivo = nome_arquivo.decode()
                caminho_destino = os.path.join(os.path.dirname(__file__), nome_arquivo)
                with open(caminho_destino, 'wb') as f:
                    f.write(conteudo)
                print(f"Arquivo '{nome_arquivo}' recebido e salvo com sucesso.")

if __name__ == "__main__":
    iniciar_servidor()
