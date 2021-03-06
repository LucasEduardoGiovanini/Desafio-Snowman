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

    def search_points(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT nome, categoria, latitude, longitude FROM tbPontoTuristico") # solicito todos os pontos turisticos
        resultado = cursor.fetchall()
        return resultado

    def check_existence_of_the_point(self, name: str):
        cursor = self.connection.cursor()
        arguments = (name,)
        cursor.execute("SELECT nome, categoria, latitude, longitude FROM tbPontoTuristico WHERE nome = %s", arguments)
        resultado = cursor.fetchone()
        if not resultado:
            return False
        else:
            return resultado

    def check_existence_of_category(self,categoria: str):
        cursor = self.connection.cursor()
        arguments=(categoria,)
        cursor.execute("SELECT cod FROM tbCategorias WHERE nome = %s",arguments)
        resultado = cursor.fetchone()
        if not resultado:
            return False
        else:
            return resultado

    def create_category(self,nome:str):
        cursor = self.connection.cursor()
        arguments = (nome,)
        cursor.execute("INSERT INTO  tbCategorias (nome) VALUES(%s)",arguments) #insiro a categoria
        self.connection.commit()
        cursor.execute("SELECT * FROM tbCategorias WHERE nome = %s",arguments)
        datas = cursor.fetchone()
        return datas

    def add_picture_spot(self,foto: str,nome: str, email:str):
        cursor = self.connection.cursor()
        arguments = (foto,nome,email)
        cursor.execute("INSERT INTO tbImagem_ponto(foto,nome,email) VALUES(%s,%s,%s)",arguments)
        self.connection.commit()
        cursor.execute("SELECT * FROM tbImagem_ponto where foto= %s and nome= %s and email= %s",arguments)
        datas = cursor.fetchone()
        return datas

    def create_tourist_point_and_upvote(self, nome: str, categoria: int, latitude: float, longitude: float, criador_ponto: str):
        cursor = self.connection.cursor()
        arguments_point=(nome,categoria,latitude,longitude,criador_ponto)
        cursor.execute("INSERT INTO tbPontoTuristico(nome,categoria,latitude,longitude,criador_ponto) VALUES (%s,%s,%s,%s,%s)",arguments_point)
        self.connection.commit()
        arguments_upvote=(nome,)
        cursor.execute("INSERT INTO tbUpvote(nome,quantidade_upvote) VALUES (%s,0)", arguments_upvote)
        self.connection.commit()
        cursor.execute("SELECT * FROM tbPontoTuristico where nome=%s and categoria=%s and latitude=%s and longitude=%s and criador_ponto=%s", arguments_point)
        datas = cursor.fetchone()
        return datas

    def check_who_favored_point(self,email:str,nome:str):
        cursor = self.connection.cursor();
        arguments = (email, nome)
        cursor.execute("SELECT nome FROM tbPontoFavoritado WHERE email=%s and nome=%s", arguments)
        result = cursor.fetchone()
        return result

    def create_comment_about_point(self, email:str, nome:str, descricao: str):

        cursor = self.connection.cursor()
        arguments = (email, nome, descricao)
        cursor.execute("INSERT INTO tbComentario (email,nome,descricao) VALUES (%s,%s,%s)",arguments)
        self.connection.commit()
        cursor.execute("SELECT * FROM tbComentario where email=%s and nome=%s and descricao=%s", arguments)
        datas = cursor.fetchone()
        return datas

    def search_comments(self,nome:str):
        cursor = self.connection.cursor()
        arguments = (nome,)
        cursor.execute("SELECT nome, descricao FROM tbComentario WHERE nome = %s",arguments)
        resultado = cursor.fetchall()
        return resultado

    def delete_picture(self,cod: int, email: str):
        cursor = self.connection.cursor()
        arguments = (cod,email)
        cursor.execute("DELETE FROM tbImagem_ponto WHERE cod = %s and email=%s", arguments)
        self.connection.commit()
        return True


    def search_picture(self,cod:int):
        cursor = self.connection.cursor()
        arguments = (cod)
        cursor.execute("SELECT foto FROM tbImagem_ponto WHERE cod = %s", arguments)
        resultado = cursor.fetchone()
        return resultado

    def register_upvote(self,nome:str):
        cursor = self.connection.cursor()
        arguments=(nome,)
        cursor.execute("SELECT quantidade_upvote from tbUpvote where nome = %s",arguments)
        value_of_upvote = cursor.fetchone()
        new_arguments = (value_of_upvote['quantidade_upvote']+1,nome) #como quero incrementar um upvote, passo o resultado como +1 na tupla
        cursor.execute("UPDATE tbUpvote SET quantidade_upvote = %s WHERE nome = %s",new_arguments)
        self.connection.commit()
        cursor.execute("SELECT * FROM tbUpvote where nome=%s",arguments)
        datas = cursor.fetchone()
        return datas




