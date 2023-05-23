import socket

HOST = 'localhost'
PORTA = 8001



menu = "Dicionário distribuído!\n" \
       "1: Busca;\n" \
       "2: Insere;\n" \
       "3: Remove;\n" \
       "4: Encerra.\n"


while True:
    sock = socket.socket()
    sock.connect((HOST, PORTA))

    operation = 0
    while(operation != '1' and operation != '2' and operation != '3' and operation != '4'):
        print(menu)
        operation = input("por favor, selecione uma opção [1-4]:")

    sock.send(bytes(operation, encoding='utf8'))

    if(operation == '1'): # search
        arg = input('chave a ser buscada:\t')

        sock.send(bytes(arg, encoding='utf8'))

    elif(operation == '2'): # insertion
        arg1 = input('chave a ser inserida:\t')
        sock.send(bytes(arg1, encoding='utf8'))

        arg2 = input('valor a ser inserida:\t')
        sock.send(bytes(arg2, encoding='utf8'))

    elif(operation == '3'): # removal
        arg1 = input('Senha de admin:\t')
        sock.send(bytes(arg1, encoding='utf8'))

        arg2 = input('valor a ser removido:\t')
        sock.send(bytes(arg2, encoding='utf8'))

    elif(operation == '4'): # end
        sock.close()
        exit(0)


    result = str(sock.recv(1024), encoding='utf-8')


    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
          "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
          " >> Resultado da operação:\t", result,"\n\n")
    sock.close()
