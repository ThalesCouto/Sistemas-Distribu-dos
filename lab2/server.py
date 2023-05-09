from dict_layer import Dictionary
import socket, sys, select


HOST = ''
PORTA = 8001

dict = Dictionary()

menu = "Dicinário distribuído!" \
       "1: Consulta;" \
       "2: Insere;" \
       "3: Remove;" \
       "4: Sair."
def server_init():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORTA))
    sock.listen(5)
    return sock

def accept_connection(sock):
    clisock, addr = sock.accept()
    print('Conectado com: ', addr)
    return clisock, addr

def handle_request(clisock, addr):
    start = str(clisock.recv(1024), encoding='utf-8')
    print(start) # <<<<<<<<<<<<<

    clisock.send(bytes(menu, encoding='utf8'))

    action = str(clisock.recv(1024), encoding='utf-8')
    print(action)



def handle_stdin(sock):
    cmd = input()
    if cmd == 'exit': sys.exit()
    sock.close()


def main():
    sock = server_init()
    print("Pronto para receber conexões")
    entradas = [sock, sys.stdin]
    while True:
        r, w, e = select.select(entradas, [], [])
        for pronto in r:
            if pronto == sock:
                clisock, addr = accept_connection(sock)
                handle_request(clisock, addr)
            elif pronto == sys.stdin:
                handle_stdin(sock)

main()