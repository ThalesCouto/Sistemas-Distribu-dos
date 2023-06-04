from rpyc.utils import server

import dict_layer

if __name__ == '__main__':
    server.ThreadedServer(
        dict_layer.Dictionary,
        hostname='localhost', port=8001
    ).start()