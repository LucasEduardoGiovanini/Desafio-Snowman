from flask import request, jsonify
import bcrypt,jwt,datetime
import os
from functools import wraps
secret_key = os.urandom(16)
import use_cases_turismo
from repositories import UserRepostory


def encrypt_password(password:str):
    byte_password = str.encode(password)
    hashed = bcrypt.hashpw(byte_password, bcrypt.gensalt(10))
    return hashed

def validate_user_password(normal_password:str,encrypted_password:str):
    return True if bcrypt.checkpw(str.encode(normal_password),str.encode(encrypted_password)) else False


def create_json_web_token(email:str):
    return jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},secret_key)


def decode_json_web_token(token:str):
    return jwt.decode(token,secret_key)


def serializer_token(token: bytes):
    return token.decode('UTF-8')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token_required = request.headers.get("Authorization")  # chega o token com bearer precedendo ele
        access_token = token_required.split(" ")[1]  # removo o bearer com o split
        if not access_token:
            return jsonify({'message': 'token is missing!'}), 401

        try:
            token =decode_json_web_token(access_token)
            email_user = token['email']
            user_validate =checar_usuario_existe(email_user)
            if not user_validate:
                return jsonify({'message': 'o usuário não é mais válido!'}), 401
        except:
            return jsonify({'message': 'invalid token'}), 403

        return f(*args,email_user, **kwargs)

    return decorated


def checar_usuario_existe(email_usuario):
    repository = UserRepostory()
    check_existance_of_user = repository.verify_email(email_usuario)
    return True if check_existance_of_user == True else False


def validar_email_senha_do_usuario(email_usuario,senha_usuario):
    repository = UserRepostory()
    encrypted_password = repository.get_encrypt_password(email_usuario)

    if encrypted_password:
        approved_password = validate_user_password(senha_usuario,encrypted_password)
        if approved_password:
            return True
    return False

