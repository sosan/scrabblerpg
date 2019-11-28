import pymysql
from ModuloMysql.ManagerMysql import Manager_MysqlDB
from ModuloEnemigos.ManEnemigos import Fases
from ModuloEnemigos.ManEnemigos import Enemigo
from flask import session
import random
import string


class Manager_Scrable:
    def __init__(self):
        self.letrasPuntuacion = {
            "W": 2, "Y": 2, "Ñ": 2, "Z": 2,
            "H": 2, "J": 2, "X": 2, "K": 2,

            "Q": 1, "E": 1, "R": 1, "T": 1,
            "U": 1, "I": 1, "O": 1, "P": 1,
            "A": 1, "S": 1, "F": 1, "G": 1,
            "L": 1, "C": 1, "V": 1, "B": 1,
            "N": 1, "M": 1, "D": 1
        }
        self.usuarios = []
        # self.poolLetras = []
        # self.matrizMapa = [[], []]
        self.db = Manager_MysqlDB()
        self.managerfases = Fases()
        self.nivelActual = 1
        # self.manenemigos = ManagerEnemigo()

    def generate_csrf_token(self, tamano):
        if '_csrf_token' not in session:
            passswordrnd = ''.join([random.choice(string.ascii_uppercase + string.digits) for i in range(tamano)])
            session['_csrf_token'] = passswordrnd

        return session['_csrf_token']

    def conectardb(self, host, user, password, db):
        self.db.conectarDB(host=host, user=user, password=password, db=db)

    def getpoolLetras(self, tamanopool):
        palabras = self.db.getPalabras(4, 10)
        print(palabras)
        conjuntounicopalabras = set(palabras[0] + palabras[1] + palabras[2])
        palabras = list(conjuntounicopalabras)
        if len(palabras) < tamanopool:
            vocales = ["A", "E", "I", "O", "U"]
            for i in range(len(palabras), tamanopool):
                posicionrndom = random.randrange(0, len(vocales))
                palabras.append(vocales[posicionrndom])

        palabrasdesordenadas = random.sample(palabras, len(palabras))
        palabras = []
        for i in range(0, len(palabrasdesordenadas)):
            palabras.append([palabrasdesordenadas[i], False])

        return palabras

    def existPalabra(self, listaPalabras):

        palabra = []
        for i in range(0, len(listaPalabras)):
            palabra.append(listaPalabras[i][0])

        palabracompleta = "".join(palabra)

        data = self.db.existPalabra(palabracompleta.lower())
        return data

    def subirnivelActual(self):
        self.nivelActual += 1
        if self.nivelActual >= 13:
            self.nivelActual = 1

    def getnivelActual(self):
        return self.nivelActual

    def getpuntuacion(self, letra):
        puntuacion = self.letrasPuntuacion[letra]
        return puntuacion
    
    def comprobarExistePalabra(self, letraspulsadas: list):
        
        if len(letraspulsadas) > 1:
            correcto = False
            if self.existPalabra(letraspulsadas) == True:
                print("existe por tanto sumamos puntuacion")
                correcto = True

            session["correcto"] = correcto
            return correcto


    def getPuntuacionLetrasPulsadas(self, letraspulsadas:list):
        puntuacion = 0
        for i in range(0, len(letraspulsadas)):
                p = self.getpuntuacion(letraspulsadas[i][0])
                puntuacion += p

        puntuacion = puntuacion * len(letraspulsadas)
        return puntuacion
