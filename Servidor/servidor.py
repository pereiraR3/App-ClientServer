import socket
import struct
import os   

# --- Configurações do Servidor ---
# Endereço IP para escutar.
# 'localhost' (ou '127.0.0.1') só aceita conexões da mesma máquina.
# '0.0.0.0' aceita conexões de qualquer interface de rede da máquina.
HOST = 'localhost'
PORT = 9999         # Porta para escutar
BUFFER_SIZE = 4096  # Tamanho do buffer para receber dados 

# --- Função auxiliar para garantir o recebimento de N bytes ---
def recv_all(sock, n):
    """ Recebe exatamente 'n' bytes do socket 'sock'. """
    data = bytearray()
    while len(data) < n:
        try:
            packet = sock.recv(n - len(data))
            if not packet: 
                return None
            data.extend(packet)
        except socket.error as e:
            print(f"[!] Erro no socket ao tentar receber dados: {e}")
            return None 
    return bytes(data)

# --- Função Principal do Servidor ---
def start_server():
    # 1. Criar o socket do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[*] Socket TCP criado.")

    try:
        # 2. Vincular o socket ao endereço e porta especificados
        server_socket.bind((HOST, PORT))
        print(f"[*] Socket vinculado ao endereço {HOST}:{PORT}")

        # 3. Colocar o socket em modo de escuta
        server_socket.listen(1)
        print(f"[*] Servidor escutando na porta {PORT}...")
        print("[*] Aguardando conexões de clientes...")

        # 4. Loop principal para aceitar conexões continuamente
        while True:
            client_socket = None 
            addr = None
            try:
                # 5. Aceitar uma nova conexão
                client_socket, addr = server_socket.accept()
                print(f"[+] Conexão aceita de {addr[0]}:{addr[1]}")

                # --- Protocolo de Recebimento ---
                # a) Receber o tamanho do nome do arquivo (4 bytes, unsigned int, big-endian)
                packed_filename_len = recv_all(client_socket, 4)
                if not packed_filename_len:
                    print(f"[-] Cliente {addr} desconectou antes de enviar o tamanho do nome.")
                    continue

                filename_len = struct.unpack('>I', packed_filename_len)[0]

                # b) Receber o nome do arquivo (bytes)
                filename_bytes = recv_all(client_socket, filename_len)
                if not filename_bytes:
                    print(f"[-] Cliente {addr} desconectou antes de enviar o nome do arquivo.")
                    continue

                # c) Decodificar o nome do arquivo (usando UTF-8)
                filename = filename_bytes.decode('utf-8', errors='replace')
                filename = os.path.basename(filename)
                print(f"[*] Recebendo arquivo: '{filename}' de {addr}")

                # d) Abrir o arquivo localmente para escrita em modo binário ('wb')
                try:
                    with open(filename, 'wb') as f:
                        print(f"[*] Iniciando recebimento e salvamento do arquivo '{filename}'...")
                        # e) Loop para receber os dados do arquivo em chunks
                        while True:
                            chunk = client_socket.recv(BUFFER_SIZE)
                            if not chunk:
                                break
                            f.write(chunk)
                    print(f"[+] Arquivo '{filename}' recebido e salvo com sucesso de {addr}.")

                except IOError as e:
                    print(f"[!] Erro de I/O ao salvar o arquivo '{filename}': {e}")
                except Exception as e:
                    print(f"[!] Erro inesperado ao processar/salvar o arquivo '{filename}': {e}")

            except socket.error as e:
                print(f"[!] Erro de Socket na conexão com {addr if addr else 'cliente desconhecido'}: {e}")
            except struct.error as e:
                 print(f"[!] Erro ao desempacotar dados (struct) de {addr if addr else 'cliente desconhecido'}: {e}")
            except Exception as e:
                 print(f"[!] Erro inesperado durante a conexão com {addr if addr else 'cliente desconhecido'}: {e}")
            finally:
                # 6. Fechar o socket DO CLIENTE após o término da comunicação ou erro
                if client_socket:
                    print(f"[*] Fechando conexão com {addr}.")
                    client_socket.close()

    except KeyboardInterrupt:
        print("\n[*] Servidor interrompido pelo usuário (Ctrl+C).")
    except socket.error as e:
        print(f"[!] Erro de Socket no servidor principal: {e}")
    except Exception as e:
        print(f"[!] Erro fatal inesperado no servidor: {e}")
    finally:
        # 7. Fechar o socket principal do servidor ao finalizar
        print("[*] Fechando o socket do servidor.")
        server_socket.close()

if __name__ == "__main__":
    start_server()