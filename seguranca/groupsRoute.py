"""
Módulo Grupos
"""
from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from usuario import Usuario
from seguranca.autenticacao import Auth
from seguranca.grupo import Grupo
from seguranca.grupo_permissao import Grupo_Permissao

from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

groupsRoute = Blueprint('groupsRoute', __name__)

# Recupera todos os Grupos Cadastrados no Banco de Dados
@groupsRoute.route('/api/grupos', methods=['GET'])
@Auth.token_required
def get_grupos(usuario_id):
    try:
        grupos = Grupo.get_grupos(usuario_id)
        g = dict_helper_list(grupos) 
        return jsonify(grupos = g)            
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401

# Recupera de um Grupo de Usuários
@groupsRoute.route('/api/grupos/<int:grupo_id>', methods=['GET'])
@Auth.token_required
def get_grupo_id(usuario_id: int, grupo_id: int):
    try:
        grupo = Grupo.get_grupo_id(usuario_id, grupo_id)
        g = dict_helper_list(grupo) 
        return jsonify(grupo = g)            
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401    

# Adiciona um Grupo no Banco de Dados
@groupsRoute.route('/api/grupos/add', methods=['POST'])
@Auth.token_required
def add_grupo(usuario_id):
    try:
        # Recupera o objeto passado como parametro
        agrupo = request.get_json()        
        grupo = Grupo.add_grupo(usuario_id, agrupo)
        g = dict_helper_obj(grupo)
        return jsonify(grupo = g)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401

# Edita um Grupo já cadastrado no Banco de Dados
@groupsRoute.route('/api/grupos/update', methods=['POST'])
@Auth.token_required
def update_grupo(usuario_id):
    try:
        # Recupera o objeto passado como parametro
        ugrupo = request.get_json()
        grupo = Grupo.update_grupo(usuario_id, ugrupo)
        g = dict_helper_obj(grupo)
        return jsonify(grupo = g)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401
    
# Recupera as permissões associadas a um Grupo de Usuários
@groupsRoute.route('/api/grupos/permissoes/<int:grupo_id>', methods=['GET'])
@Auth.token_required
def get_permissoes_do_grupo(usuario_id: int, grupo_id: int):
    try:
        grupo_permissoes = Grupo_Permissao.get_permissoes_do_grupo(usuario_id, grupo_id)
        gp = dict_helper_list(grupo_permissoes) 
        return jsonify(grupo_permissao = gp)            
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401  