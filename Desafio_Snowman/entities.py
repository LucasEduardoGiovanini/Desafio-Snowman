from flask import Flask, request, jsonify, app
import pymysql
from use_cases_turismo import *
from math import radians, cos, sin, asin, sqrt  # conteudo importado para encontrar pontos por km utilizando formula de haversine
import pymysql

entites = Flask(__name__)

app = Flask(__name__)



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


def convert_image(path): #pega a imagem e converte em binário para que possa ser inserida no banco
    with open(path,'rb') as file:
        binaryPhoto = file.read()
    return binaryPhoto

    

@app.route("/", methods=['POST'])
def inicial():#passo todos os meus testes


    return "Inicial", 400  # status code http


@app.route("/users/seealltouristspot", methods=['GET'])  #ver todos os pontos turisticos cadastrados
def ver_todos_pontos():
    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco #a variavel dispensavel n sera utilizada nessa def pois não necessitamos de seu retorno
    cursor[0].execute("SELECT nome, categoria, latitude, longitude FROM tbPontoTuristico")  # faço uma busca no banco pelo ponto turistico informado
    resultado = cursor[0].fetchall()  # comando que faz a busca por toda a informação da tabela
    if(not resultado):
        return jsonify({'message':'nao existem pontos cadastrados'}),404
    else:
        return jsonify({'message':resultado}), 200  # status code http


@app.route("/users/touristSpot5KM", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
def pontos_turisticos_5km():
    data = request.json  # solicita o json enviado pelo postman
    return pontos_turisticos_5km_logica(data)



@app.route("/users/touristSpotName", methods=['GET'])  # decorator para enviar um ponto turistico com base no nome
def pontos_turisticos_por_nome():
    data = request.json  # solicita o json enviado pelo postman
    return pontos_turisticos_por_nome_logica(data)


@app.route("/users/registertouristspot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
def registrar_ponto_turistico():
    data = request.json  # solicita o json enviado pelo postman
    return registrar_ponto_turistico_logica(data)


@app.route("/users/commenttouritspot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
def comentar_ponto_turistico():
    data = request.json  # solicita o json enviado pelo postman
    return comentar_ponto_turistico_logica(data)


@app.route("/users/seecommenttouritspot", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
def ver_comentarios_pontos_turisticos():
    data = request.json  # solicita o json enviado pelo postman
    return ver_comentario_ponto_turistico_logica(data)


@app.route("/users/favoriteaspot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
def favoritar_pontos_turisticos():
    data = request.json  # solicita o json enviado pelo postman
    return favoritar_ponto_turistico_logica(data)


@app.route("/users/seefavoritespot", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
def ver_ponto_favorito():
    data = request.json  # solicita o json enviado pelo postman
    return ver_ponto_turistico_logica(data)

@app.route("/users/removefavoritespot", methods=['DELETE'])  # rota para enviar um ponto turistico com base no nome
def remover_ponto_favoritado():
    data = request.json  # solicita o json enviado pelo postman
    return remover_ponto_favoritado_logica(data)

@app.route("/users/upvotespot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
def upvote_ponto():
    data = request.json  # solicita o json enviado pelo postman
    return upvote_ponto_logica(data)

@app.route("/users/seetouristspotcreatedbyme", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
def ver_pontos_criados_por_mim():
    data = request.json  # solicita o json enviado pelo postman
    return ver_pontos_criados_por_mim_logica(data)



@app.route("/users/createnewcategorie", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
def criar_nova_categoria():
    data = request.json  # solicita o json enviado pelo postman
    return criar_nova_categoria_logica(data)



"a camada de entidades contém as regras que tenham menos possibilidade de mudança"