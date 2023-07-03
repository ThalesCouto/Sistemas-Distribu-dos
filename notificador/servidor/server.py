from rpyc.utils import server
import threading
import broker
from dataclasses import dataclass

class Server:
    def __init__(self,host,porta) -> None:
        host: str = host
        porta: int = porta
        list_brokers: list = []
        
    def monitorar_prompt(self):
        #TODO integrar monitorar para linkar com a funcao de criar tópicos
        assert False

    def iniciar(self):
        '''
        Inicia o servidor e a thread de monitoramento do terminal
        '''
        # Iniciar uma thread para monitorar o prompt do servidor
        thread_prompt = threading.Thread(target=self.monitorar_prompt)
        print(f"Servidor iniciado em {self.host}:{self.porta}")
        thread_prompt.start()

        server.ThreadedServer(
            broker.BrokerService,
            hostname=self.host, port=self.porta,
            protocol_config={'allow_public_attrs': True}
        ).start()

def main():
    server = Server('localhost',8000)
    server.iniciar()


if __name__ == '__main__':
    main()