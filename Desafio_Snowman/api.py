from flask import Flask, request, jsonify, app
from use_cases_turismo import *
from functools import wraps


import pymysql

api = Flask(__name__)

app = Flask(__name__)

if __name__ == "__main__":
    api.run()



@app.route("/", methods=['POST'])
def inicial():#passo todos os meus testes


    return "Inicial", 200  # status code http


@app.route("/users/login", methods=['GET'])
def login():
    data = request.json
    return login_logica(data)

@app.route("/users/register", methods=['POST'])  #ver todos os pontos turisticos cadastrados
def register_user():
    data = request.json
    return registrar_usuario_logica(data)


@app.route("/users/seealltouristspot", methods=['GET'])  #ver todos os pontos turisticos cadastrados
def ver_todos_pontos():
    return ver_todos_pontos_logica()



@app.route("/users/touristSpot5KM/", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
@token_required
def pontos_turisticos_5km():

    data = request.json  # solicita o json enviado pelo postman
    return pontos_turisticos_5km_logica(data)




@app.route("/users/touristSpotName", methods=['GET'])  # decorator para enviar um ponto turistico com base no nome
@token_required
def pontos_turisticos_por_nome():

    data = request.json  # solicita o json enviado pelo postman
    return pontos_turisticos_por_nome_logica(data)


@app.route("/users/registertouristspot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
@token_required
def registrar_ponto_turistico():
    data = request.json  # solicita o json enviado pelo postman


    return registrar_ponto_turistico_logica(data)


@app.route("/users/commenttouritspot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
@token_required
def comentar_ponto_turistico():
    data = request.json  # solicita o json enviado pelo postman
    return comentar_ponto_turistico_logica(data)


@app.route("/users/seecommenttouritspot", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
def ver_comentarios_pontos_turisticos():
    data = request.json  # solicita o json enviado pelo postman
    return ver_comentario_ponto_turistico_logica(data)

@app.route("/users/addpicturespot", methods=['POST'])
@token_required
def adicionar_foto_ponto():
    data = request.json
    return adicionar_foto_ponto_logica(data)


@app.route("/users/deletepicturespot", methods=['DELETE'])
@token_required
def remover_foto_ponto():
    data=request.json
    return remover_foto_ponto_logica(data)

@app.route("/users/favoriteaspot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
@token_required
def favoritar_ponto_turistico():
    data = request.json  # solicita o json enviado pelo postman
    return favoritar_ponto_turistico_logica(data)


@app.route("/users/seefavoritespot", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
@token_required
def ver_ponto_turistico_favorito():
    return ver_ponto_turistico_favoritado_logica()

@app.route("/users/removefavoritespot", methods=['DELETE'])  # rota para enviar um ponto turistico com base no nome
@token_required
def remover_ponto_favoritado():
    data = request.json  # solicita o json enviado pelo postman
    return remover_ponto_favoritado_logica(data)

@app.route("/users/upvotespot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
@token_required
def upvote_ponto():
    data = request.json  # solicita o json enviado pelo postman
    return upvote_ponto_logica(data)

@app.route("/users/seetouristspotcreatedbyme", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
@token_required
def ver_pontos_criados_por_mim():

    return ver_pontos_criados_por_mim_logica()



@app.route("/users/createnewcategorie", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
@token_required
def criar_nova_categoria():
    data = request.json  # solicita o json enviado pelo postman
    return criar_nova_categoria_logica(data)


