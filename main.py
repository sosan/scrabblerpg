# -*- coding: utf-8 -*-
"""

LA DB TIENE UN FICHERO SCRABLE_PALABRAS.SQL PARA INSERTAR LOS DATOS
EL FICHERO TIENE MAS DE 1.200.000 PALABRAS

"""


from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask import session
from flask_bootstrap import Bootstrap
from ModuloScrable.ManagerScrable import Manager_Scrable
from ModuloEnemigos.ManEnemigos import Enemigo
from ModuloEnemigos.ManEnemigos import Fases
from ModuloHelper.Helper import comprobarExistenciaSession

app = Flask(__name__)

app.secret_key = "secrett"
bootstrap = Bootstrap(app)

manScrabble = Manager_Scrable()
manScrabble.conectardb(host="localhost", user="jose",
                       password="jose", db="scrable")
app.jinja_env.add_extension("jinja2.ext.loopcontrols")


@app.route("/", methods=["GET"])
def home():
    manScrabble.nivelActual = 1
    return render_template("index.html")


@app.route("/", methods=["POST"])
def recibirDatosHome():
    return render_template("index.html")


@app.route("/juego", methods=["GET"])
def mostrarjuego():
    comprobarExistenciaSession()
    ronda = session["ronda"]
    enemigo = session["enemigos"][ronda]
    # vidaenemigo =

    return render_template("juego.html", letras=session["poolLetras"],
                           letraspulsadas=session["letraspulsadas"],
                           correcto=session["correcto"],
                           imagenenemigo=enemigo["imagen"],
                           vidaenemigo=enemigo["hp"],
                           vidaplayer=100

                           )


@app.route("/juego", methods=["POST"])
def recibirDatos_mostrarjuego():
    if "quitarletra" in request.form:
        letraspulsadas: list = session["letraspulsadas"]
        letrasPool: list = session["poolLetras"]
        try:
            posicion = int(request.form["quitarletra"])
        except ValueError:
            raise Exception("Valor no valido recibirdatos_mostrarjuego")
            # return redirect(url_for("mostrarjuego"))

        for i in range(0, len(letraspulsadas)):
            if i >= posicion:
                posicionPool = letraspulsadas[posicion][1]
                letrasPool[posicionPool][1] = False
                letraspulsadas.pop(posicion)

        manScrabble.comprobarExistePalabra(letraspulsadas)
        puntuacion = manScrabble.getPuntuacionLetrasPulsadas(
            letraspulsadas)

        session["puntuacion"] = puntuacion
        session["letraspulsadas"] = letraspulsadas
        session["letrasPool"] = letrasPool

        return redirect(url_for("mostrarjuego"))

    if "opcionletra" in request.form:

        posicion = int(request.form["opcionletra"])
        letraspulsadas: list = session["letraspulsadas"]
        letras: list = session["poolLetras"]

        for i in range(0, len(letras)):
            if i == posicion:
                letras[i][1] = True
                letraspulsadas.append([letras[i][0], i])
                break

        puntuacion = 0
        manScrabble.comprobarExistePalabra(letraspulsadas)
        puntuacion = manScrabble.getPuntuacionLetrasPulsadas(
            letraspulsadas)

        session["puntuacion"] = puntuacion
        session["letraspulsadas"] = letraspulsadas

        return redirect(url_for("mostrarjuego"))

    if "nuevaronda" in request.form:

        letraspulsadas: list = session["letraspulsadas"]
        if manScrabble.comprobarExistePalabra(letraspulsadas) == False:
            # TODO: sospechoso
            return redirect(url_for("iniciarjuego"))

        ronda = session["ronda"]
        vidaenemigo = session["enemigos"][ronda]["hp"]
        puntuacion = manScrabble.getPuntuacionLetrasPulsadas(
            letraspulsadas)
        vidaenemigo -= puntuacion
        session["enemigos"][ronda]["hp"] = vidaenemigo

        if vidaenemigo <= 0:
            ronda += 1
            if ronda >= len(session["enemigos"]):
                # te has cargado a todos los enemigos de esa fase
                ronda = 0
                session["fasecompletada"] = True
                manScrabble.subirnivelActual()
                session["nivelelegido"] = manScrabble.getnivelActual()
                return redirect(url_for("iniciarjuego"))
            # else:
            #     enemigo = session["enemigos"][ronda]

        session["puntuacion"] = puntuacion
        session["ronda"] = ronda

        return redirect(url_for("golpear"))  # mostrar animacion de holpear


@app.route("/nuevapartida", methods=["GET"])
def nuevapartida():

    session["poolLetras"] = manScrabble.getpoolLetras(tamanopool=15)
    session["letraspulsadas"] = []
    session["correcto"] = False
    session["puntuacion"] = 0
    session["fasecompletada"] = False

    return redirect(url_for("mostrarjuego"))


@app.route("/mapa", methods=["GET"])
def iniciarjuego():

    # # if session["fasecompletada"] == True:
    # #     pass
    # else:

    nivelPlayer = manScrabble.getnivelActual()
    session["letraspulsadas"] = []
    session["correcto"] = False
    session["puntuacion"] = 0
    session["nivelelegido"] = nivelPlayer
    session["ronda"] = 0

    return render_template("mapa.html", nivel=nivelPlayer)


@app.route("/mapa", methods=["POST"])
def recibirdatos_mapa():
    # if comprobarExistenciaSession() == False:
    #         # TODO: sospechoso
    #         return redirect(url_for("iniciarjuego"))

    if "lucharnivel" in request.form:
        nivelelegido = int(request.form["lucharnivel"])

        if "nivelelegido" not in session and "" not in session:
            pass
        else:
            pass

        if nivelelegido == manScrabble.getnivelActual():
            # nuevapartida()
            # enemigos = manScrabble.managerfases.fases["fase{0}".format(
            #     nivelelegido)]

            enemigos = manScrabble.managerfases.tojson(nivelelegido)
            session["enemigos"] = enemigos

            return redirect("nuevapartida")

    if "subir" in request.form:
        manScrabble.subirnivelActual()

    return redirect(url_for("iniciarjuego"))


@app.route("/golpear", methods=["GET"])
def golpear():
    return redirect(url_for("nuevapartida"))


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
