import json

class Dictionary():
    def __init__(self):

        with open('dict.json') as json_file:
            self.dict = json.load(json_file)

        print(self.dict)


    def load(self):
        '''load já está sendo feito no construtor'''
        pass

    def save(self):
        '''salva dict no disco'''
        json_dict = json.dumps(self.dict, indent=4)
        with open("dict.json", "w") as outfile:
            outfile.write(json_dict)

    def search(self, key):
        '''busca key no dicionario e retorna lista com os valores'''
        ret = self.dict.get(key)

        if(ret == None or ret == []):
            ret = "chave não encontrada"

        return ret


    def insert(self, key, value):
        if key not in self.dict:
            self.dict[key] = [value]
        else:
            self.dict[key].append(value)
        self.save()


    def delete(self, value):
        for k in self.dict:
            for i in self.dict[k]:
                if i == value:
                    self.dict[k].remove(i)


        self.save()


def generate_sample_dict():
    sample_dict = {
        "um": ["1", "01"],
        "dois": ["2", "4/2"],
        "três": ["3"],
        "quatro": ["4"],
        "cinco": ["5"]
    }
    json_dict = json.dumps(sample_dict, indent=4)
    with open("dict.json", "w") as outfile:
        outfile.write(json_dict)


generate_sample_dict()