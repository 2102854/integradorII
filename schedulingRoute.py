"""
Módulo Agendamento
"""
from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from agendamento import Agendamento
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

schedulingRoute = Blueprint('schedulingRoute', __name__)

#Abre a página de agendamentos
@schedulingRoute.route("/api/agendamentos")
@Auth.token_required
def get_agendamentos(usuario_id: int):
    try:
        agendamentos = Agendamento.get_agendamentos(usuario_id)
        return make_response(agendamentos, 200)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404
    
# Adiciona uma agendamento no Banco de Dados
@schedulingRoute.route('/api/agendamentos/add', methods=['POST'])
@Auth.token_required
def add_agendamento(usuario_id: int):
    try:
        # Recupera o objeto passado como parametro
        aagendamento = request.get_json()
        agendamento = Agendamento.add_agendamento(usuario_id, aagendamento)
        c = dict_helper_obj(agendamento)
        return jsonify(agendamento = c)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404