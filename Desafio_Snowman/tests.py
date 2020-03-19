import unittest,pymysql
from use_cases_turismo import *
from flask_api import status


class test_for_tourist_points(unittest.TestCase):

        
    def test_register_tourist_point(self):
        data = {
            "login": "lucas_giovanini",
            "senha": "lucasgiovanini",
            "nome": "praça do Cassiano1",
            "latitude": 00,
            "longitude": 00,
            "categoria": "parque"
        }
        response = registrar_ponto_turistico_logica(data) #retorna o meu json e
        # a função assertAlmostEqual tem o primeiro parâmetro como o valor atual e o segundo como o valor correto

        self.assertEqual(response[1],status.HTTP_200_OK)  # como a função retorna o json de dados e o status code, passo a posição 1 da tupla para pegar o status code

if __name__ == '__main__':
    unittest.main()