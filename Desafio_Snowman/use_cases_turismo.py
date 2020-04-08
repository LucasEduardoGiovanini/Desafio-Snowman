from flask import Flask, request, jsonify,app,make_response
from werkzeug.datastructures import FileStorage
import pymysql
import base64
from math import radians, cos, sin, asin, sqrt  # conteudo importado para encontrar pontos por km utilizando formula de haversine
from tests import *
import random
from repositories import PontoTuristicoRepository,UserRepostory
from http import HTTPStatus
import auth
from typing import Tuple





def haversine(lon1, lat1, lon2, lat2):  # def que aplica a formula de haversine para encontrar pontos num raio de 5km

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r



def escreve_imagem(data):
    for x in data:
        imagem = x['foto']
        nome_foto = x['nome'] + str(x['cod'])
        with open('C:/Users/lucas/Desktop/photo test/'+nome_foto+'.png', 'wb') as q:
            q.write(imagem)


def checar_usuario_existe(email_usuario):
    repository = UserRepostory()
    check_existance_of_user = repository.verify_email(email_usuario)
    return True if check_existance_of_user == True else False


def validar_email_senha_do_usuario(email_usuario,senha_usuario):
    repository = UserRepostory()
    encrypted_password = repository.get_encrypt_password(email_usuario)

    if encrypted_password:
        approved_password = auth.validate_user_password(senha_usuario,encrypted_password)
        if approved_password:
            return True

    return False

UserLoginResponse = Tuple['success', 'user_email']
def login_logica(email_usuario,senha_usuario,presenter) -> UserLoginResponse:
    authorization = validar_email_senha_do_usuario(email_usuario,senha_usuario)
    if authorization:
        repository = UserRepostory()

        user_token = auth.create_json_web_token(email_usuario)
        return presenter(True,auth.serializer_token(user_token))
    else:
        return presenter(False)



UserRegistrationResponse = Tuple['success', 'user_email'] #dicionário informativo sobre os dados que serão repassados
def registrar_usuario_logica(email_usuario,senha_usuario,presenter) -> UserRegistrationResponse: #indico o tipo de retorno que essa função vai ter
    encrypted_password = auth.encrypt_password(senha_usuario)
    repository = UserRepostory()

    user_already_registered = repository.get_encrypt_password(email_usuario)

    if user_already_registered:

        return presenter(False)
    else:
        registered = repository.insert_user(email_usuario, encrypted_password)
        return presenter(True,*registered.values()) #retorno todos os dados de registro desmembrados para a respectiva função do presenter .values retorna apenas os valores do json


AllPointsResponse = Tuple['list_points']
def ver_todos_pontos_logica(presenter) -> AllPointsResponse:
    repository = PontoTuristicoRepository()
    all_points = repository.search_points()
    return presenter(all_points)

Points5kmResponse = Tuple['list_points']
def pontos_turisticos_5km_logica(latitude_usuario,longitude_usuario,email_user,presenter) ->Points5kmResponse:
    repository = PontoTuristicoRepository()
    resultado = repository.search_points()
    dado = list()
    for ponto in resultado:
        distancia_km = haversine(float(longitude_usuario), float(latitude_usuario), float(ponto['longitude']), float(ponto['latitude']))     # aplico a latitude e longitude dos dois pontos na formula de haversine para obter a distancia em km
        if (distancia_km <= 5):
            ponto['distancia em Km'] = round(distancia_km, 2)
            dado.append(ponto)
    if not dado:
        return presenter(False)
    else:
        return presenter(dado)

SearchPointResponse = Tuple['Success','point']
def pontos_turisticos_por_nome_logica(ponto,email_usuario,presenter)->SearchPointResponse:
    repository = PontoTuristicoRepository()
    ponto = repository.get_ponto_turistico_by_name(ponto)
    if not ponto:
        return presenter(False)
    else:
        return presenter(True,ponto)


def registrar_ponto_turistico_com_categoria(nome_ponto,latitude_ponto,longitude_ponto,categoria_ponto,email_usuario,presenter_point,presenter_category):
    create_new_category_if_not_exist(categoria_ponto,presenter_category)
    return registrar_ponto_turistico_logica(nome_ponto,latitude_ponto,longitude_ponto,categoria_ponto,email_usuario,presenter_point)

PointCreationResponse = Tuple['Success','nome','laitutde','longitude','categoria','criador']
def registrar_ponto_turistico_logica(nome_ponto,latitude_ponto,longitude_ponto,categoria_ponto,email_usuario,presenter)->PointCreationResponse:
    repository = PontoTuristicoRepository()
    point_exists = repository.check_existence_of_the_point(nome_ponto)
    if not point_exists:
        categoria_ponto = categoria_ponto.lower().capitalize()
        codigo_categoria = repository.check_existence_of_category(categoria_ponto)
        extract_cod_category = int(codigo_categoria['cod'])
        point_created=repository.create_tourist_point_and_upvote(nome_ponto, extract_cod_category, latitude_ponto, longitude_ponto, email_usuario)
        return presenter(True,*point_created.values())
    else:
        return presenter(False)


def comentar_ponto_turistico_logica(nome_ponto,descricao_comentario,email_usuario):
    repository = PontoTuristicoRepository()
    point_exists = repository.check_existence_of_the_point(nome_ponto)
    if point_exists :
        repository.create_comment_about_point(email_usuario, nome_ponto, descricao_comentario)
        return jsonify({'message': 'comentário cadastrado com sucesso!'}), 200
    else:
        return jsonify({'message': 'o ponto informado não existe.'}), 404

def ver_comentario_ponto_turistico_logica(nome_ponto):

    repository = PontoTuristicoRepository()
    point_exist = repository.check_existence_of_the_point(nome_ponto)
    print(point_exist)
    if point_exist:
        comments = repository.search_comments(nome_ponto)
        if not comments:
            return jsonify({'message': 'parece que esse ponto ainda não possui comentários'}), 200
        else:
            list_comments=list() #os comentários serão inseridos na lista para que retorne com um formato adequado.
            for comment in comments:
                list_comments.append(comment['descricao'])
            return jsonify({'comentário(s)\n':list_comments}), 200
    else:
        return jsonify({'message': 'o ponto informado não existe.'}), 404


def adicionar_foto_ponto_logica(data,email_usuario):
    decode_picture = base64.b64decode(foto_ponto)
    repository = PontoTuristicoRepository()
    point_exists = repository.check_existence_of_the_point(nome_ponto)
    if point_exists :
        repository.add_picture_spot(foto_ponto, nome_ponto, email_usuario)
        return jsonify({'messege': 'foto cadastrada com sucesso!'}), 200
    else:
        return jsonify({'messege': 'o ponto informado não existe!'}), 403




def remover_foto_ponto_logica(data,email_usuario):
    repository = PontoTuristicoRepository()
    photo_exist = repository.search_picture(cod_foto)
    if photo_exist :
        photo_deleted = repository.delete_picture(cod_foto,email_usuario)
        return jsonify({'messege': 'foto apagada com sucesso'}), 200
    else:
        return jsonify({'messege': 'foto não encontrada'}), 404


def favoritar_ponto_turistico_logica(nome_ponto,email_usuario):
    repository = PontoTuristicoRepository()
    point_exists = repository.check_existence_of_the_point(nome_ponto)
    if  point_exists :
        repository = UserRepostory()
        points = repository.search_favorited_spots(email_usuario)
        for ponto in points:
            if ponto['nome'] == nome_ponto:
                return jsonify({'messege': 'o ponto já está favoritado'}), 403

        result = repository.favorite_tourist_spot(email_usuario, nome_ponto)
        if result:
            return jsonify({'messege': 'ponto favoritado com sucesso!'}), 200
    else:
        return jsonify({'messege': 'o ponto informado não existe!'}), 404




def ver_ponto_turistico_favoritado_logica(email_usuario):
    repository = UserRepostory()
    points_favoriteds = repository.search_favorited_spots(email_usuario)
    if points_favoriteds:
        return jsonify({'Mensagem': 'sucesso! aqui estão seus pontos!', "ponto": points_favoriteds}), 200
    else:
        return jsonify({'messege': 'o ponto informado não existe!'}), 404




def remover_ponto_favoritado_logica(nome_ponto,email_usuario):
    repository=PontoTuristicoRepository()
    user_favored_this_point = repository.check_who_favored_point(email_usuario,nome_ponto)
    if  user_favored_this_point :
        repository = UserRepostory()
        repository.remove_favorited_tourist_spot(email_usuario, nome_ponto)
        return jsonify({'messege': 'ponto removido!'}), 200
    else:
        return jsonify({'messege': 'o ponto não foi localizado'}), 404




def upvote_ponto_logica(nome_ponto,email_usuario):

    repository = PontoTuristicoRepository()
    point_exists = repository.check_existence_of_the_point(nome_ponto)
    if point_exists:
        repository.register_upvote(nome_ponto)
        return jsonify({'messege': 'ponto favoritado!'}), 200
    else:
        return jsonify({'messege': 'o ponto informado não existe!'}), 404



def ver_pontos_criados_por_mim_logica(email_usuario):
    repository = UserRepostory()
    my_points = repository.search_tourist_points_created_by_user(email_usuario)
    if my_points :
        return jsonify({'messege': 'aqui estão seus pontos:', 'ponto(os)': my_points}), 200
    else:
        return jsonify({'messege': 'parece que você não cadastrou nenhum ponto!'}), 200


CategoryCreationResponse = Tuple['Success','cod','nome_categoria']
def create_new_category_if_not_exist(nome_categoria,presenter)->CategoryCreationResponse:
    nome_categoria=nome_categoria.lower().capitalize()
    repository = PontoTuristicoRepository()
    category_exist=repository.check_existence_of_category(nome_categoria)

    if  category_exist:
        return presenter(False)
    else:
        new_category = repository.create_category(nome_categoria)
        return presenter(True,*new_category.values())



