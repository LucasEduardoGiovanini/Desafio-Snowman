from flask import request
def adapter_tourist_spot():
    data = request.json
    nome_ponto = data.get('nome')
    latitude_ponto = data.get('latitude')
    longitude_ponto = data.get('longitude')
    categoria_ponto = data.get('categoria')
    foto_ponto = data.get('foto')
    return nome_ponto,latitude_ponto,longitude_ponto,categoria_ponto,foto_ponto
