from flask import Flask, request, jsonify, app
from use_cases_turismo import *

from math import radians, cos, sin, asin, sqrt  # conteudo importado para encontrar pontos por km utilizando formula de haversine

import pymysql

entites = Flask(__name__)

app = Flask(__name__)

if __name__ == "__main__":
    entites.run()



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
    '''imagem = request.files['imagem'] #exemplo de como ler uma imagem que vem pelo form-data do postman
    path = imagem.read()
    cadastrar_imagem_ponto(path)'''
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

@app.route("/users/addpicturespot", methods=['POST'])
def add_picture_tourist_spot():
    data = request.json
    return add_picture_tourist_spot_logica(data)


@app.route("/users/detepicturespot", methods=['DELETE'])
def remove_picture_tourist_spot_():
    data=request.json
    return remove_picture_tourist_spot_logica(data)

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



@app.route("/users/test", methods=['POST'])
def testing_save_image():
    data = request.json
    return testing_save_image_logic(data)