from content import Content

class Fila:
    id_global:int = 0 #ID global e único para filas
    
    def __init__(self):
        self.mensagens = [] #Lista de conteudos a serem distribuidos


    def adicionar_mensagem(self, mensagens: Content):
        '''
        Adiciona mensagem a ser enviada na fila
        '''
        self.mensagens.append(mensagens)

    def obter_mensagem(self):
        '''
        Retorna a mesnagem na primeira posição da fila
        '''
        try:
            return self.mensagens[0]
        except IndexError  as e:
            pass
    
    def obter_todas_mensagem(self):
        '''
        Retorna todas mesnagem na fila
        '''
        return self.mensagens
        
    def limpar_mensagem(self):
        '''
        Limpa a mesnagem na primeira posição da fila
        '''
        try:
            return self.mensagens.pop(0)
        except IndexError as e:
            pass

    def limpar_fila(self):
        '''
        Limpa a fila inteira
        '''
        self.mensagens = []

    def check_populada(self):
        '''
        Checa se a fila ta vazia
        '''
        if self.mensagens:
            return True
        else: 
            return False