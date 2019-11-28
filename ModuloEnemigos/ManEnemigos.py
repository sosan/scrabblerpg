import json


class Enemigo:
    def __init__(self, hp=0, ataque=0, imagen=0):
        self.hp = hp
        self.ataque = ataque
        self.imagen = imagen

    def quitarvida(self, ataque):
        self.hp -= ataque


class Fases:
    def __init__(self):
        
        self.fases = \
        {
            "fase1": [Enemigo(100, 100, 1), Enemigo(100, 100, 2), Enemigo(100, 100, 3), Enemigo(100, 100, 1)],
            "fase2": [Enemigo(110, 110, 1), Enemigo(110, 110, 2), Enemigo(110, 110, 3), Enemigo(110, 110, 1)],
            "fase3": [Enemigo(110, 110, 1), Enemigo(110, 110, 2), Enemigo(110, 110, 3), Enemigo(110, 110, 1)],
            "fase4": [Enemigo(110, 110, 1), Enemigo(110, 110, 2), Enemigo(110, 110, 3), Enemigo(110, 110, 1)],
            "fase5": [Enemigo(110, 110, 1), Enemigo(110, 110, 2), Enemigo(110, 110, 3), Enemigo(110, 110, 1)],
            "fase6": [Enemigo(110, 110, 1), Enemigo(110, 110, 2), Enemigo(110, 110, 3), Enemigo(110, 110, 1)],
            "fase7": [Enemigo(110, 110, 1), Enemigo(110, 110, 2), Enemigo(110, 110, 3), Enemigo(110, 110, 1)],
            "fase8": [Enemigo(110, 110, 1), Enemigo(110, 110, 2), Enemigo(110, 110, 3), Enemigo(110, 110, 1)],
            "fase9": [Enemigo(110, 110, 1), Enemigo(110, 110, 2), Enemigo(110, 110, 3), Enemigo(110, 110, 1)],
            "fase10": [Enemigo(110, 110, 1), Enemigo(110, 110, 2), Enemigo(110, 110, 3), Enemigo(110, 110, 1)],
            "fase11": [Enemigo(110, 110, 1), Enemigo(110, 110, 2), Enemigo(110, 110, 3), Enemigo(110, 110, 1)],
            "fase12": [Enemigo(200, 200, 1), Enemigo(200, 200, 2), Enemigo(200, 200, 3), Enemigo(200, 110, 1)]
            
        }
        
    def tojson(self, fase):
        
        
        enemigostemp = self.fases["fase{0}".format(fase)]
        lista = []
        for i in range(0, len(enemigostemp)):
            elementoclase:Enemigo = enemigostemp[i]
            dic = {"hp": elementoclase.hp,
                    "ataque": elementoclase.ataque,
                    "imagen": elementoclase.imagen
                    }
            lista.append(dic)
        
        return lista
       
