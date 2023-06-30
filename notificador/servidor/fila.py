from content import Content

class Fila:
    id_global:int = 0 #ID global e único para filas
    
    def __init__(self):
        self.id = Fila.id_global # contador único associado ao tópico
        self.mensagens = [] #Lista de conteudos a serem distribuidos


    #TODO implementar forma de gerir para quais clientes já foi enviado o conteudo
    def adicionar_mensagem(self, mensagens: Content):
        '''
        Adiciona mensagem a ser enviada na fila
        '''
        self.id += 1
        self.mensagens.append([mensagens,self.id])
        return self.id

    def obter_mensagem(self):
        '''
        Retorna a mesnagem na primeira posição da fila
        '''
        try:
            return self.mensagens.pop(0)
        except IndexError  as e:
            pass
    
    def check_vazia(self):
        '''
        Checa se a fila ta vazia
        '''
        if self.mensagens:
            return True
        else: 
            return False