from flask import Flask, request, jsonify, app
from use_cases_turismo import *
from functools import wraps
import auth
import adapter
import presenters



import pymysql

app = Flask(__name__)



@app.route("/", methods=['POST'])
def inicial():
    return "Inicial", 200


@app.route("/users/login", methods=['GET'])
def login():
    data = request.json
    values = adapter.adapter_user_datas(data)
    return login_logica(*values,presenters.user_login_presenter)

@app.route("/users/register", methods=['POST'])
def register_user():
    data = request.json
    return registrar_usuario_logica(*adapter.adapter_user_datas(data),presenters.user_registration_presenter)

@app.route("/users/seealltouristspot", methods=['GET'])
def ver_todos_pontos():
    return ver_todos_pontos_logica(presenters.points_presenter)

@app.route("/users/touristSpot5KM/", methods=['GET'])
@auth.token_required
def pontos_turisticos_5km(email_user):
    data = request.json

    return pontos_turisticos_5km_logica(*adapter.adapter_coordenates_spot(data),email_user,presenters.points_presenter)

@app.route("/users/touristSpotName", methods=['GET'])
@auth.token_required
def pontos_turisticos_por_nome(email_user):
    data = request.json
    return pontos_turisticos_por_nome_logica(adapter.adapter_name_spot(data),email_user,presenters.one_point_presenter)

@app.route("/users/registertouristspot", methods=['POST'])
@auth.token_required
def registrar_ponto_turistico(email_user):
    data = request.json
    return registrar_ponto_turistico_com_categoria(*adapter.adapter_tourist_spot(data),email_user,presenters.point_registration_presenter,presenters.category_registration_presenter)

@app.route("/users/commenttouritspot", methods=['POST'])
@auth.token_required
def comentar_ponto_turistico(email_user):
    data = request.json

    return comentar_ponto_turistico_logica(*adapter.adapter_comment_spot(data),email_user,presenters.commentary_registration_presenter)

@app.route("/users/seecommenttouritspot", methods=['GET'])
def ver_comentarios_pontos_turisticos():
    data = request.json
    return ver_comentario_ponto_turistico_logica(adapter.adapter_name_spot(data),presenters.points_presenter,presenters.commentary_visualization_presenter)

@app.route("/users/favoriteaspot", methods=['POST'])
@auth.token_required
def favoritar_ponto_turistico(email_user):
    data = request.json
    return favoritar_ponto_turistico_logica(adapter.adapter_name_spot(data),email_user,presenters.favored_spot_presenter,presenters.points_presenter)

@app.route("/users/seefavoritespot", methods=['GET'])
@auth.token_required
def ver_ponto_turistico_favorito(email_user):
    return ver_ponto_turistico_favoritado_logica(email_user,presenters.see_favored_spot_presenter)

@app.route("/users/removefavoritespot", methods=['DELETE'])
@auth.token_required
def remover_ponto_favoritado(email_user):
    data = request.json
    return remover_ponto_favoritado_logica(adapter.adapter_name_spot(data),email_user,presenters.remove_favored_spot_presenter)

@app.route("/users/upvotespot", methods=['POST'])
@auth.token_required
def upvote_ponto(email_user):
    data = request.json
    return upvote_ponto_logica(adapter.adapter_name_spot(data),email_user)

@app.route("/users/seetouristspotcreatedbyme", methods=['GET'])
@auth.token_required
def ver_pontos_criados_por_mim(email_user):
    return ver_pontos_criados_por_mim_logica(email_user)

@app.route("/users/createnewcategorie", methods=['POST'])
@auth.token_required
def criar_nova_categoria():
    data = request.json
    return create_new_category_if_not_exist(adapter.adapter_category_spot(data))


