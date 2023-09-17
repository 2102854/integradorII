"""
Módulo Tipo Encaminhamento
"""
from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from tipo_encaminhamento import Tipo_Encaminhamento
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

patient_referralRoute = Blueprint('patient_referralRoute', __name__)

#Recupera todos os tipos de doenças cadastrados
@patient_referralRoute.route("/api/patient_referral")
@Auth.token_required
def get_tipoDoenca(usuario_id: int):
    try:
        tipoEncaminhamento = Tipo_Encaminhamento.get_tipo_encaminhamento(usuario_id)
        te = dict_helper_list(tipoEncaminhamento)
        return make_response(te, 200)          
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Recupera o tipo de doenca pelo id
@patient_referralRoute.route('/api/patient_referral/<int:tipo_doenca_id>', methods=['GET'])
@Auth.token_required
def get_tipoDoenca_id(usuario_id: int, tipo_encaminhamento_id: int):
    try:
        tipoEncaminhamento = Tipo_Encaminhamento.get_tipo_encaminhamento_id(usuario_id, tipo_encaminhamento_id)
        te = dict_helper_obj(tipoEncaminhamento) 
        return make_response(te, 200)      
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Adiciona um novo tipo de doença no Banco de Dados
@patient_referralRoute.route('/api/patient_referral/add', methods=['POST'])
@Auth.token_required
def add_tipoDoenca(usuario_id: int):
    try:
        # Recupera o objeto passado como parametro
        atipoEncaminhamento = request.get_json()
        tipoEncaminhamento = Tipo_Encaminhamento.add_tipo_encaminhamento(usuario_id, atipoEncaminhamento)
        te = dict_helper_obj(tipoEncaminhamento)
        return jsonify(tipoEncaminhamento = te)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404 

# Edita um tipo de doença já cadastrado no Banco de Dados
@patient_referralRoute.route('/api/patient_referral/<int:tipo_doenca_id>', methods=['PUT'])
@Auth.token_required
def update_tipoDoenca(usuario_id: int, tipo_doenca_id: int):
    try:
        # Recupera o objeto passado como parametro
        utipoEncaminhamento = request.get_json()
        tipoEncaminhamento = Tipo_Encaminhamento.update_tipoDoenca(usuario_id, tipo_doenca_id, utipoEncaminhamento)
        te = dict_helper_obj(tipoEncaminhamento)
        return jsonify(tipoEncaminhamento = te)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401          