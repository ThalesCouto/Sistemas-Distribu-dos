# echo lado ativo

import socket

HOST = 'localhost'
PORTA = 5000

sock = socket.socket()
sock.connect((HOST, PORTA))

print("Envie 'quit' para encerrar")

msg = ''
while msg != 'quit':
    msg = input('envia mensagem: ')
    sock.send(bytes(msg, encoding='utf-8'))

sock.close()
