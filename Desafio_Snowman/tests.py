import unittest, use_cases_turismo
from flask_api import status


class test_for_tourist_points(unittest.TestCase):

    def test_register_tourist_point(self):

        data = {
            "login": "lucas_giovanini",
            "senha": "lucasgiovanini",
            "nome": "praça do Cassiano",
            "latitude": 00,
            "longitude": 00,
            "categoria": "parque"
        }
        response = use_cases_turismo.registrar_ponto_turistico() #retorna o meu json e
        # a função assertAlmostEqual tem o primeiro parâmetro como o valor atual e o segundo como o valor correto
        self.assertAlmostEqual(response[1],status.HTTP_200_OK)  # como a função retorna o json de dados e o status code, passo a posição 1 da tupla para pegar o status code
