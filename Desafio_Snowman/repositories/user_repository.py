import pymysql

class UserRepostory:

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                user='root',
                                password='lucasgiovanini',
                                db='DBturismo',
                                cursorclass=pymysql.cursors.DictCursor)

    def verify_email(self,email:str):
        cursor = self.connection.cursor()
        arguments = (email,)
        cursor.execute("SELECT senha FROM tbUsuario WHERE email=%s", arguments)
        result = cursor.fetchone()
        return True if result else False

    def get_encrypt_password(self,email:str):
        cursor = self.connection.cursor()
        arguments = (email,)
        cursor.execute("SELECT senha FROM tbUsuario WHERE email=%s",arguments)
        result=cursor.fetchone()
        return result['senha'] if result!=None else False


    def insert_user(self, email:str, password:str):
        cursor=self.connection.cursor()
        arguments = (email, password)
        cursor.execute("INSERT INTO tbUsuario (email,senha) VALUES(%s,%s)", arguments)
        self.connection.commit()
        cursor.execute("SELECT email FROM tbUsuario where email=%s", arguments[0])
        datas = cursor.fetchone()
        return datas


    def select_all_favored_spots_from_user(self,email:str):
        cursor = self.connection.cursor()
        arguments = (email,)
        cursor.execute("SELECT nome FROM tbPontoFavoritado WHERE email = %s",arguments)  # confiro se já não foi favoritado
        spots = cursor.fetchall()
        return spots



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
        return True


    def search_tourist_points_created_by_user(self,email:str):
        cursor = self.connection.cursor()
        arguments = (email,)
        cursor.execute("SELECT nome,categoria,latitude,longitude FROM tbPontoTuristico WHERE criador_ponto= %s",arguments)
        result = cursor.fetchall()
        return result

