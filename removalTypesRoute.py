"""
Módulo Tipo de Remoção
"""
from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from tipo_remocao import Tipo_Remocao
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

removalTypesRoute = Blueprint('removalTypesRoute', __name__)

# Abre a página de tipo de remoção
@removalTypesRoute.route("/api/tipo_remocao")
@Auth.token_required
def get_tipo_remocao(usuario_id: int):
    try:
        tipo_remocao = Tipo_Remocao.get_tipo_remocao(usuario_id)
        e = dict_helper_list(tipo_remocao)
        return make_response(e, 200) 
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Recupera o tipo de remoção pelo id
@removalTypesRoute.route('/api/tipo_remocao/<int:tipo_remocao_id>', methods=['GET'])
@Auth.token_required
def get_tipo_remocao_id(usuario_id: int, tipo_remocao_id: int):
    try:
        tipo_remocao = Tipo_Remocao.get_tipo_remocao_id(usuario_id, tipo_remocao_id)
        e = dict_helper_obj(tipo_remocao)
        return make_response(e, 200) 
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Adiciona um tipo de remoção no Banco de Dados
@removalTypesRoute.route('/api/tipo_remocao/add', methods=['POST'])
@Auth.token_required
def add_tipo_remocao(usuario_id: int):
    try:
        # Recupera o objeto passado como parametro
        atiporemocao = request.get_json()
        tipo_remocao = Tipo_Remocao.add_tipo_remocao(usuario_id, atiporemocao)
        c = dict_helper_obj(tipo_remocao)
        return jsonify(tipo_remocao=c)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Edita um Tipod e remoção já cadastrado no Banco de Dados
@removalTypesRoute.route('/api/tipo_remocao/update', methods=['POST'])
@Auth.token_required
def update_tipo_remocao(usuario_id: int, tipo_remocao_id: int):
    try:
        # Recupera o objeto passado como parametro
        utiporemocao = request.get_json()
        tipo_remocao = Tipo_Remocao.update_tipo_remocao(usuario_id, tipo_remocao_id ,utiporemocao)
        p = dict_helper_obj(tipo_remocao)
        return jsonify(tipo_remocao=p)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401


