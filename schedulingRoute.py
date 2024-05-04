"""
Módulo Agendamento
"""
from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from agendamento import Agendamento
from motorista import Motorista
from veiculo import Veiculo
from hospital import Hospital
from tipo_doenca import Tipo_Doenca
from tipo_remocao import Tipo_Remocao
from tipo_encaminhamento import Tipo_Encaminhamento
from paciente import Paciente
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

schedulingRoute = Blueprint('schedulingRoute', __name__)

@schedulingRoute.route("/api/agendamentos/data_form")
@Auth.token_required
def get_data_form(usuario_id: int):
    try:
        paciente = Paciente.get_pac(usuario_id)
        motorista = Motorista.get_motoristas(usuario_id)
        veiculo = Veiculo.get_veiculos(usuario_id)
        tipo_doenca = Tipo_Doenca.get_tipoDoenca(usuario_id)
        tipo_remocao = Tipo_Remocao.get_tipo_remocao(usuario_id)
        tipo_encaminhamento = Tipo_Encaminhamento.get_tipo_encaminhamento(usuario_id)
        hospital = Hospital.get_hospitais(usuario_id)
        
        td = dict_helper_list(tipo_doenca)
        te = dict_helper_list(tipo_encaminhamento)
        tr = dict_helper_list(tipo_remocao)
        m = dict_helper_list(motorista)
        v = dict_helper_list(veiculo)
        h = dict_helper_list(hospital)
        p = dict_helper_list(paciente)
                
        return jsonify(
            paciente = p, hospital = h, motorista = m, veiculo = v, 
            tipo_encaminhamento = te, tipoDoenca = td, tipo_remocao = tr

        )    
    
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404        

#Abre a página de agendamentos
@schedulingRoute.route("/api/agendamentos")
@Auth.token_required
def get_agendamentos(usuario_id: int):
    try:
        agendamentos = Agendamento.get_agendamentos(usuario_id)
        return make_response(agendamentos, 200)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401
    
#Recupera agendamento pelo id
@schedulingRoute.route('/api/agendamentos/<int:agendamento_id>', methods=['GET'])
@Auth.token_required
def get_agendamentos_id(usuario_id: int, agendamento_id: int):
    try:
        agendamentos = Agendamento.get_agendamentos_id(usuario_id, agendamento_id)
        p = dict_helper_obj(agendamentos) 
        return make_response(p, 200)
        #return make_response(agendamentos, 200)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401

    
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
    
# Edita um Usuario já cadastrado no Banco de Dados
@schedulingRoute.route('/api/agendamentos/update/<int:agendamento_id>', methods=['PUT'])
@Auth.token_required
def update_agendamento(usuario_id: int, agendamento_id: int):
    try:
        # Recupera o objeto passado como parametro
        uagendamento = request.get_json()
        agendamento = Agendamento.update_agendamento(usuario_id, agendamento_id, uagendamento)
        p = dict_helper_obj(agendamento)
        return jsonify(agendamento = p)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401