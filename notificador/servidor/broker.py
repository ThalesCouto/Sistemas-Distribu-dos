from __future__ import annotations
import rpyc
from topic import Topic
from user import UserInfo
from content import Content
from typing import Callable, Optional, Tuple, TypeAlias
from dataclasses import dataclass
from fila import Fila
import rpyc # type: ignore

UserId: TypeAlias = str


# Aqui pode ser uma função que recebe apenas um Tuple[Topic, Content]
# ou seja:
# FnNotify: TypeAlias = Callable[[Tuple[Topic, Content]], None]
FnNotify: TypeAlias = Callable[[list[Content]], None]

class BrokerService(rpyc.Service): # type: ignore
    topics: dict = {} #Chave-valor de tópicos, associa um nome ao objeto tópico com aquele nome
    users: dict = {} #Chave-valor de usuários, associa um nome ao objeto tópico com aquele nome
    # Não é exposed porque só o "admin" tem acesso
    def create_topic(self, id: UserId, topicname: str) -> Topic:
        '''
        Cria novo tópico e adiciona a lista de tópicos
        '''
        new_topic = Topic(topicname,len(BrokerService.topics)) #############IMPORTANTE!ESTOU USANDO como variável estática porque 
                                                                #não sei como funciona o compartilhamento de objetos entre as threads nesse modulo. 
                                                                # se eles forem capaz de enxergar o mesmo objeto de BrokerService, substituir por self.
                                                                ################### esses locais estão marcados com #(*)

        BrokerService.topics[topicname] = new_topic # Adiciona tópico ao dicionário de tópicos associado ao nome
        return new_topic

    def send_queued_messages(self,topic: Topic, subscriber_id: UserId) -> None:
        callback = topic.callbacks.get(subscriber_id)
        if callback is not None:
            queued_messages = BrokerService.users[subscriber_id].fila #Recupera mensagens na fila do usuário
            callback(queued_messages) #Chama o callback daquele tópico
            BrokerService.users[subscriber_id].limpar_fila() #Esvazia a fila

    # # Handshake

    def exposed_login(self, username: str) -> bool:
        #Função de login
        self.userid = username #Seta o nome de usuário dessa instancia do broker pra ser o do usuário

        if username in BrokerService.users.keys:
            BrokerService.users[username].online = True #Modifica status para online
        else:
            BrokerService.users[username] = UserInfo(username) #Cria novo usuário
            BrokerService.users[username].online = True 
        # Depois do usuário logar, envia as mensagens na fila
        user_id = username
        for topic in BrokerService.topics.values:
            if user_id in topic.list_subscribers:
                self.send_queued_messages(topic,user_id) #Envia as mensagens em fila

        return True

    #Sobrescreve a função de desconexão do RPyC
    def on_disconnect(self):
        disconnected_user_id = self.userid #Recupera o id do usuário que disconectou
        if disconnected_user_id in BrokerService.users:
            BrokerService.users[disconnected_user_id].online = False #Marca como offline
    # Query operations

    def exposed_get_user_info(self, id: UserId) -> UserInfo:
        if  id in  BrokerService.users.keys:#(*)
            user = BrokerService.users[id]#(*)
            return user
        else:
            return None #TODO Decidir o que retornar em caso de inexistencia

    def exposed_list_topics(self) -> list[Topic]:
        '''
        Lista tóicos disponíveis
        '''
        return BrokerService.topics.keys
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
                                callback = topic.callbacks.get(user_id)
                                if callback is not None:
                                    callback([content])
                            else: #Usuário deslogado, adiciona na fila
                                BrokerService.users[user_id].fila.append(content)

        return True
    # Subscriber operations

    def exposed_subscribe_to(self, id: UserId, topicname: str, callback: FnNotify) -> bool:
        '''
        Inscreve usuário no interesse de um tópico
            args:
                - id: Id do usuário
                - topic: Tópico a ser públicado
                - callback: Função de callback do cliente para notificar
        
        '''
        if topicname in BrokerService.topics.keys:#(*)
            topic = BrokerService.topics[topicname]#(*)
            if id not in topic.list_subscribers:
                topic.list_subscribers.append(id)
                topic.callbacks[id] = callback

    def exposed_unsubscribe_to(self, id: UserId, topicname: str) -> bool:
        '''
        Desinscreve usuário no interesse de um tópico
            args:
                - id: Id do usuário
                - topic: Tópico a ser públicado
        
        '''
        if topicname in BrokerService.topics.keys:#(*)
            topic = BrokerService.topics[topicname]#(*)
            if id in topic.list_subscribers:
                topic.list_subscribers.remove(id)
                del topic.callbacks[id]
