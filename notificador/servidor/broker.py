from __future__ import annotations
import rpyc
from topic import Topic
from user import UserInfo
from content import Content
from typing import Callable, TYPE_CHECKING, TypeAlias
from dataclasses import dataclass
from fila import Fila
import rpyc # type: ignore
import sys

IS_NEW_PYTHON: bool = sys.version_info >= (3, 8)
if IS_NEW_PYTHON:
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias
    

UserId: TypeAlias = str


# Aqui pode ser uma função que recebe apenas um Tuple[Topic, Content]
# ou seja:
# FnNotify: TypeAlias = Callable[[Tuple[Topic, Content]], None]
if IS_NEW_PYTHON:
    FnNotify: TypeAlias = Callable[[list[Content]], None]
elif not TYPE_CHECKING:
    FnNotify: TypeAlias = Callable
    
class BrokerService(rpyc.Service): # type: ignore
    topics: dict = {} #Chave-valor de tópicos, associa um nome ao objeto tópico com aquele nome
    users: dict = {} #Chave-valor de usuários, associa um nome ao objeto tópico com aquele nome
    # Não é exposed porque só o "admin" tem acesso
    def create_topic(self, topicname: str) -> Topic:
        '''
        Cria novo tópico e adiciona a lista de tópicos
        '''
        new_topic = Topic(topicname,len(BrokerService.topics)) #############IMPORTANTE!ESTOU USANDO como variável estática porque 
                                                                #não sei como funciona o compartilhamento de objetos entre as threads nesse modulo. 
                                                                # se eles forem capaz de enxergar o mesmo objeto de BrokerService, substituir por self.
                                                                ################### esses locais estão marcados com #(*)

        BrokerService.topics[topicname] = new_topic # Adiciona tópico ao dicionário de tópicos associado ao nome
        return new_topic

    def send_queued_messages(self, subscriber_id: UserId) -> None:
        '''
        Envia todas as mensagens na fila de um usuário
        '''
        user = BrokerService.users[subscriber_id]
        callback = user.callback
        if callback is not None:
            queued_messages = BrokerService.users[subscriber_id].fila #Recupera mensagens na fila do usuário
            callback(queued_messages) #Chama o callback daquele tópico
            BrokerService.users[subscriber_id].limpar_fila() #Esvazia a fila

    # # Handshake

    def exposed_login(self, id: UserId, callback: FnNotify) -> bool:
        '''
        Função para realização de login e definição de função calback
        '''
        #Função de login
        self.userid = id #Seta o nome de usuário dessa instancia do broker pra ser o do usuário
        #checa se o usuário já esta cadastrado
        if id in BrokerService.users.keys():
            BrokerService.users[id].online = True #Modifica status para online
            BrokerService.users[id].callback = callback
            user_id = id
            # Depois do usuário logar, envia as mensagens na fila
            self.send_queued_messages(user_id) #Envia as mensagens em fila
        else:
            BrokerService.users[id] = UserInfo(id,callback) #Cria novo usuário
            BrokerService.users[id].online = True 

        return True

    #Sobrescreve a função de desconexão do RPyC
    def on_disconnect(self, _):
        '''
        Sobrescreve a função de disconect, quando o usuário interrompe a conexão pega o id e altera o status de online
        '''
        disconnected_user_id = self.userid #Recupera o id do usuário que disconectou
        print(f'Usuário {disconnected_user_id} saiu do servidor')
        if disconnected_user_id in BrokerService.users:
            BrokerService.users[disconnected_user_id].online = False #Marca como offline
    # Query operations

    def exposed_get_user_info(self, id: UserId) -> UserInfo:
        if id in  BrokerService.users.keys():#(*)
            user = BrokerService.users[id]#(*)
            return user
        else:
            return None #TODO Decidir o que retornar em caso de inexistencia

    def exposed_list_topics(self) -> list[str]:
        '''
        Lista tóicos disponíveis
        '''
        return BrokerService.topics.keys()
    # Publisher operations

    def exposed_publish(self, id: UserId, topicname: str, data: str) -> bool:
        '''
        Publica novo conteudo em referido tópico
            args:
                - id: Id do usuário
                - topic: Tópico a ser públicado
                - data: Conteudo da publicação
        '''
        topic = BrokerService.topics.get(topicname)
        if topic is None:
            return False

        content = Content(id, topic, data)
        for user_id in topic.list_subscribers:
            if user_id in BrokerService.users:
                user = BrokerService.users[user_id]
                if user.online:
                    # Usuário ta logado, notifica agora
                    callback = user.callback
                    if callback is not None:
                        callback([content])
                else: #Usuário deslogado, adiciona na fila
                    BrokerService.users[user_id].fila.append(content)

        return True
    # Subscriber operations

    def exposed_subscribe_to(self, id: UserId, topicname: str) -> bool:
        '''
        Inscreve usuário no interesse de um tópico
            args:
                - id: Id do usuário
                - topic: Tópico a ser públicado
                - callback: Função de callback do cliente para notificar
        
        '''
        if topicname in BrokerService.topics.keys():#(*)
            topic = BrokerService.topics[topicname]#(*)
            if id not in topic.list_subscribers:
                topic.list_subscribers.append(id)

                return True 
        return False  

    def exposed_unsubscribe_to(self, id: UserId, topicname: str) -> bool:
        '''
        Desinscreve usuário no interesse de um tópico
            args:
                - id: Id do usuário
                - topic: Tópico a ser públicado
        
        '''
        if topicname in BrokerService.topics.keys():#(*)
            topic = BrokerService.topics[topicname]#(*)
            if id in topic.list_subscribers:
                topic.list_subscribers.remove(id)
                return True 
        return False  

