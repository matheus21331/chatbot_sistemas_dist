from logging import exception
import socket 
import select
import errno
import sys

header_length = 10
IP = "127.0.0.1"
PORT  = 1234

nome_usuario = input("Nome do Usuario: ")
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((IP, PORT))
cliente_socket.setblocking(False)

nome_usuario_decode = nome_usuario.encode('utf-8')
nome_usuario_header = f"{len(nome_usuario_decode):<{header_length}}".encode("utf-8")
cliente_socket.send(nome_usuario_header + nome_usuario_decode)

while True:
    mensagem = input(f"{nome_usuario} > ")
    

    if mensagem:
        mensagem = mensagem.encode('utf-8')
        mensagem_header = f"{len(mensagem):<{header_length}}".encode('utf-8')
        cliente_socket.send(mensagem_header + mensagem)
    try: 
        while True:
            nome_usuario_header = cliente_socket.recv(header_length)
            if not len(nome_usuario_header):
                print("Conexão fechada pelo server")
                sys.exit()

            nome_usuario_tamanho = int(nome_usuario_header.decode('utf-8').strip())
            nome_usuario = cliente_socket.recv(nome_usuario_tamanho).decode('utf-8')

            mensagem_header = cliente_socket.recv(header_length)
            mensagem_tamanho = int(mensagem_header.decode('utf-8').strip())
            mensagem = cliente_socket.recv(mensagem_tamanho).decode('utf-8')

            print(f"{nome_usuario} > {mensagem}")
    
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Erro de leitura', str(e))
            sys.exit()
        continue

    except Exception as e:
        print("Erro genérico", str(e))
        sys.exit()