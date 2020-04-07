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


def login_logica(email_usuario,senha_usuario):
    authorization = validar_email_senha_do_usuario(email_usuario,senha_usuario)
    if authorization:
        repository = UserRepostory()
        user_token = auth.create_json_web_token(email_usuario)
        return jsonify({'token':auth.serializer_token(user_token)})
    else:
        return jsonify({'messege': 'Acesso negado!'}), 401



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



def ver_todos_pontos_logica():
    repository = PontoTuristicoRepository()
    all_points = repository.search_points()
    return jsonify({'messege': 'aqui estão os pontos:','ponto(os)':all_points}), 200

def pontos_turisticos_5km_logica(latitude_usuario,longitude_usuario,email_user):
    repository = PontoTuristicoRepository()
    points = repository.search_points()
    resultado = points
    dado = list()
    for x in resultado:  #como temos varios pontos, preciso percorrer todos, pegar seus dados e compara-los utilizando a formula
        distancia_km = haversine(float(longitude_usuario), float(latitude_usuario), float(x['longitude']), float(x['latitude']))     # aplico a latitude e longitude dos dois pontos na formula de haversine para obter a distancia em km
        if (distancia_km <= 5):
            x['distancia em Km'] = round(distancia_km, 2)
            dado.append(x)
    if not dado:
        return jsonify({'resultado': 'nenhum ponto foi encontrado'}), 404
    else:
        return jsonify({'resultado ': dado}), 200  # status code http


def pontos_turisticos_por_nome_logica(ponto,email_usuario):
    repository = PontoTuristicoRepository()
    ponto = repository.get_ponto_turistico_by_name(ponto)
    if not ponto:
        return jsonify({'message':'O ponto informado não existe'}),404
    else:
        return jsonify({'Pontos':ponto}), 200


def registrar_ponto_turistico_logica(nome_ponto,latitude_ponto,longitude_ponto,categoria_ponto,foto_ponto,email_usuario):

    decode_picture = base64.b64decode(foto_ponto)

    categoria_ponto = categoria_ponto.lower().capitalize()

    repository = PontoTuristicoRepository()
    point_exists = repository.check_existence_of_the_point(nome_ponto)
    if point_exists:
        return jsonify({'message': 'esse ponto já foi cadastrado!'}), 403
    else:
        category_exist = repository.check_existence_of_category(categoria_ponto)

        if not category_exist : #nesse caso eu preciso manter a verificação de booleano, pois preciso obter o falso primeiro, para saber se devo criar essa categoria antes de passar par a proxima condição
            datas_category = repository.create_category(categoria_ponto)
            category_exist = repository.check_existence_of_category(categoria_ponto) #solicito novamente a verificação da categoria, para que possa entrar no elif abaixo
            print(category_exist)
            jsonify({'Mensagem': 'categoria criada com sucesso!'})

        if category_exist:
             extract_cod_category = int(category_exist['cod'])
             repository.create_tourist_point_and_upvote(nome_ponto, extract_cod_category, latitude_ponto, longitude_ponto, email_usuario)

             if foto_ponto:
                repository.add_picture_spot(foto_ponto,nome_ponto,email_usuario)
        return jsonify({'messege': 'ponto cadastrado com sucesso!'}), 200


def comentar_ponto_turistico_logica(nome_ponto,descricao_comentario,email_usuario):
    nome_ponto = data.get('nome')
    descricao_comentario = data.get('comentario')

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




def criar_nova_categoria_logica(nome_categoria):
    nome_categoria=nome_categoria.lower().capitalize()

    repository = PontoTuristicoRepository()
    category_exist=repository.check_existence_of_category(nome_categoria)

    if  category_exist:
        return jsonify({'messege': 'essa categoria já existe.'}), 403
    else:
        repository.create_category(nome_categoria)
        return jsonify({'messege': 'categoria criada com sucesso!'}), 200



