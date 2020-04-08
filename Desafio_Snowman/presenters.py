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

