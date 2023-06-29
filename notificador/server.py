from rpyc.utils import server

import broker

if __name__ == '__main__':
    server.ThreadedServer(
        broker.BrokerService,
        hostname='localhost', port=8001
    ).start()