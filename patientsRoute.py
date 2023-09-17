"""
Módulo Pacientes
"""

from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from paciente import Paciente
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

patientsRoute = Blueprint('patientsRoute', __name__)

#Abre a página de pacientes
@patientsRoute.route("/api/pacientes")
@Auth.token_required
def get_pacientes(usuario_id: int):
    try:
        paciente = Paciente.get_pacientes(usuario_id)
        return make_response(paciente, 200)  
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Recupera o paciente pelo id
@patientsRoute.route('/api/pacientes/<int:paciente_id>', methods=['GET'])
##@Auth.token_required
def get_paciente_id(paciente_id: int):
    try:
        usuario_id = 1
        paciente = Paciente.get_paciente_id(usuario_id, paciente_id)
        e = dict_helper_list(paciente)
        return jsonify(paciente = e)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Adiciona um Veículo no Banco de Dados
@patientsRoute.route('/api/pacientes/add', methods=['POST'])
##@Auth.token_required
def add_paciente():
    try:
        usuario_id = 1
        # Recupera o objeto passado como parametro
        apaciente = request.get_json()
        paciente = Paciente.add_paciente(usuario_id, apaciente)
        c = dict_helper_obj(paciente)
        return jsonify(paciente = c)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Edita um Paciente já cadastrado no Banco de Dados
@patientsRoute.route('/api/pacientes/update', methods=['POST'])
#@Auth.token_required
def update_paciente():
    try:
        usuario_id = 1
        # Recupera o objeto passado como parametro
        upaciente = request.get_json()
        paciente = Paciente.update_paciente(usuario_id, upaciente)
        p = dict_helper_obj(paciente)
        return jsonify(paciente = p)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401