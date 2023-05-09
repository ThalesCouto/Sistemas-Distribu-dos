import json

class Dictionary():
  def __init__(self):

    with open('dict.json') as json_file:
        self.dict = json.load(json_file)

    print(self.dict)


    def load():
        '''load já está sendo feito no construtor'''
        pass

    def save():
        '''salva dict no disco'''
        json_dict = json.dumps(self.dict, indent=4)
        with open("dict.json", "w") as outfile:
            outfile.write(json_dict)

    def search(key):
        '''busca key no dicionario e retorna lista com os valores'''
        return self.dict[key]


    def insert(key, value):
        if key not in self.dict:
            self.dict[key] = [value]
        else:
            self.dict[key].append([value])


    def delet(psswd, key):
        while(psswd != 'silvana123'):
            pass # pede senha novamente

        pass # deleta entrada no dict


def generate_sample_dict():
    sample_dict = {
        "um": ["1", "01"],
        "dois": ["2"],
        "três": ["3"],
        "quatro": ["4"],
        "cinco": ["5"]
    }
    json_dict = json.dumps(sample_dict, indent=4)
    with open("dict.json", "w") as outfile:
        outfile.write(json_dict)


generate_sample_dict()