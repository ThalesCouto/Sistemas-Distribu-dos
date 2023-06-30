from __future__ import annotations
import rpyc
from topic import Topic
from user import UserInfo
from content import Content
from typing import Callable, Optional, Tuple, TypeAlias
from dataclasses import dataclass
from fila import Fila
import rpyc # type: ignore

UserId: TypeAlias = int

# Aqui pode ser uma função que recebe apenas um Tuple[Topic, Content]
# ou seja:
# FnNotify: TypeAlias = Callable[[Tuple[Topic, Content]], None]
FnNotify: TypeAlias = Callable[[list[Tuple[Topic, Content]]], None]

class BrokerService(rpyc.Service): # type: ignore
    topics: dict = {} #Chave-valor de tópicos, associa um nome ao objeto tópico com aquele nome
    
    # Não é exposed porque só o "admin" tem acesso
    def create_topic(self, id: UserId, topicname: str) -> Topic:
        '''
        Cria novo tópico e adiciona a lista de tópicos
        '''
        new_topic = Topic(topicname,len(self.topics))
        self.list_of_topics[topicname] = new_topic # Adiciona tópico ao dicionário de tópicos associado ao nome
        return new_topic

    # Handshake

    def exposed_login(self, username: str) -> Optional[UserId]:
        assert False, "TO BE IMPLEMENTED"

    # Query operations

    def exposed_get_user_info(self, id: UserId) -> UserInfo:
        assert False, "TO BE IMPLEMENTED"

    def exposed_list_topics(self) -> list[Topic]:
        '''
        Lista tóicos disponíveis
        '''
        return self.list_of_topics.keys
    # Publisher operations

    def exposed_publish(self, id: UserId, topicname: str, data: str) -> None:
        '''
        Publica novo conteudo em referido tópico
            args:
                - id: Id do usuário
                - topic: Tópico a ser públicado
                - data: Conteudo da publicação
        '''
        topic = self.list_of_topics[topicname]
        content = Content(id,topic,data)
        topic.fila.adicionar_mensagem(content) #Adiciona mensagem na fila daquele tópico
        #TODO implementar método para limpar conteudo após certa data(data limite)
        #TODO implementar gestão de para quem a mensagem já foi enviada

    # Subscriber operations

    def exposed_subscribe_to(self, id: UserId, topicname: str, callback: FnNotify) -> Optional[FnNotify]:
        '''
        Inscreve usuário no interesse de um tópico
            args:
                - id: Id do usuário
                - topic: Tópico a ser públicado
                - callback: Função de callback do cliente para notificar
        
        '''
        if topicname in self.list_of_topics.keys:
            topic = self.list_of_topics[topicname]
            if id not in topic.list_subscribers:
                topic.list_subscribers.append(id)#Alerta da inscrição
                callback()
        else:
            callback()#Alerta que não se inscreveu
        #TODO decidir funcionamento do callback
        
    def exposed_unsubscribe_to(self, id: UserId, topicname: str) -> Optional[FnNotify]:
        '''
        Desinscreve usuário no interesse de um tópico
            args:
                - id: Id do usuário
                - topic: Tópico a ser públicado
        
        '''
        if topicname in self.list_of_topics.keys:
            topic = self.list_of_topics[topicname]
            if id in topic.list_subscribers:
                topic.list_subscribers.remove(id)
        #TODO decidir sobre Função de notify


    def exposed_subscribe_all(self, id: UserId, callback: FnNotify) -> Optional[FnNotify]:
        '''
        Inscreve usuário em todos os tópicos existentes atualmente
            args:
                - id: Id do usuário
                - callback: Função de callback do cliente para notificar
        
        '''
        for topic in  self.list_of_topics.values:
            if id not in topic.list_subscribers:
                topic.list_subscribers.append(id)
                callback()#Alerta da inscrição
        #TODO decidir funcionamento do callback


    def exposed_unsubscribe_all(self, id: UserId) -> FnNotify:
        '''
        Desinscreve usuário no interesse de um tópico
            args:
                - id: Id do usuário
                - topic: Tópico a ser públicado
        
        '''
        for topic in  self.list_of_topics.values:
            if id not in topic.list_subscribers:
                topic.list_subscribers.remove(id)
        #TODO decidir sobre Função de notify
