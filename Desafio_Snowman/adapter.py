from flask import request
import auth
def adapter_tourist_spot():
    data = request.json
    nome_ponto = data.get('nome')
    latitude_ponto = data.get('latitude')
    longitude_ponto = data.get('longitude')
    categoria_ponto = data.get('categoria')
    foto_ponto = data.get('foto')
    return nome_ponto,latitude_ponto,longitude_ponto,categoria_ponto,foto_ponto

def adapter_user_datas():
    data = request.json
    email_usuario = data.get('email')
    senha_usuario = data.get('senha')
    return email_usuario,senha_usuario

def adapter_token_email():
    access_token = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
    decoded_token = auth.decode_json_web_token(access_token.split(" ")[1])
    email_user = decoded_token['email']
    return email_user


def adapter_coordenates_spot():
    data = request.json
    latitude_usuario = data.get('lat')
    longitude_usuario = data.get('long')
    return latitude_usuario,longitude_usuario

def adapter_name_spot():
    data = request.json
    ponto = data.get('spot')
    return ponto

def adapter_comment_spot():
    data = request.json
    nome_ponto = data.get('nome')
    descricao_comentario = data.get('comentario')
    return nome_ponto,descricao_comentario

def adapter_picture_spot():
    data = request.json
    nome_ponto = data.get('nome')
    foto_ponto = data.get('foto')
    return nome_ponto,foto_ponto

def adapter_cod_picture_spot():
    data = request.json
    cod_foto = data.get('cod_foto')
    return cod_foto

def adapter_category_spot():
    data = request.json
    nome_categoria = data.get('categoria')
    return nome_categoria