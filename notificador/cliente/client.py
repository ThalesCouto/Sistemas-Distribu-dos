import os
import rpyc

# Função de callback para receber notificações de novas mensagens
def callback(novas_mensagens):
    for mensagem in novas_mensagens:
        print(f"Nova mensagem no tópico {mensagem.topic}")
        print(f"Autor: {mensagem.author}")
        print(f"{mensagem.data}")
        print('##### FIM #####')

HOST = 'localhost'
PORT = 8000

# Conectar ao serviço do broker
def iniciaConexao():
    conn = rpyc.connect(HOST, PORT)
    return conn

# Fazer login como usuário
# id_usuario = "usuario1"
def login():
    user = str(input("Insira seu user: "))
    isLogged = conn.root.login(user, callback)
    if(isLogged):
        return user
    else:
        return ''

def printOpcoes():
    global escolha

    os.system('clear')
    print(f"Bem vindo, {user}!\n\n")
    print("O que deseja fazer?")
    print("0 - Sair")
    print("1 - Listar tópicos")
    print("2 - Inscrever-se em um tópico")
    print("3 - Desinscrever-se de um tópico")
    print("4 - Publicar")
    # print("5 - Exibir mensagens")
    try:
        escolha = int(input("\nDigite o número da sua escolha: "))
    except:
        print('Erro lendo escolha. Digite novamente')
        escolha = int(input("\nDigite o número da sua escolha: "))

def voltaMenu():
    global escolha

    input('Aperte uma tecla p/ voltar ao menu')
    escolha = -1

def listaTopicos():
    topicos = conn.root.list_topics()
    print("Tópicos disponíveis:")
    if len(topicos) == 0: print('Nenhum topico cadastrado nesse servidor :(')
    else:
        print(f'Encontrados {len(topicos)} topico(s) nesse servidor:')
        for i, topico in enumerate(topicos):
            print(f'{i} - {topico}')

    voltaMenu()

def inscreveTopico():
    topico_interesse = str(input('Qual seu topico de interesse? '))
    inscricao_sucesso = conn.root.subscribe_to(user, topico_interesse)
    if inscricao_sucesso:
        print(f"Inscrição no tópico {topico_interesse} realizada com sucesso")
    else:
        print(f"Falha ao se inscrever no tópico {topico_interesse}")

    voltaMenu()

def desinscreveTopico():
    topico = str(input("De qual topico deseja se desinscrever? "))
    if(conn.root.unsubscribe_to(user, topico)):
        print(f"Desinscrito do topico {topico} com sucesso!")
    else:
        print(f"Ocorreu um erro. Verifique se o topico {topico} existe nesse servidor")

    voltaMenu()

def publicaTopico():
    topico_pub = str(input('Em qual topico deseja publicar? '))
    mensagem = str(input('Escreva sua mensagem: '))
    publicacao_sucesso = conn.root.publish(user, topico_pub, mensagem)
    if publicacao_sucesso:
        print("Mensagem publicada com sucesso")
    else:
        print("Falha ao publicar mensagem")

    voltaMenu()

def printMensagens():
    # TODO
    print('TODO')

    voltaMenu()

def iniciaRotina():
    global escolha

    while True:
        if escolha == -1: printOpcoes()
        if escolha == 0: break
        
        # Listar os tópicos disponíveis
        if escolha == 1: listaTopicos()

        # Inscrever-se em um tópico
        if escolha == 2: inscreveTopico()

        # Desinscrever-se de um tópico
        if escolha == 3: desinscreveTopico()

        # Publicar uma mensagem em um tópico
        if escolha == 4: publicaTopico()

        # # Imprime as mensagens
        # if escolha == 5: printMensagens()

        else:
            print("Opcao nao Reconhecida")
            escolha == -1

def main():
    global conn
    global user
    global escolha
    
    user = ''
    conn = iniciaConexao()
    bgsrv = rpyc.BgServingThread(conn)
    while user == '':
        user = login()
        if user == '':
            print('Usuário nao encontrado.')
    input('')
    escolha = -1
    iniciaRotina()
    bgsrv.stop()
    conn.close()

if __name__ == '__main__':
    main()