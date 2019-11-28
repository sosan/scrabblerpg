from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask import session
from flask_bootstrap import Bootstrap
# from ModuloScrable.ManagerScrable import Manager_Scrable
from ModuloEnemigos.ManEnemigos import Enemigo
from ModuloEnemigos.ManEnemigos import Fases
# from main import manScrabble


def comprobarExistenciaSession():
    if ("poolLetras" not in session) or \
            ("letraspulsadas" not in session) or \
            ("correcto" not in session):
                return False
    else:
        return True
