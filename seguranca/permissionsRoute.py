"""
Módulo Permissoes
"""
from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from seguranca.permissoes import Permissao
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

permissionsRoute = Blueprint('permissionsRoute', __name__)

# Recupera todas as permissoes
@permissionsRoute.route('/api/permissions', methods=['GET'])
@Auth.token_required
def get_permissions(usuario_id: int):
    try:
        permissions = Permissao.get_permissoes(usuario_id)
        p = dict_helper_list(permissions) 
        return make_response(p, 200)          
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Recupera todas as permissoes
@permissionsRoute.route('/api/permissions/<int:id>', methods=['GET'])
@Auth.token_required
def get_permissoes_usuario(usuario_id: int, id: int):
    try:
        permissions = Permissao.get_permissoes_usuario(usuario_id, id)
        p = dict_helper_list(permissions) 
        return make_response(p, 200)          
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404    
