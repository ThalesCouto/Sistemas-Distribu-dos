
import rpyc

# Função de callback para receber notificações de novas mensagens
def callback(novas_mensagens):
    for mensagem in novas_mensagens:
        print(f"Nova mensagem no tópico {mensagem.topic}: {mensagem.data}")

# Conectar ao serviço do broker
conn = rpyc.connect("localhost", 8000)

# Fazer login como usuário
id_usuario = "usuario1"
conn.root.login(id_usuario, callback)

# Listar os tópicos disponíveis
topicos = conn.root.list_topics()
print("Tópicos disponíveis:")
for topico in topicos:
    print(topico)

# Inscrever-se em um tópico
topico_interesse = "esportes"
inscricao_sucesso = conn.root.subscribe_to(id_usuario, topico_interesse)
if inscricao_sucesso:
    print(f"Inscrição no tópico {topico_interesse} realizada com sucesso")
else:
    print(f"Falha ao se inscrever no tópico {topico_interesse}")

# Publicar uma mensagem em um tópico
mensagem = "Nova mensagem sobre esportes"
publicacao_sucesso = conn.root.publish(id_usuario, topico_interesse, mensagem)
if publicacao_sucesso:
    print("Mensagem publicada com sucesso")
else:
    print("Falha ao publicar mensagem")

# Fazer logout e desconectar do serviço do broker
conn.close()
