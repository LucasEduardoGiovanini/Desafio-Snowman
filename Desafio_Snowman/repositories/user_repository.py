import pymysql
from auth import  *
class UserRepostory:

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                user='root',
                                password='lucasgiovanini',
                                db='DBturismo',
                                cursorclass=pymysql.cursors.DictCursor)

    def user_exists(self,email:str): #checo apenas se o email dele consta no banco
        cursor = self.connection.cursor()
        arguments = (email,)

        cursor.execute("SELECT email FROM tbUsuario WHERE email=%s",arguments)
        result=cursor.fetchone()
        return result


    def validate_user_email(self, email:str): #se o email é valido, retornamos a senha

        cursor = self.connection.cursor() #recebo o cursor
        arguments = (email,)
        cursor.execute("SELECT email,senha  FROM tbUsuario WHERE email = %s ",arguments)
        resultado = cursor.fetchone() #caso tenha um valor, é válido,por isso o fetchone
        return resultado['senha']


    def register_user(self, email:str, password:str):
        cursor=self.connection.cursor()
        user_already_registered=self.user_exists(email)

        if(user_already_registered):
            return False
        else:
            arguments = (email,password)
            cursor.execute("INSERT INTO tbUsuario (email,senha) VALUES(%s,%s)",arguments)
            self.connection.commit()
            return True



    def favorite_tourist_spot(self,email:str, nome:str):
        cursor = self.connection.cursor()
        arguments = (email,nome)
        cursor.execute("SELECT nome FROM tbPontoFavoritado WHERE email = %s and nome=%s",arguments) #confiro se já não foi favoritado
        verification = cursor.fetchall()
        if(not verification):
            cursor.execute("INSERT INTO tbPontoFavoritado(email,nome) VALUES (%s,%s)",arguments)
            self.connection.commit()
            return True #o ponto não existia e cadastramos ele
        else:
            return False #o ponto exisita então não foi cadastrado

    def search_favorited_spots(self,email:str):
        cursor = self.connection.cursor()
        arguments=(email,)
        cursor.execute("SELECT nome FROM tbPontoFavoritado WHERE email=%s",arguments)
        result = cursor.fetchall()
        return result

    def remove_favorited_tourist_spot(self,email:str,nome:str):
        cursor = self.connection.cursor();
        arguments=(email,nome)
        cursor.execute("DELETE FROM tbPontoFavoritado WHERE email=%s and nome=%s",arguments)
        self.connection.commit()

    def check_who_favored_point(self,email:str,nome:str):
        cursor = self.connection.cursor();
        arguments = (email, nome)
        cursor.execute("SELECT nome FROM tbPontoFavoritado WHERE email=%s and nome=%s", arguments)
        result = cursor.fetchone()
        return result

    def search_tourist_points_created_by_user(self,email:str):
        cursor = self.connection.cursor()
        arguments = (email,)
        cursor.execute("SELECT nome,categoria,latitude,longitude FROM tbPontoTuristico WHERE criador_ponto= %s",arguments)
        result = cursor.fetchall()
        return result

