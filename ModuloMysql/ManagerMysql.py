import pymysql
import random


class Manager_MysqlDB:
    def __init__(self):
        self.conexion = None
        self.cursor = None

    def conectarDB(self, host, user, password, db, port=3306):
        self.conexion = pymysql.connect(host=host, port=port, user=user, password=password, database=db)
        self.cursor = self.conexion.cursor()

    def getPalabras(self, tamanoinicial, tamanofinal):

        sql = """
        select count(palabra)
        from palabras
        """
        self.cursor.execute(sql)
        longitud = self.cursor.fetchall()[0][0]

        n1 = 1
        n2 = 1
        n3 = 1

        n1 = random.randint(1, longitud)
        n2 = random.randint(1, longitud)
        if n2 == n1:
            n2 = random.randint(1, longitud)

        n3 = random.randint(1, longitud)
        if n3 == n1 or n3 == n2:
            n3 = random.randint(1, longitud)

        sql = """
        select palabras.palabra
        from palabras
        where palabras.id={0} or palabras.id={1} or palabras.id={2}
        limit 3;
        """.format(n1, n2, n3)

        # sql = """
        # select palabras.palabra
        # from palabras
        # where length(palabra) > {0} and length(palabra) < {1}
        # order by rand()
        # limit 3;
        # """.format(tamanoinicial, tamanofinal)

        self.conexion.query('SET GLOBAL connect_timeout=6000')
        self.cursor.execute(sql)
        datos = self.cursor.fetchall()

        return datos[0][0].upper(), datos[1][0].upper(), datos[2][0].upper()

    def existPalabra(self, palabra):
        sql = """
        select palabras.palabra
        from palabras
        where palabras.palabra='{0}'
        limit 1;
                """.format(palabra)

        self.cursor.execute(sql)
        datos = self.cursor.fetchall()
        if len(datos) >= 1:
            if datos[0][0] == palabra:
                return True
            else:
                return False
        else:
            return False
