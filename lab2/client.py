def get_input():
    filename = input('Insira o nome do arquivo a ser analisado:\t')
    keyword = input('Insira a palavra a ser contada:\t')
    return filename, keyword

def file_error(filename):
    print('arquivo {} não encontrado'.format(filename))

def display_count(filename, keyword, count):
    print('a palavra \"{}\" aparece {} vezes no arquivo {}'.format(keyword, count, filename))

#Até aqui é uma repetição da camada 1 da atividade 1

import socket

HOST = 'localhost'
PORTA = 8001

sock = socket.socket()
sock.connect((HOST, PORTA))

filename, keyword = get_input()

sock.send(bytes(filename, encoding='utf8'))
sock.recv(1024)
sock.send(bytes(keyword, encoding='utf8'))

ok = str(sock.recv(8), encoding='utf8')
sock.send(bytes(".", encoding='utf8'))

if ok == 'err':
    file_error(filename)

elif ok == 'ok':
    count = str(sock.recv(8), encoding='utf8')
    display_count(filename, keyword, count)

sock.close()