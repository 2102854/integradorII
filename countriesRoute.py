##########################################################
#                       Módulo Países                    #
# ########################################################  

from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from pais import Pais
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

countriesRoute = Blueprint('countriesRoute', __name__)
     
# Recupera todos os Países Cadastrados no Banco de Dados
@countriesRoute.route('/api/paises', methods=['GET'])
@Auth.token_required
def get_paises(usuario_id):
    try:
        paises = Pais.get_paises(usuario_id)
        p = dict_helper_list(paises) 
        #return jsonify(paises = p) 
        return make_response(p, 200)
                    
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401

# Recupera o País pelo id
@countriesRoute.route('/api/paises/<int:pais_id>', methods=['GET'])
@Auth.token_required
def get_pais_id(usuario_id: int, pais_id: int):
    try:
        pais = Pais.get_pais_id(usuario_id, pais_id)
        p = dict_helper_obj(pais) 
        return make_response(p, 200)         
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401        

# Adiciona um Pais no Banco de Dados
@countriesRoute.route('/api/paises/add', methods=['POST'])
@Auth.token_required
def add_pais(usuario_id: int):
    try:
        # Recupera o objeto passado como parametro
        apais = request.get_json()        
        pais = Pais.add_pais(usuario_id, apais)
        p = dict_helper_obj(pais)
        return jsonify(pais = p)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401

# Edita um Pais já cadastrado no Banco de Dados
@countriesRoute.route('/api/paises/update/<int:pais_id>', methods=['PUT'])
@Auth.token_required
def update_pais(usuario_id: int, pais_id: int):
    try:
        # Recupera o objeto passado como parametro
        upais = request.get_json()
        pais = Pais.update_pais(usuario_id, pais_id, upais)
        p = dict_helper_obj(pais)
        return jsonify(pais = p)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401