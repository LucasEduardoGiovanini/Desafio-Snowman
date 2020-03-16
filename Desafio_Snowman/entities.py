from flask import Flask, request, jsonify, app
import pymysql
from math import radians, cos, sin, asin, sqrt  # conteudo importado para encontrar pontos por km utilizando formula de haversine

import pymysql

entites = Flask(__name__)

def dbconnection():  # def responsável pela conexão com mysql
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='lucasgiovanini',
                                 db='DBturismo',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    return cursor, connection  # uso 2 returns pois algumas funções precisam fazer commit, e o commit só pode ser feito com o connection


def verifica_login(email_usuario,senha_usuario): #verifico se ele é um usuario cadastrado, se for, retorno um true e permito que ele use o banco
    cursor=dbconnection()
    cursor[0].execute("SELECT email,senha  FROM tbUsuario WHERE email = '{}' and senha='{}'".format(email_usuario, senha_usuario))
    resultado = cursor[0].fetchall()
    if (not resultado):
        return False
    else:
        return True

if __name__ == "__main__":
    entites.run()

"a camada de entidades contém as regras que tenham menos possibilidade de mudança"