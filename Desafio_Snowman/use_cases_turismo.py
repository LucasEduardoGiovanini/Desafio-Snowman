from flask import Flask, request, jsonify,app #importo a app que é a primeira classe que irá rodar
import pymysql
from math import radians, cos, sin, asin, sqrt  # conteudo importado para encontrar pontos por km utilizando formula de haversine
from entities import dbconnection,verifica_login
from tests import *

use_cases_turismo = Flask(__name__)

app = Flask(__name__)


if __name__ == "__main__":
    app.run() #rodo a classe app


@app.route("/", methods=['POST'])
def inicial():#passo todos os meus testes


    return "Inicial", 400  # status code http


def haversine(lon1, lat1, lon2, lat2):  # def que aplica a formula de haversine para encontrar pontos num raio de 5km

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r


@app.route("/users/seealltouristspot", methods=['GET'])  #ver todos os pontos turisticos cadastrados
def ver_todos_pontos():
    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco #a variavel dispensavel n sera utilizada nessa def pois não necessitamos de seu retorno
    cursor[0].execute("SELECT nome, categoria, latitude, longitude FROM tbPontoTuristico")  # faço uma busca no banco pelo ponto turistico informado
    resultado = cursor[0].fetchall()  # comando que faz a busca por toda a informação da tabela
    if(not resultado):
        return jsonify({'message':'nao existem pontos cadastrados'}),404
    else:
        return jsonify({'message':resultado}), 200  # status code http




@app.route("/users/touristSpot5KM", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
def pontos_turisticos_5km():
    data = request.json  # solicita o json enviado pelo postman
    return pontos_turisticos_5km_logica(data)

def pontos_turisticos_5km_logica(data):
    latitude_usuario = data.get('lat')  # pega o valor seguido se spot
    longitude_usuario = data.get('long')
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')

    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco
    autenticacao = verifica_login(email_usuario, senha_usuario)
    if (autenticacao == False):
        return jsonify({'messege': 'login ou senha incorretos'}), 404
    else:
        cursor[0].execute(
            "SELECT nome, categoria, latitude, longitude FROM tbPontoTuristico")  # solicito todos os pontos turisticos
        resultado = cursor[0].fetchall()  # comando que faz a busca por toda a informação da tabela

        dado = list()  # lista que armazenará todos os resultados
        for x in resultado:
            latitude_parque = x['latitude']  # seleciono o valor de latitude contido no json
            longitude_parque = x['longitude']  # seleciono o valor de latitude contido no json

            distancia_km = haversine(float(longitude_usuario), float(latitude_usuario), float(longitude_parque), float(
                latitude_parque))  # aplico a latitude e longitude dos dois pontos na formula de haversine para obter a distancia em km
            if (distancia_km <= 5):
                x['distancia em Km'] = round(distancia_km, 2)
                dado.append(x)
        if (not dado):
            return jsonify({'resultado': 'nenhum ponto foi encontrado'}), 404
        else:
            return jsonify({'resultado': dado}), 200  # status code http







@app.route("/users/touristSpotName", methods=['GET'])  # decorator para enviar um ponto turistico com base no nome
def pontos_turisticos_por_nome():
    data = request.json  # solicita o json enviado pelo postman
    return pontos_turisticos_por_nome_logica(data)

def pontos_turisticos_por_nome_logica(data):
    ponto = data.get('spot')  # pega o valor seguido se spot
    tuple=(ponto,)
    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco #a variavel dispensavel n sera utilizada nessa def pois não necessitamos de seu retorno
    cursor[0].execute("SELECT nome, categoria, latitude, longitude FROM tbPontoTuristico WHERE nome = %s",tuple[0])  # faço uma busca no banco pelo ponto turistico informado
    resultado = cursor[0].fetchall()  # comando que faz a busca por toda a informação da tabela
    if(not resultado):
        return jsonify({'message':'O ponto informado não existe'}),404
    else:

        return jsonify({'Pontos':resultado}), 200  # status code http







@app.route("/users/registertouristspot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
def registrar_ponto_turistico():
    data = request.json  # solicita o json enviado pelo postman
    return registrar_ponto_turistico_logica(data)


def registrar_ponto_turistico_logica(data):
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')
    nome_ponto = data.get('nome')  # pega o valor armazenado em "nome"
    latitude_ponto = data.get('latitude')
    longitude_ponto = data.get('longitude')
    categoria_ponto = data.get('categoria')
    categoria_ponto = categoria_ponto.lower().capitalize()
    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco
    autenticacao = verifica_login(email_usuario, senha_usuario)
    if (autenticacao == False):
        return jsonify({'messege': 'login ou senha incorretos'}), 404
    else:
        tuple = (email_usuario,nome_ponto,latitude_ponto,longitude_ponto,categoria_ponto) #a minha variavel tupla armazena todos os valores que serão passados como parâmetro na query
        cursor[0].execute("SELECT nome FROM tbPontoTuristico WHERE nome = %s",tuple[1])  # realizo uma busca para conferir se o ponto a ser cadastrado já existe
        resultado = cursor[0].fetchall()
        if (not resultado):  # se o ponto não existir, permito a criação

            cursor[0].execute("SELECT cod FROM tbCategorias WHERE nome = %s",tuple[4])  # primeiro faço uma busca para ver se a categoria indicada existe
            resultado = cursor[0].fetchall();

            if (not resultado):  # se a categoria informada não existir

                cursor[0].execute("INSERT INTO  tbCategorias (nome) VALUES(%s)",tuple[4])
                cursor[1].commit()  # inserção da categoria no banco
                cursor[0].execute("SELECT cod FROM tbCategorias WHERE nome = %s",tuple[4])  # pego o nome da categoria recém criada para poder continuar o processo e registrar o ponto
                resultado = cursor[
                    0].fetchall();  # armazeno o noem da categoria nova, o que me permitirá entrar no elif da criação
                jsonify({'Mensagem': 'categoria criada com sucesso!'})  # status code http

            elif (resultado):  # se resultado tiver um valor
                cursor[0].execute("SELECT cod FROM tbCategorias WHERE nome = %s",tuple[4])
                resultado = cursor[0].fetchall()
                for x in resultado:  # preciso do for para ler o conjunto de jsons. Ele fará apenas um loop, pois não existe mais de uma categoria com o mesmo nome
                    touppleAux=(int(x['cod']),) #crio essa tupla apenas para lidar com o X
                    cursor[0].execute(
                        "INSERT INTO tbPontoTuristico(nome,categoria,latitude,longitude,criador_ponto) VALUES (%s,%s,%s,%s,%s)",(tuple[1], int(x['cod']), tuple[2], tuple[3], tuple[0]))
                    cursor[1].commit()
                cursor[0].execute("INSERT INTO tbUpvote(nome,quantidade_upvote) VALUES (%s,0)",tuple[1])  # assim que o ponto turistico é registrado, ja é criado uma respectiva tabela em upvote
                cursor[1].commit()
            return jsonify({'messege': 'ponto cadastrado com sucesso!'}), 200
        else:  # se o ponto existir, retorno uma mensagem que impossibilita a criação

            return jsonify({'message': 'esse ponto já foi cadastrado!'}), 403  # proibido






@app.route("/users/commenttouritspot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
def comentar_ponto_turistico():
    data = request.json  # solicita o json enviado pelo postman
    return comentar_ponto_turistico_logica(data)

def comentar_ponto_turistico_logica(data):
    nome_ponto = data.get('nome')  # pega o valor armazenado em "nome"
    comentario_ponto = data.get('comentario')
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')

    tuple=(nome_ponto,comentario_ponto,email_usuario,senha_usuario)

    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco
    autenticacao = verifica_login(email_usuario, senha_usuario)
    if (autenticacao == True):
        cursor[0].execute("SELECT nome FROM tbPontoTuristico WHERE nome = %s",tuple[0])  # faço a busca pelo ponto para ver se ele existe
        resultado = cursor[0].fetchall()  # comando que faz a busca por toda a informação da tabela

        if (
        not resultado):  # se a string não tiver valor dentro, quer dizer que o ponto não existe, se tiver valor, permito que insira um novo comentario
            return jsonify({'message': 'o ponto informado não existe'}), 404
        else:
            cursor[0].execute("INSERT INTO tbComentario (email,nome,descricao) VALUES (%s,%s,%s)",(tuple[2],tuple[0],tuple[1]))  # faço uma busca no banco pelo ponto turistico informado
            cursor[1].commit()

        return jsonify({'message': 'comentário registrado com sucesso!'}), 200  # status code http
    else:
        return jsonify({'message': 'login ou senha incorretos!'}), 404





@app.route("/users/seecommenttouritspot", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
def ver_comentarios_pontos_turisticos():
    data = request.json  # solicita o json enviado pelo postman
    return ver_comentario_ponto_turistico_logica(data)


def ver_comentario_ponto_turistico_logica(data):
    nome_ponto = data.get('nome')  # pega o valor armazenado em "nome"
    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco

    tuple =(nome_ponto,)

    cursor[0].execute("SELECT nome, descricao FROM tbComentario WHERE nome = %s",tuple[0])  # faço a busca pelo ponto para ver se ele existe

    resultado = cursor[0].fetchall()  # comando que faz a busca por toda a informação da tabela
    dado = list()  # lista que armazenará todos os resultados
    if (
    not resultado):  # se a string não tiver valor dentro, quer dizer que o ponto não existe, se tiver valor, permito que insira um novo comentario
        return jsonify({'message': 'o ponto informado não existe!'}), 404
    else:
        for x in resultado:
            dado.append(x)
        return jsonify({'resultado': dado}), 200




@app.route("/users/favoriteaspot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
def favoritar_pontos_turisticos():
    data = request.json  # solicita o json enviado pelo postman
    return favoritar_ponto_turistico_logica(data)


def favoritar_ponto_turistico_logica(data):
    nome_ponto = data.get('nome')  # pega o valor armazenado em "nome"
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')
    tuple = (nome_ponto,email_usuario)
    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco
    cursor[0].execute("SELECT nome  FROM tbPontoTuristico WHERE nome = %s",tuple[0])  # faço a busca pelo ponto para ver se ele existe
    resultado = cursor[0].fetchall()  # comando que faz a busca por toda a informação da tabela
    if (
    not resultado):  # se a string não tiver valor dentro, quer dizer que o ponto não existe, se tiver valor, permito que insira um novo comentario
        return jsonify({'messege': 'o ponto informado não existe!'}), 404
    else:
        autenticador = verifica_login(email_usuario, senha_usuario)
        if (autenticador == False):
            return jsonify({'messege': 'login ou senha incorretos'}), 404
        else:
            cursor[0].execute("INSERT INTO tbPontoFavoritado(email,nome) VALUES(%s,%s)",(tuple[1],tuple[0]))
            cursor[1].commit()
        return jsonify({'messege': 'ponto favoritado com sucesso!'}), 200  # status code http







@app.route("/users/seefavoritespot", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
def ver_ponto_favorito():
    data = request.json  # solicita o json enviado pelo postman
    return ver_ponto_turistico_logica(data)

def ver_ponto_turistico_logica(data):
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')
    tuple=(email_usuario,senha_usuario)
    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco

    autenticador = verifica_login(email_usuario, senha_usuario)
    cursor[0].execute(
        "SELECT email,senha  FROM tbUsuario WHERE email = %s and senha= %s",(tuple[0],tuple[1]))
    resultado = cursor[0].fetchall()
    if (not resultado):
        return jsonify({'messege': 'login ou senha incorretos'}), 404
    else:
        cursor[0].execute("SELECT nome FROM tbPontoFavoritado WHERE email=%s",tuple[0])
        resultado = cursor[0].fetchall()

        return jsonify({'Mensagem': 'sucesso! aqui estão seus pontos!', "ponto": resultado}), 200  # status code http






@app.route("/users/removefavoritespot", methods=['DELETE'])  # rota para enviar um ponto turistico com base no nome
def remover_ponto_favoritado():
    data = request.json  # solicita o json enviado pelo postman
    return remover_ponto_favoritado_logica(data)

def remover_ponto_favoritado_logica(data):
    nome_ponto = data.get('nome')  # pega o valor armazenado em "nome"
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')

    tuple = (nome_ponto,email_usuario,senha_usuario)

    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco
    cursor[0].execute("SELECT nome  FROM tbPontoTuristico WHERE nome = %s",tuple[0])  # faço a busca pelo ponto para ver se ele existe
    resultado = cursor[0].fetchall()  # comando que faz a busca por toda a informação da tabela
    if (
    not resultado):  # se a string não tiver valor dentro, quer dizer que o ponto não existe, se tiver valor, permito que insira um novo comentario
        return jsonify({'messege': 'o ponto informado não existe!'}), 404
    else:
        cursor[0].execute(
            "SELECT email,senha  FROM tbUsuario WHERE email = %s and senha=%s",(tuple[1],tuple[2]))
        resultado = cursor[0].fetchall()
        if (not resultado):
            return jsonify({'messege': 'login ou senha incorretos'}), 404
        else:
            cursor[0].execute(
                "DELETE FROM tbPontoFavoritado WHERE email = %s and nome=%s",(tuple[1],tuple[0]))
            cursor[1].commit()
        return jsonify({'messege': 'ponto removido com sucesso!'}), 200  # status code http









@app.route("/users/upvotespot", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
def upvote_ponto():
    data = request.json  # solicita o json enviado pelo postman
    return upvote_ponto_logica(data)


def upvote_ponto_logica(data):
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')
    nome_ponto = data.get('nome')

    tuple=(email_usuario,senha_usuario,nome_ponto)

    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco

    autenticacao = verifica_login(email_usuario, senha_usuario)
    if (autenticacao == False):
        return jsonify({'messege': 'login ou senha incorretos'}), 404
    else:
        cursor[0].execute("SELECT nome FROM tbPontoTuristico WHERE nome=%s",tuple[2])  ##verifico se o ponto existe
        resultado = cursor[0].fetchall()
        if (not resultado):
            return jsonify(
                {'Mensagem': 'o ponto informado não existe'}), 404  # status code http
        else:
            cursor[0].execute("SELECT quantidade_upvote from tbUpvote where nome = %s",tuple[2])  # pego a quantidade de upvotes do ponto desejado parar poder incrementar

            resultado = cursor[0].fetchall()

            for x in resultado:  # o for é necessário para entrar no json e filtrar o dado
                quantidade_atual_de_upvotes = (x['quantidade_upvote'],)  # armazeno o valor atual dos uvptoes
                cursor[0].execute("UPDATE tbUpvote SET quantidade_upvote = %s WHERE nome = %s",(quantidade_atual_de_upvotes[0] + 1,tuple[2]))  # insiro a quantidade atual com incremento, para registrar o upvote
                cursor[1].commit()
            jsonify({'messege': 'ponto favoritado com sucesso!'})
            return jsonify({'Mensagem': 'upvote registrado com sucesso!'}), 200  # status code http












@app.route("/users/seetouristspotcreatedbyme", methods=['GET'])  # rota para enviar um ponto turistico com base no nome
def ver_pontos_criados_por_mim():
    data = request.json  # solicita o json enviado pelo postman
    return ver_pontos_criados_por_mim_logica(data)

def ver_pontos_criados_por_mim_logica(data):
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')

    tuple = (email_usuario,senha_usuario)

    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco

    autenticador = verifica_login(tuple[0], tuple[1])
    if (autenticador == False):
        return jsonify({'messege': 'login ou senha incorretos'}), 404
    else:
        cursor[0].execute(
            "SELECT nome,categoria,latitude,longitude FROM tbPontoTuristico WHERE criador_ponto= %s",tuple[0])
        resultado = cursor[0].fetchall()
        jsonify({'messege': 'ponto favoritado com sucesso!'})
        return jsonify(
            {'Mensagem': 'sucesso! aqui estão os pontos que você criou!', "ponto": resultado}), 200  # status code http



@app.route("/users/createnewcategorie", methods=['POST'])  # rota para enviar um ponto turistico com base no nome
def criar_nova_categoria():
    data = request.json  # solicita o json enviado pelo postman
    return criar_nova_categoria_logica(data)

def criar_nova_categoria_logica(data):
    email_usuario = data.get('login')
    senha_usuario = data.get('senha')
    nome_categoria = data.get('categoria')

    nome_categoria=nome_categoria.lower().capitalize() #pego a string e deixo toda em minusculo com apenas a primeira letra maisucula, para seguir o padrão do meu banco

    tuple=(email_usuario,senha_usuario,nome_categoria)

    cursor = dbconnection()  # atribuo ao cursor a conexão com o banco
    autenticador = verifica_login(tuple[0], tuple[1])

    if (autenticador == False):
        return jsonify({'messege':'login ou senha incorretos'}),404
    else:
        cursor[0].execute("SELECT nome FROM tbCategorias WHERE nome=%s",tuple[2])
        resultado=cursor[0].fetchall()
        if(not resultado):
            cursor[0].execute("INSERT INTO  tbCategorias (nome) VALUES(%s)",tuple[2])
            cursor[1].commit()
            return jsonify({'Mensagem':'categoria criada com sucesso!'}), 200  # status code http
        else:

            return jsonify({'Mensagem': 'a categoria já existe!'}), 204  # status code http