from flask import jsonify

def user_registration_presenter(success,user_email=None):
    if not success:
        return jsonify({'messege': 'O usuário já existe'}), 403
    else:
        return jsonify({'user_email': user_email}), 201


def user_login_presenter(success, token=None):
    if success:
        return jsonify({'token':token})
    else:
        return jsonify({'messege': 'Acesso negado!'}), 401



def points_presenter(points=None):
    if points!=None:
        return jsonify({'aqui estão os pontos:': points}), 200
    else:
        return jsonify({'nenhum ponto encontrado.':''}),200

def  one_point_presenter(success,point=None):
    if success:
        return jsonify({'ponto:':point}),200
    else:
        return jsonify({'messege': 'O ponto informado não foi localizado'}), 404

def point_registration_presenter(success,nome_ponto=None,categoria_ponto=None,latitude_ponto=None,longitude_ponto=None,email_usuario=None):
    if success:
        return jsonify({'nome: ': nome_ponto,'categoria: ': categoria_ponto,'latitude: ': latitude_ponto,'longitude: ':longitude_ponto,'criador: ':email_usuario}), 201
    else:
        return jsonify({'messege': 'O ponto já  existe.'}), 403

def category_registration_presenter(success,cod = None,nome=None):
    if success:
        return jsonify({'código: ': cod,'nome: ': nome}), 201
    else:
        return jsonify({'messege': 'A categoria já eixste.'}), 403