from flask import Flask
from flask_restful import Api, Resource, reqparse

from estado import Estado
from pais import Pais

from seguranca.permissoes import Permissao
from seguranca.business_exception import BusinessException

class EstadosResource(Resource):
    #Todos os estados
    def get(self, estados):
        try:
            estados_instance = Estados()
            result = estados_instance.get_estados(usuarios_id)
            return result
        except BusinessException as err:
            abort(400, description=str(err))

    #Estado Especifico
    def get(self, estado):
        estado_instance = Estado()
        result = estado_instance.get_estado(usuario_id, estado_id, permissao_pai)
        return result

    #Adicionar estado
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('pais_id', type=str, required=True)
        parser.add_argument('nome', type=str, required=True)
        parser.add_argument('sigla', type=str, required=True)
        try:
