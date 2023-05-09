import threading
import socket, sys, select
import dict_layer

HOST = ''
PORTA = 8001

dict = dict_layer.Dictionary()

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

    operation = str(clisock.recv(1024), encoding='utf-8')
    print("operation:\t", operation)
    if (operation == '1'):  # search
        arg = str(clisock.recv(1024), encoding='utf-8')
        print("arg:\t", arg)

        resp = str(dict.search(arg))
        clisock.send(bytes(resp, encoding='utf8'))

    elif (operation == '2'):  # insertion
        key = str(clisock.recv(1024), encoding='utf-8')
        value = str(clisock.recv(1024), encoding='utf-8')

        dict.insert(key, value)
        clisock.send(bytes("Inserção concluída", encoding='utf8'))

    elif (operation == '3'):  # removal

        passwd = str(clisock.recv(1024), encoding='utf-8')
        value = str(clisock.recv(1024), encoding='utf-8')

        if (passwd != 'silvana123'):
            res = "Senha incorreta"
        else:
            dict.delete(value)
            res = "Entrada {} removida.".format(value)

        clisock.send(bytes(res, encoding='utf8'))
    elif (operation == '4'):  #
        pass

    clisock.close()


def handle_stdin(sock):
    cmd = input()
    if cmd == 'exit':
        sys.exit()
        sock.close()


def main():
    clientes = [] # multiplos clientes serão atendido com uso de threads
    sock = server_init()
    print("Pronto para receber conexões, digite 'exit' para sair.")
    entradas = [sock, sys.stdin]
    while True:
        r, w, e = select.select(entradas, [], [])
        for pronto in r:
            if pronto == sock:
                clisock, addr = accept_connection(sock)
                nu_client = threading.Thread(target=handle_request, args=(clisock, addr))
                nu_client.start()
                clientes.append(nu_client)

            elif pronto == sys.stdin:
                handle_stdin(sock)

main()