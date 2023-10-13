"""
Módulo Cidades
"""
from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from cidade import Cidade
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

citiesRoute = Blueprint('citiesRoute', __name__)

#Abre a página de cidades
@citiesRoute.route("/api/cidades")
@Auth.token_required
def get_cidades(usuario_id: int):
    try:
        cidades = Cidade.get_cidades(usuario_id)
        return make_response(cidades, 200)          
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Recupera a cidade pelo id
@citiesRoute.route('/api/cidades/<int:cidade_id>', methods=['GET'])
@Auth.token_required
def get_cidade_id(usuario_id: int, cidade_id: int):
    try:
        cidade = Cidade.get_cidade_id(usuario_id, cidade_id)
        c = dict_helper_obj(cidade) 
        return make_response(c, 200)      
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Adiciona uma Cidade no Banco de Dados
@citiesRoute.route('/api/cidades/add', methods=['POST'])
@Auth.token_required
def add_cidade(usuario_id: int):
    try:
        # Recupera o objeto passado como parametro
        acidade = request.get_json()
        cidade = Cidade.add_cidade(usuario_id, acidade)
        c = dict_helper_obj(cidade)
        return jsonify(cidade = c)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404 

# Edita uma Cidade já cadastrada no Banco de Dados
@citiesRoute.route('/api/cidades/<int:cidade_id>', methods=['PUT'])
@Auth.token_required
def update_cidade(usuario_id: int, cidade_id: int):
    try:
        # Recupera o objeto passado como parametro
        ucidade = request.get_json()
        cidade = Cidade.update_cidade(usuario_id, cidade_id, ucidade)
        c = dict_helper_obj(cidade)
        return jsonify(cidade = c)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401          