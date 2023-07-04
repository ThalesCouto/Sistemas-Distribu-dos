from rpyc.utils import server
import threading
from broker import BrokerService
from dataclasses import dataclass

class Server:
    def __init__(self,host,porta) -> None:
        self.host: str = host
        self.porta: int = porta
        self.broker: BrokerService = BrokerService()  # Cria uma instancia do broker

        
    def monitorar_prompt(self):
        while True:
            user_input = input("Insira comando: ")
            if user_input.startswith("create_topic"):
                command_parts = user_input.split(" ")
                if len(command_parts) >= 2:
                    topic_name = command_parts[1]
                    broker = self.broker
                    broker.create_topic("admin", topic_name)
                    print(f"Topic '{topic_name}' criado.")
                else:
                    print("Comando inválido. Uso: create_topic <topic_name>")
            else:
                print("Comando inválido.")

    def iniciar(self):
        '''
        Inicia o servidor e a thread de monitoramento do terminal
        '''
        # Iniciar uma thread para monitorar o prompt do servidor
        thread_prompt = threading.Thread(target=self.monitorar_prompt)
        print(f"Servidor iniciado em {self.host}:{self.porta}")
        thread_prompt.start()

        server.ThreadedServer(
            BrokerService,
            hostname=self.host, port=self.porta,
            protocol_config={'allow_public_attrs': True}
        ).start()

def main():
    server_instance  = Server('localhost',8000)
    server_instance .iniciar()


if __name__ == '__main__':
    main()