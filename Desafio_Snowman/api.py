from flask import Flask, request, jsonify, app
from use_cases_turismo import *
from functools import wraps
import auth
import adapter



import pymysql

app = Flask(__name__)



@app.route("/", methods=['POST'])
def inicial():
    return "Inicial", 200


@app.route("/users/login", methods=['GET'])
def login():
    data = request.json
    values = adapter.adapter_user_datas(data)
    return login_logica(*values)

@app.route("/users/register", methods=['POST'])
def register_user():
    data = request.json
    values = adapter.adapter_user_datas(data)
    return login_logica(*values)

@app.route("/users/seealltouristspot", methods=['GET'])
def ver_todos_pontos():
    return ver_todos_pontos_logica()

@app.route("/users/touristSpot5KM/", methods=['GET'])
@auth.token_required
def pontos_turisticos_5km(email_user):
    data = request.json
    values = adapter.adapter_coordenates_spot(data)
    return pontos_turisticos_5km_logica(*values,email_user)

@app.route("/users/touristSpotName", methods=['GET'])
@auth.token_required
def pontos_turisticos_por_nome(email_user):
    data = request.json
    values = adapter.adapter_name_spot(data)
    return pontos_turisticos_por_nome_logica(values,email_user)

@app.route("/users/registertouristspot", methods=['POST'])
@auth.token_required
def registrar_ponto_turistico(email_user):
    data = request.json
    values = adapter.adapter_tourist_spot(data)
    return registrar_ponto_turistico_logica(*values,email_user)

@app.route("/users/commenttouritspot", methods=['POST'])
@auth.token_required
def comentar_ponto_turistico(email_user):
    data = request.json
    values = adapter.adapter_comment_spot(data)
    return comentar_ponto_turistico_logica(*values,email_user)

@app.route("/users/seecommenttouritspot", methods=['GET'])
def ver_comentarios_pontos_turisticos():
    data = adapter.adapter_name_spot()
    return ver_comentario_ponto_turistico_logica(data)

@app.route("/users/addpicturespot", methods=['POST'])
@auth.token_required
def adicionar_foto_ponto(email_user):
    data = adapter.adapter_picture_spot()
    return adicionar_foto_ponto_logica(*data,email_user)

@app.route("/users/deletepicturespot", methods=['DELETE'])
@auth.token_required
def remover_foto_ponto(email_user):
    data=adapter.adapter_cod_picture_spot()
    return remover_foto_ponto_logica(data,email_user)

@app.route("/users/favoriteaspot", methods=['POST'])
@auth.token_required
def favoritar_ponto_turistico(email_user):
    data = adapter.adapter_name_spot()
    return favoritar_ponto_turistico_logica(data,email_user)

@app.route("/users/seefavoritespot", methods=['GET'])
@auth.token_required
def ver_ponto_turistico_favorito(email_user):
    return ver_ponto_turistico_favoritado_logica(email_user)

@app.route("/users/removefavoritespot", methods=['DELETE'])
@auth.token_required
def remover_ponto_favoritado(email_user):
    data = adapter.adapter_name_spot()
    return remover_ponto_favoritado_logica(data,email_user)

@app.route("/users/upvotespot", methods=['POST'])
@auth.token_required
def upvote_ponto(email_user):
    data = adapter.adapter_name_spot()
    return upvote_ponto_logica(data,email_user)

@app.route("/users/seetouristspotcreatedbyme", methods=['GET'])
@auth.token_required
def ver_pontos_criados_por_mim(email_user):
    return ver_pontos_criados_por_mim_logica(email_user)

@app.route("/users/createnewcategorie", methods=['POST'])
@auth.token_required
def criar_nova_categoria():
    data = adapter.adapter_category_spot()
    return criar_nova_categoria_logica(data)


