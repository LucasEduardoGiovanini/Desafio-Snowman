from flask import Flask, request, jsonify, app
from use_cases_turismo import *
from functools import wraps
import auth
from auth import Token
import adapter



import pymysql

app = Flask(__name__)



@app.route("/", methods=['POST'])
def inicial():
    return "Inicial", 200


@app.route("/users/login", methods=['GET'])
def login():
    data = adapter.adapter_user_datas()
    return login_logica(*data)

@app.route("/users/register", methods=['POST'])
def register_user():
    data = adapter.adapter_user_datas()
    return login_logica(*data)

@app.route("/users/seealltouristspot", methods=['GET'])
def ver_todos_pontos():
    return ver_todos_pontos_logica()

@app.route("/users/touristSpot5KM/", methods=['GET'])
@Token.token_required
def pontos_turisticos_5km():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.Token().decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']
    data = adapter.adapter_coordenates_spot()
    return pontos_turisticos_5km_logica(*data,email_user)

@app.route("/users/touristSpotName", methods=['GET'])
@Token.token_required
def pontos_turisticos_por_nome():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.Token().decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']
    data = adapter.adapter_name_spot()
    return pontos_turisticos_por_nome_logica(data,email_user)

@app.route("/users/registertouristspot", methods=['POST'])
@Token.token_required
def registrar_ponto_turistico():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.Token().decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']

    data = adapter.adapter_tourist_spot()
    return registrar_ponto_turistico_logica(*data,email_user)

@app.route("/users/commenttouritspot", methods=['POST'])
@Token.token_required
def comentar_ponto_turistico():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.Token().decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']
    data = adapter.adapter_comment_spot()
    return comentar_ponto_turistico_logica(*data,email_user)

@app.route("/users/seecommenttouritspot", methods=['GET'])
def ver_comentarios_pontos_turisticos():
    data = request.json
    nome_ponto = data.get('nome')
    return ver_comentario_ponto_turistico_logica(nome_ponto)

@app.route("/users/addpicturespot", methods=['POST'])
@Token.token_required
def adicionar_foto_ponto():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.Token().decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']
    data = request.json
    nome_ponto = data.get('nome')
    foto_ponto = data.get('foto')
    return adicionar_foto_ponto_logica(nome_ponto,foto_ponto,email_user)

@app.route("/users/deletepicturespot", methods=['DELETE'])
@Token.token_required
def remover_foto_ponto():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.Token().decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']
    data=request.json
    cod_foto = data.get('cod_foto')
    return remover_foto_ponto_logica(cod_foto,email_user)

@app.route("/users/favoriteaspot", methods=['POST'])
@Token.token_required
def favoritar_ponto_turistico():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.Token().decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']
    data = request.json
    nome_ponto = data.get('nome')
    return favoritar_ponto_turistico_logica(nome_ponto,email_user)

@app.route("/users/seefavoritespot", methods=['GET'])
@Token.token_required
def ver_ponto_turistico_favorito():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.Token().decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']
    return ver_ponto_turistico_favoritado_logica(email_user)

@app.route("/users/removefavoritespot", methods=['DELETE'])
@Token.token_required
def remover_ponto_favoritado():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.Token().decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']
    data = request.json
    nome_ponto = data.get('nome')
    return remover_ponto_favoritado_logica(nome_ponto,email_user)

@app.route("/users/upvotespot", methods=['POST'])
@Token.token_required
def upvote_ponto():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.Token().decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']
    data = request.json
    nome_ponto = data.get('nome')
    return upvote_ponto_logica(nome_ponto,email_user)

@app.route("/users/seetouristspotcreatedbyme", methods=['GET'])
@Token.token_required
def ver_pontos_criados_por_mim():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.Token().decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']
    data = request.json
    return ver_pontos_criados_por_mim_logica(email_user)

@app.route("/users/createnewcategorie", methods=['POST'])
@Token.token_required
def criar_nova_categoria():
    data = request.json
    nome_categoria = data.get('categoria')
    return criar_nova_categoria_logica(nome_categoria)


