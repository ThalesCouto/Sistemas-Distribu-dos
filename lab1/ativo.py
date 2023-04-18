# echo lado ativo

import socket

HOST = 'localhost'
PORTA = 5000

sock = socket.socket()
sock.connect((HOST, PORTA))

print("Envie 'fim' para encerrar")

msg = ''
while msg != 'fim':
    msg = input('envia mensagem: ')
    sock.send(bytes(msg, encoding='utf-8'))

sock.close()
