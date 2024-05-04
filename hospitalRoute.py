"""
Módulo Hospitais
"""

from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from hospital import Hospital
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

hospitalRoute = Blueprint('hospitalRoute', __name__)

#Abre a página de hospitais
@hospitalRoute.route("/api/hospitais")
@Auth.token_required
def get_hospitais(usuario_id: int):
    try:
        hospital = Hospital.get_hospitais(usuario_id)
        e = dict_helper_list(hospital)
        return make_response(e, 200)    
    
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Recupera o hospital pelo id
@hospitalRoute.route('/api/hospitais/<int:hospital_id>', methods=['GET'])
@Auth.token_required
def get_hospital_id(usuario_id: int, hospital_id: int):
    try:
        hospital = Hospital.get_hospital_id(usuario_id, hospital_id)
        e = dict_helper_list(hospital)
        return make_response(e, 200)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Adiciona um Hospital no Banco de Dados
@hospitalRoute.route('/api/hospitais/add', methods=['POST'])
@Auth.token_required
def add_hospital(usuario_id: int):
    try:
        # Recupera o objeto passado como parametro
        ahospital = request.get_json()
        hospital = Hospital.add_hospital(usuario_id, ahospital)
        c = dict_helper_obj(hospital)
        return jsonify(hospital = c)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404
    
# Edita um Hospital já cadastrado no Banco de Dados
@hospitalRoute.route('/api/hospitais/update/<int:hospital_id>', methods=['PUT'])
@Auth.token_required
def update_hospital(usuario_id: int, hospital_id: int):
    try:
        # Recupera o objeto passado como parametro
        uhospital = request.get_json()
        hospital = Hospital.update_hospital(usuario_id, hospital_id, uhospital)
        h = dict_helper_obj(hospital)
        return jsonify(hospital = h)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401    