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


def points_presenter(success,points=None):
    if success:
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

def commentary_visualization_presenter(success,list_comments=None):
    if success:
        return jsonify({'comentário(s)\n':list_comments}), 200
    else:
        return jsonify({'message': 'parece que esse ponto ainda não possui comentários'}), 200

def favored_spot_presenter(success,nome_ponto=None,email_usuario=None):
    if success:
        return jsonify({'ponto:': nome_ponto,'criador: ':email_usuario}), 201
    else:
        return jsonify({'messege': 'o ponto já está favoritado'}), 403

def see_favored_spot_presenter(success,pontos=None):
    if success:
        return jsonify({"ponto(os): ": pontos}), 200
    else:
        return jsonify({'messege': 'o ponto informado não existe!'}), 404
def remove_favored_spot_presenter(success):
    if success:
        return jsonify({'messege': 'ponto removido!'}), 200
    else:
        return jsonify({'messege': 'o ponto não foi localizado.'}), 404