"""
Módulo Tipo de Doenças
"""
from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from tipo_doenca import Tipo_Doenca
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

diseaseTypesRoute = Blueprint('diseaseTypesRoute', __name__)

#Recupera todos os tipos de doenças cadastrados
@diseaseTypesRoute.route("/api/disease_types")
@Auth.token_required
def get_tipoDoenca(usuario_id: int):
    try:
        tipoDoencas = Tipo_Doenca.get_tipoDoenca(usuario_id)
        td = dict_helper_list(tipoDoencas)
        return make_response(td, 200)          
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Recupera o tipo de doenca pelo id
@diseaseTypesRoute.route('/api/disease_types/<int:tipo_doenca_id>', methods=['GET'])
@Auth.token_required
def get_tipoDoenca_id(usuario_id: int, tipo_doenca_id: int):
    try:
        tipoDoenca = Tipo_Doenca.get_tipoDoenca_id(usuario_id, tipo_doenca_id)
        td = dict_helper_obj(tipoDoenca) 
        return make_response(td, 200)      
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Adiciona um novo tipo de doença no Banco de Dados
@diseaseTypesRoute.route('/api/disease_types/add', methods=['POST'])
@Auth.token_required
def add_tipoDoenca(usuario_id: int):
    try:
        # Recupera o objeto passado como parametro
        atipoDoenca = request.get_json()
        atipoDoenca = Tipo_Doenca.add_tipoDoenca(usuario_id, atipoDoenca)
        td = dict_helper_obj(atipoDoenca)
        return jsonify(tipoDoenca = td)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404 

# Edita um tipo de doença já cadastrado no Banco de Dados
@diseaseTypesRoute.route('/api/disease_types/<int:tipo_doenca_id>', methods=['PUT'])
@Auth.token_required
def update_tipoDoenca(usuario_id: int, tipo_doenca_id: int):
    try:
        # Recupera o objeto passado como parametro
        utipoDoenca = request.get_json()
        tipoDoenca = Tipo_Doenca.update_tipoDoenca(usuario_id, tipo_doenca_id, utipoDoenca)
        td = dict_helper_obj(tipoDoenca)
        return jsonify(tipoDoenca = td)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401          