from email.base64mime import header_length
from ipaddress import ip_address
import socket
import select
import random
import re

header_length = 10
IP = "127.0.0.1"
PORT  = 1234

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

servidor_socket.bind((IP, PORT))

servidor_socket.listen()

sockets_lista = [servidor_socket]

clientes = {}
mensagens = ["A cada minuto, cerca de 72 horas de conteúdo são enviadas ao site de vídeos Youtube.", "Estima-se que, a cada ano, o monte Everest cresça 4 milímetros.", "Durante o fenômeno Superlua, calcula-se que o diâmetro lunar possa aumentar em até 14%.", "Há uma lâmpada que permanece ligada continuamente há mais de 113 anos na cidade de Livermore, na Califórnia.", "Em média, um adulto respira 550 litros de oxigênio puro diariamente.", "A maior palavra da língua portuguesa refere-se a uma doença causada pela respiração de cinzas vulcânicas: pneumoultramicroscopicossilicovulcanoconiótico.", "Mais de 10% de toda a biodiversidade do mundo é encontrada no continente australiano.", "A Rússia é o maior país do mundo, ocupando cerca de 10% de toda a terra do planeta.", "O menor país do mundo é o Vaticano, com cerca de 800 habitantes oficiais.", "A parte mais profunda do oceano chega a 11 mil metros.", "O corpo humano tem mais de 96 mil km de vasos sanguíneos.", "O recorde de voo de uma galinha é de 13 segundos.", "Uma pulga pode saltar até 350 vezes sua altura."]

def receber_mensagem(cliente_socket): 
    try:
        mensagem_header = cliente_socket.recv(header_length)

        if not len(mensagem_header):
            return False
        
        mensagem_tamanho = int(mensagem_header.decode('utf-8').strip())
        return {"header": mensagem_header, "data": cliente_socket.recv(mensagem_tamanho)}

    except:
        return False


while True:
    ler_sockets, _, exception_sockets = select.select(sockets_lista, [], sockets_lista)

    for notificado_socket in ler_sockets:
        if notificado_socket == servidor_socket:
            cliente_socket, cliente_endereco = servidor_socket.accept()

            usuario = receber_mensagem(cliente_socket)
            if usuario is False:
                continue

            sockets_lista.append(cliente_socket)

            clientes[cliente_socket] = usuario

            print(f"Conexão aceita de {cliente_endereco[0]}:{cliente_endereco[1]} Usuario: {usuario['data'].decode('utf-8')}")
        else:
            mensagem = receber_mensagem(notificado_socket)

            if mensagem is False:
                print(f"Conexão terminada de {clientes[notificado_socket]['data'].decode('utf-8')}")
                sockets_lista.remove(notificado_socket)
                del clientes[notificado_socket]
                continue
            usuario = clientes[notificado_socket]
            numeroIndex = random.randint(0,3)  


            print(f"Mensagem recebida de {usuario['data'].decode('utf-8')}: {mensagem['data'].decode('utf-8')}")
            
            for cliente_socket in clientes:
                if cliente_socket != notificado_socket:
                    cliente_socket.send(usuario['header'] + usuario['data'] + mensagem['header'] + mensagem['data'])
            if "curiosidade" in mensagem['data'].decode('utf-8').lower() or "curioso" in mensagem['data'].decode('utf-8').lower() or "entediado" in mensagem['data'].decode('utf-8').lower() or "triste" in mensagem['data'].decode('utf-8').lower() or "conte" in mensagem['data'].decode('utf-8').lower(): 
                print(f"Você sabia que ... {mensagens[numeroIndex]}")
            
  
    for notificado_socket in exception_sockets:
        sockets_lista.remove(notificado_socket)
        del clientes[notificado_socket]