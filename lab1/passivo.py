# echo lado passivo

import socket

HOST = ''
PORTA = 5000
sock = socket.socket()
sock.bind((HOST, PORTA))
sock.listen(5)

novoSock, endereco = sock.accept()
print('Conectado com: {} \npronto para repetir'.format(endereco))

while True:
    msg = novoSock.recv(1024)
    if not msg:
        break
    else:
        print(str(msg, encoding='utf-8'))
    if str(msg, encoding='utf-8') != 'quit':
        novoSock.send(msg)
    else:
        break

novoSock.close()
sock.close()
