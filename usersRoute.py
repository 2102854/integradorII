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
        return make_response(u, 200)            
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

# Atualiza a senha do usuario no banco de dados
@usersRoute.route('/api/usuarios/change_password', methods=['POST'])
@Auth.token_required
def change_password(usuario_id):
    try:
        obj = request.get_json()                
        ok = Usuario.change_password(usuario_id, int(obj['user_id_to_be_changed']), obj['old_pass'], obj['new_pass'], obj['new_pass_confirmed'])
        return jsonify(changed = ok)            
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401    

# Atualiza a permissao do usuario
@usersRoute.route('/api/usuarios/change_user_permission', methods=['POST'])
@Auth.token_required
def change_user_permission(usuario_id):
    try:
        obj = request.get_json()                
        ok = Usuario.change_user_permission(usuario_id, int(obj['user_id']), obj['permissao_id'])
        return jsonify(changed = ok)            
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401 
    

    # Adiciona uma usuário no Banco de Dados
@usersRoute.route('/api/usuarios/add', methods=['POST'])
@Auth.token_required
def add_usuarios(usuario_id: int):
    try:
        # Recupera o objeto passado como parametro
        ausuarios = request.get_json()
        usuario = Usuario.add_usuarios(usuario_id, ausuarios)
        c = dict_helper_obj(usuario)
        return jsonify(usuario = c)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404
    
    # Atualiza os dados do Usuário
@usersRoute.route('/api/usuarios/update/<int:id>', methods=['PUT'])
@Auth.token_required
def update_usuarios(usuario_id: int, id: int):
    try:
        # Recupera o objeto passado como parametro
        uusuario = request.get_json()
        usuario = Usuario.update_usuarios(usuario_id, id, uusuario)
        p = dict_helper_obj(usuario)
        return jsonify(usuario = p)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401
    

