"""
Módulo Motoristas
"""
from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from motorista import Motorista
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

driversRoute = Blueprint('driversRoute', __name__)

#Abre a página de motoristas
@driversRoute.route("/api/motoristas")
@Auth.token_required
def get_motoristas(usuario_id: int):
    try:
        motorista = Motorista.get_motoristas(usuario_id)
        m = dict_helper_list(motorista)
        return make_response(m, 200)    
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Recupera o motorista pelo id
@driversRoute.route('/api/motoristas/<int:motorista_id>', methods=['GET'])
@Auth.token_required
def get_motorista_id(usuario_id: int, motorista_id: int):
    try:
        motorista = Motorista.get_motorista_id(usuario_id, motorista_id)
        m = dict_helper_obj(motorista)
        return make_response(m, 200)   
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Adiciona um Motorista no Banco de Dados
@driversRoute.route('/api/motoristas/add', methods=['POST'])
@Auth.token_required
def add_motorista(usuario_id: int):
    try:
        # Recupera o objeto passado como parametro
        amotorista = request.get_json()
        motorista = Motorista.add_motorista(usuario_id, amotorista)
        m = dict_helper_obj(motorista)
        return jsonify(motorista = m)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Edita um Motorista já cadastrado no Banco de Dados
@driversRoute.route('/api/motoristas/update/<int:motorista_id>', methods=['PUT'])
@Auth.token_required
def update_motorista(usuario_id: int, motorista_id: int):
    try:
        # Recupera o objeto passado como parametro
        umotorista = request.get_json()
        motorista = Motorista.update_motorista(usuario_id, motorista_id, umotorista)
        m = dict_helper_obj(motorista)
        return jsonify(motorista = m)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401