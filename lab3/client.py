import rpyc

menu = "Dicionário distribuído!\n" \
       "1: Busca;\n" \
       "2: Insere;\n" \
       "3: Remove;\n" \
       "4: Encerra.\n"


if __name__ == '__main__':
    conn = rpyc.connect('localhost', 8001)

    while True:
        operation = 0
        while (operation != '1' and operation != '2' and operation != '3' and operation != '4'):
            print(menu)
            operation = input("por favor, selecione uma opção [1-4]:")

        if (operation == '1'):  # search
            arg = input('chave a ser buscada:\t')

            resp = conn.root.search(arg)

        elif (operation == '2'):  # insertion
            arg1 = input('chave a ser inserida:\t')

            arg2 = input('valor a ser inserida:\t')

            resp = conn.root.insert(arg1, arg2)


        elif (operation == '3'):  # removal
            arg1 = input('Senha de admin:\t')

            arg2 = input('valor a ser removido:\t')

            resp = conn.root.delete(arg1, arg2)

        elif (operation == '4'):  # end
            conn.close()
            exit(0)

        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(resp)
        print('\n\n\n')

