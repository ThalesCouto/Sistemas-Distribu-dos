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

    # # Handshake

    def exposed_login(self, username: str) -> bool:
        assert False, "TO BE IMPLEMENTED"

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
        return self.list_of_topics.keys
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
            callback = topic.callbacks.get(user_id)
            if callback is not None:
                callback([content])

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
                topic.list_subscribers.append(id)#Alerta da inscrição
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


    def exposed_subscribe_all(self, id: UserId, callback: FnNotify) -> bool:
        '''
        Inscreve usuário em todos os tópicos existentes atualmente
            args:
                - id: Id do usuário
                - callback: Função de callback do cliente para notificar
        
        '''
        for topic in  BrokerService.topics.values:#(*)
            if id not in topic.list_subscribers:
                topic.list_subscribers.append(id)
                callback()#Alerta da inscrição
        #TODO decidir funcionamento do callback


    def exposed_unsubscribe_all(self, id: UserId) -> bool:
        '''
        Desinscreve usuário no interesse de um tópico
            args:
                - id: Id do usuário
                - topic: Tópico a ser públicado
        
        '''
        for topic in  BrokerService.topics.values:#(*)
            if id not in topic.list_subscribers:
                topic.list_subscribers.remove(id)
        #TODO decidir sobre Função de notify
