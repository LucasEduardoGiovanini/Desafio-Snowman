

from flask import Flask, request, jsonify,app,make_response #importo a app que é a primeira classe que irá rodar
from werkzeug.datastructures import FileStorage
import pymysql
import base64
from math import radians, cos, sin, asin, sqrt  # conteudo importado para encontrar pontos por km utilizando formula de haversine
from tests import *
import random
from repositories import PontoTuristicoRepository,UserRepostory
from http import HTTPStatus
import auth
from functools import wraps





use_cases_turismo = Flask(__name__)


if __name__ == "__main__":
    app.run() #rodo a classe app





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

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = request.args.get('token')
        if not(access_token):
            return jsonify({'message': 'token is missing!'}),401

        try:
            auth.Token().decode_json_web_token(access_token,'johnnyboy')
        except:
            return jsonify({'message':'invalid token'}),403
        return f(*args,**kwargs)

    return decorated


def login_logica(data):
    email_usuario = data.get('email')
    senha_usuario = data.get('senha')

    authorization = validar_senha_do_usuario(data)
    print(authorization[1])
    if(authorization[1] == HTTPStatus.OK): #se a autorização for http OK
        repository = UserRepostory()
        database_user_password = repository.validate_user_email_and_get_his_password(email_usuario)
        return jsonify({'token':auth.Token().create_json_web_token(database_user_password)})

    else:
        return jsonify({'messege': 'Acesso negado!'}), 401

#use case chama a função de encrptar pra senha, encripta e chama a função do repositorio do usuario pra armazenar os dados já encriptados
def registrar_usuario_logica(data):

    email_usuario = data.get('email')
    senha_usuario = data.get('senha')

    encrypted_password = auth.Encrypt.encrypt_password(senha_usuario)
    repository = UserRepostory()
    registered = repository.register_user(email_usuario,encrypted_password)
    if(registered == False):
        return jsonify({'messege': 'O usuário já existe'}), 403
    else:
        return jsonify({'messege': 'Usuário cadastrado com sucesso'}), 200

def validar_senha_do_usuario(data):
    email_usuario = data.get('email')
    senha_usuario = data.get('senha')

    repository = UserRepostory()

    database_user_password = repository.validate_user_email_and_get_his_password(email_usuario) #retorna a senha



    if(database_user_password):
        encrypt = auth.Encrypt()
        validation = encrypt.validate_user_password(senha_usuario,database_user_password)
        if(validation == True):
            return jsonify({'messege': 'Usuário válido.'}), 200
        else:
            return jsonify({'messege': 'Usuário inválido.'}), 403

    else:
        return jsonify({'messege': 'Usuário não localizado.'}), 404


def ver_todos_pontos_logica():
    repository =PontoTuristicoRepository()
    all_points = repository.search_points()
    return jsonify({'messege': 'aqui estão os pontos:','ponto(os)':all_points}), 200


def pontos_turisticos_5km_logica(data):
    latitude_usuario = data.get('lat')
    longitude_usuario = data.get('long')
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')

    repository = UserRepostory()
    user_registered = repository.validate_user_email_and_get_his_password(email_usuario, senha_usuario) #primeiro trato da validação

    if(user_registered == False):#se o login não for autorizado
        return jsonify({'messege': 'login ou senha incorretos'}), 401
    else:
        # se o meu login for autorizado eu realizo a busca pelos pontos,
        repository = PontoTuristicoRepository()
        points = repository.search_points()
        resultado = points
        dado = list()
        for x in resultado:  #como temos varios pontos, preciso percorrer todos, pegar seus dados e compara-los utilizando a formula
            distancia_km = haversine(float(longitude_usuario), float(latitude_usuario), float(x['longitude']), float(x['latitude']))     # aplico a latitude e longitude dos dois pontos na formula de haversine para obter a distancia em km
            if (distancia_km <= 5):
                x['distancia em Km'] = round(distancia_km, 2)
                dado.append(x)
        if (not dado):
            return jsonify({'resultado': 'nenhum ponto foi encontrado'}), 404
        else:
            return jsonify({'resultado ': dado}), 200  # status code http


def pontos_turisticos_por_nome_logica(data):
    ponto = data.get('spot')  # pega o valor seguido se spot
    repository = PontoTuristicoRepository() #chama a classe que faz as ligações com o banco
    ponto = repository.get_ponto_turistico_by_name(ponto)
    if(not ponto):
        return jsonify({'message':'O ponto informado não existe'}),404
    else:
        return jsonify({'Pontos':ponto}), 200  # status code http


def registrar_ponto_turistico_logica(data):

    email_usuario = data.get('login')
    senha_usuario = data.get('senha')
    nome_ponto = data.get('nome')
    latitude_ponto = data.get('latitude')
    longitude_ponto = data.get('longitude')
    categoria_ponto = data.get('categoria')
    foto_ponto = data.get('foto')
    # picture decode (base 64) -------------------------------------------
    decode_picture = base64.b64decode(foto_ponto) #recebo a foto em base 64 e dou um decode
    #---------------
    categoria_ponto = categoria_ponto.lower().capitalize()
    repository = UserRepostory()
    user_registered = repository.validate_user_email_and_get_his_password(email_usuario, senha_usuario)
    if(user_registered == False):
        return jsonify({'messege': 'login ou senha incorretos'}), 401
    else:
        repository = PontoTuristicoRepository()
        point_exists = repository.check_existence_of_the_point(nome_ponto)

        if(point_exists):
            return jsonify({'message': 'esse ponto já foi cadastrado!'}), 403  # proibido
        else:
            category_exist = repository.check_existence_of_category(categoria_ponto)

            if(category_exist == False):
                cod_category = repository.create_category(categoria_ponto)
                category_exist = repository.check_existence_of_category(categoria_ponto) #solicito novamente a verificação da categoria, para que possa entrar no elif abaixo
                jsonify({'Mensagem': 'categoria criada com sucesso!'})  # status code http

            elif(category_exist):
                 extract_cod_category = int(category_exist['cod'])
                 repository.create_tourist_point(nome_ponto,extract_cod_category,latitude_ponto,longitude_ponto,email_usuario)


                 if(foto_ponto!=None):# se o usuário tiver enviado uma foto do ponto, cadastramos
                    repository.add_picture_spot(foto_ponto,nome_ponto,email_usuario) #adicionamos a foto do ponto
            return jsonify({'messege': 'ponto cadastrado com sucesso!'}), 200




def comentar_ponto_turistico_logica(data):
    nome_ponto = data.get('nome')  # pega o valor armazenado em "nome"
    descricao_comentario = data.get('comentario')
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')

    repository = UserRepostory()
    user_registered = repository.validate_user_email_and_get_his_password(email_usuario, senha_usuario)  # primeiro trato da validação

    if (user_registered == False):  # se o login não for autorizado
        return jsonify({'messege': 'login ou senha incorretos'}), 401
    else:
        repository = PontoTuristicoRepository()
        point_exists = repository.check_existence_of_the_point(nome_ponto)
        if(point_exists):
            repository.create_comment_about_poin(email_usuario,nome_ponto,descricao_comentario)
            return jsonify({'message': 'comentário cadastrado com sucesso!'}), 200  # proibido

        else:
            return jsonify({'message': 'o ponto informado não existe.'}), 404  # proibido


def ver_comentario_ponto_turistico_logica(data):
    nome_ponto = data.get('nome')
    repository = PontoTuristicoRepository()
    point_exist = repository.check_existence_of_the_point(nome_ponto)
    if(point_exist):
        comments = repository.search_comments(nome_ponto)
        if(comments==None):
            return jsonify({'message': 'parece que esse ponto ainda não possui comentários'}), 200  # proibido
        else:
            list_comments=list() #os comentários serão inseridos na lista para que retorne com um formato adequado.

            for comment in comments:
                list_comments.append(comment['descricao'])
            return jsonify({'comentário(s)\n':list_comments}), 200  # proibido

    else:
        return jsonify({'message': 'o ponto informado não existe.'}), 404  # proibido


def adicionar_foto_ponto_logica(data):
    login_usuario = data.get('login')
    senha_usuario = data.get('senha')
    nome_ponto = data.get('nome')
    foto_ponto = data.get('foto')
    decode_picture = base64.b64decode(foto_ponto)  # recebo a foto em base 64 e dou um decode

    repository = UserRepostory()
    user_registered = repository.validate_user_email_and_get_his_password(login_usuario, senha_usuario)
    if(user_registered==False):
        return jsonify({'messege': 'login ou senha incorretos'}), 401
    else:
        repository = PontoTuristicoRepository()
        point_exists = repository.check_existence_of_the_point(nome_ponto)
        if(not point_exists):
            return jsonify({'messege': 'o ponto informado não existe!'}), 403
        else:
            repository.add_picture_spot(foto_ponto,nome_ponto,login_usuario)
            return jsonify({'messege': 'foto cadastrada com sucesso!'}), 200



def remover_foto_ponto_logica(data):
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')
    cod_foto = data.get('cod_foto')

    repository = UserRepostory()
    user_registered = repository.validate_user_email_and_get_his_password(email_usuario, senha_usuario)

    if (user_registered == False):  # se o login não for autorizado
        return jsonify({'messege': 'login ou senha incorretos'}), 401
    else:
        repository = PontoTuristicoRepository()
        photo_exist = repository.search_picture(cod_foto)
        if(photo_exist):
            photo_deleted = repository.delete_picture(cod_foto,email_usuario)
            return jsonify({'messege': 'foto apagada com sucesso'}), 200
        else:
            return jsonify({'messege': 'foto não encontrada'}), 404


def favoritar_ponto_turistico_logica(data):
    nome_ponto = data.get('nome')  # pega o valor armazenado em "nome"
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')

    repository = UserRepostory()
    user_registered = repository.validate_user_email_and_get_his_password(email_usuario, senha_usuario)
    if(user_registered==False):
        return jsonify({'messege': 'login ou senha incorretos'}), 401
    else:
        repository = PontoTuristicoRepository()
        point_exists = repository.check_existence_of_the_point(nome_ponto)
        if(not point_exists):
            return jsonify({'messege': 'o ponto informado não existe!'}), 404
        else:
            repository = UserRepostory()
            result = repository.favorite_tourist_spot(email_usuario,nome_ponto)
            if(result):
                return jsonify({'messege': 'ponto favoritado com sucesso!'}), 200
            else:
                return jsonify({'messege': 'o ponto já está favoritado'}), 403



def ver_ponto_turistico_favoritado_logica(data):
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')

    repository = UserRepostory()
    user_registered = repository.validate_user_email_and_get_his_password(email_usuario, senha_usuario)
    if (user_registered == False):
        return jsonify({'messege': 'login ou senha incorretos'}), 401
    else:

        points = repository.search_favorited_spots(email_usuario)
        if (not points):
            return jsonify({'messege': 'o ponto informado não existe!'}), 404
        else:
            return jsonify({'Mensagem': 'sucesso! aqui estão seus pontos!', "ponto": points}), 200


def remover_ponto_favoritado_logica(data):
    nome_ponto = data.get('nome')  # pega o valor armazenado em "nome"
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')

    repository = UserRepostory()
    user_registered = repository.validate_user_email_and_get_his_password(email_usuario, senha_usuario)
    if(user_registered==False):
        return jsonify({'messege': 'login ou senha incorretos'}), 401
    else:
        repository=UserRepostory()

        point_favored = repository.check_who_favored_point(email_usuario,nome_ponto)
        if(point_favored == None):
            return jsonify({'messege': 'o ponto não foi localizado'}), 404
        else:
            repository.remove_favorited_tourist_spot(email_usuario,nome_ponto)
            return jsonify({'messege': 'ponto removido!'}), 200



def upvote_ponto_logica(data):
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')
    nome_ponto = data.get('nome')

    repository = UserRepostory()
    user_registered = repository.validate_user_email_and_get_his_password(email_usuario, senha_usuario)
    if(user_registered==False):
        return jsonify({'messege': 'login ou senha incorretos'}), 401
    else:
        repository = PontoTuristicoRepository()
        point_exists = repository.check_existence_of_the_point(nome_ponto)
        if(not point_exists):
            return jsonify({'messege': 'o ponto informado não existe!'}), 404
        else:
            repository.register_upvote(nome_ponto)
            return jsonify({'messege': 'ponto favoritado!'}), 200



def ver_pontos_criados_por_mim_logica(data):
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')

    repository = UserRepostory()
    user_registered = repository.validate_user_email_and_get_his_password(email_usuario, senha_usuario)
    if(user_registered==False):
        return jsonify({'messege': 'login ou senha incorretos'}), 401
    else:

        my_points = repository.search_tourist_points_created_by_user(email_usuario)
        if(my_points == None):
            return jsonify({'messege': 'parece que você não cadastrou nenhum ponto!'}), 200
        else:
            return jsonify({'messege': 'aqui estão seus pontos:','ponto(os)':my_points}),200


def criar_nova_categoria_logica(data):
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')
    nome_categoria = data.get('categoria')

    nome_categoria=nome_categoria.lower().capitalize() #pego a string e deixo toda em minusculo com apenas a primeira letra maisucula, para seguir o padrão do meu banco

    repository = UserRepostory()
    user_registered = repository.validate_user_email_and_get_his_password(email_usuario, senha_usuario)
    if (user_registered == False):
        return jsonify({'messege': 'login ou senha incorretos'}), 401
    else:
        repository = PontoTuristicoRepository()
        category_exist=repository.check_existence_of_category(nome_categoria)

        if (category_exist == False):
            repository.create_category(nome_categoria)
            return jsonify({'messege': 'categoria criada com sucesso!'}), 200
        else:
            return jsonify({'messege': 'essa categoria já existe.'}), 403

