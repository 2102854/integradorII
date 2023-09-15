"""
Módulo Usuários
"""
from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from usuario import Usuario
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

usersRoute = Blueprint('usersRoute', __name__)

# Recupera todos os Usuários Cadastrados no Banco de Dados
@usersRoute.route('/api/usuarios', methods=['GET'])
@Auth.token_required
def get_usuarios(usuario_id):
    try:
        usuarios = Usuario.get_usuarios(usuario_id)
        u = dict_helper_list(usuarios) 
        return jsonify(usuarios = u)            
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401

# Recupera os dados do Usuário
@usersRoute.route('/api/usuarios/<int:id>', methods=['GET'])
@Auth.token_required
def get_usuario_id(usuario_id, id:int):
    try:
        usuario = Usuario.get_usuario_id(usuario_id, id)
        u = dict_helper_list(usuario) 
        return jsonify(usuario = u)            
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401    