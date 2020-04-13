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

def point_registration_presenter(success,categoria_existe,nome_ponto=None,categoria_ponto=None,latitude_ponto=None,longitude_ponto=None,email_usuario=None):
    if success and categoria_existe:
        return jsonify({'nome: ': nome_ponto,'categoria: ': categoria_ponto,'latitude: ': latitude_ponto,'longitude: ':longitude_ponto,'criador: ':email_usuario}), 201
    elif not success and categoria_existe:
        return jsonify({'messege': 'O ponto já  existe.'}), 403
    else:
        return jsonify({'message': 'a categoria não existe!'}), 404

def category_registration_presenter(success,cod = None,nome=None):
    if success:
        return jsonify({'código: ': cod,'nome: ': nome}), 201
    else:
        return jsonify({'messege': 'A categoria já eixste.'}), 403

def commentary_visualization_presenter(success,point_exist,list_comments=None):
    if success and point_exist:
        return jsonify({'comentário(s)\n':list_comments}), 200
    elif not success and point_exist:
        return jsonify({'message': 'parece que esse ponto ainda não possui comentários'}), 200
    else:
        return jsonify({'message': 'o ponto informado não existe.'}), 404

def favored_spot_presenter(success,point_exist,nome_ponto=None,email_usuario=None):
    if success and point_exist:
        return jsonify({'ponto:': nome_ponto,'criador: ':email_usuario}), 201
    elif not success and point_exist:
        return jsonify({'messege': 'o ponto já está favoritado'}), 403
    else:
        return jsonify({'messege': 'o ponto informado não existe!'}), 404

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

def upvote_point_presenter(success,nome=None,quant=None):
    if success:
        return jsonify({'nome: ':nome,'quantidade_upvotes':quant}), 200
    else:
        return jsonify({'message':'O ponto informado não existe.'}),404
def see_my_spots_created_presenter(success,points=None):
    if success:
        return jsonify({'messege': 'aqui estão seus pontos:', 'ponto(os)': points}), 200
    else:
        return jsonify({'messege': 'parece que você não cadastrou nenhum ponto!'}), 200