import pymysql


class PontoTuristicoRepository:

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                user='root',
                                password='lucasgiovanini',
                                db='DBturismo',
                                cursorclass=pymysql.cursors.DictCursor)

    def get_ponto_turistico_by_name(self, name: str):
        cursor = self.connection.cursor()
        arguments = (name,)
        cursor.execute("SELECT nome, categoria, latitude, longitude FROM tbPontoTuristico WHERE nome = %s", arguments)
        resultado = cursor.fetchone()
        if not resultado:
            return False
        else:
            return resultado
        
    def checa_se_ponto_turistico_existe(self, name: str):
        cursor = self.connection.cursor()
        arguments = (name,)
        cursor.execute("SELECT EXISTS(SELECT nome, categoria, latitude, longitude FROM tbPontoTuristico WHERE nome = %s)", arguments)
        resultado = cursor.fetchone()
        if not resultado:
            return False
        else:
            return resultado