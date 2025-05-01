import socket
import sys     
import os      
import struct  

# Porta do servidor (deve ser a mesma definida no servidor.py)
SERVER_PORT = 9999
BUFFER_SIZE = 4096 # Tamanho do buffer para ler/enviar o arquivo (4KB)

# --- Função Principal do Cliente ---
def send_file(server_ip, filepath):
    # 1. Validar o arquivo de entrada
    if not os.path.exists(filepath):
        print(f"[!] Erro: O arquivo '{filepath}' não foi encontrado.")
        return
    if not os.path.isfile(filepath):
        print(f"[!] Erro: O caminho '{filepath}' não é um arquivo válido.")
        return

    # Extrair apenas o nome base do arquivo 
    filename = os.path.basename(filepath)
    if not filename:
         print(f"[!] Erro: Não foi possível extrair um nome de arquivo válido de '{filepath}'")
         return

    # 2. Criar o socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[*] Socket TCP do cliente criado.")

    try:
        # 3. Conectar ao servidor
        print(f"[*] Tentando conectar ao servidor {server_ip} na porta {SERVER_PORT}...")
        client_socket.connect((server_ip, SERVER_PORT))
        print(f"[+] Conexão com o servidor estabelecida.")

        # --- Protocolo de Envio (deve casar com o do servidor) ---
        # a) Enviar o tamanho do nome do arquivo
        filename_bytes = filename.encode('utf-8')
        filename_len = len(filename_bytes)
        packed_filename_len = struct.pack('>I', filename_len)

        client_socket.sendall(packed_filename_len)
        print(f"[*] Tamanho do nome do arquivo enviado ({filename_len} bytes).")

        # b) Enviar o nome do arquivo
        client_socket.sendall(filename_bytes)
        print(f"[*] Nome do arquivo '{filename}' enviado.")

        # c) Enviar o conteúdo do arquivo
        print(f"[*] Iniciando envio do conteúdo de '{filepath}'...")
        try:
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(BUFFER_SIZE)
                    if not chunk:
                        break
                    client_socket.sendall(chunk)
            print(f"[+] Conteúdo do arquivo '{filename}' enviado com sucesso.")

        except FileNotFoundError:
             print(f"[!] Erro: Arquivo '{filepath}' não encontrado durante a leitura.")
        except IOError as e:
            print(f"[!] Erro de I/O ao ler o arquivo '{filepath}': {e}")
        except Exception as e:
            print(f"[!] Erro inesperado ao ler ou enviar o arquivo: {e}")

    except socket.gaierror as e:
        print(f"[!] Erro de endereço: Não foi possível resolver o host '{server_ip}'. Verifique o IP/nome.")
        print(f"    Detalhe: {e}")
    except ConnectionRefusedError:
        print(f"[!] Erro: A conexão foi recusada. Verifique se o servidor está rodando em {server_ip}:{SERVER_PORT}.")
    except socket.error as e:
        print(f"[!] Erro de Socket durante a conexão/envio: {e}")
    except Exception as e:
        print(f"[!] Um erro inesperado ocorreu no cliente: {e}")
    finally:
        # 4. Fechar o socket do cliente, independentemente de sucesso ou erro
        print("[*] Fechando o socket do cliente.")
        client_socket.close()

if __name__ == "__main__":
    # 1. Verificar se o número correto de argumentos foi passado
    if len(sys.argv) != 3:
        print("\nErro: Número incorreto de argumentos.")
        print("Uso correto: python cliente.py <ip-do-servidor> <caminho-do-arquivo>")
        print("Exemplo:   python cliente.py localhost meu_documento.txt")
        print("           python cliente.py 192.168.1.10 /home/user/foto.jpg\n")
        sys.exit(1)

    # 2. Pegar os argumentos da linha de comando
    server_address = sys.argv[1]
    file_to_send = sys.argv[2]

    # 3. Chamar a função principal para enviar o arquivo
    send_file(server_address, file_to_send)