##########################################################
#                      Módulo Estados                    #
# ########################################################  

from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from estado import Estado
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

statesRoute = Blueprint('statesRoute', __name__)

#Abre a página de estados
@statesRoute.route("/api/estados")
@Auth.token_required
def get_estados(usuario_id):
    try:
        estados = Estado.get_estados(usuario_id)
        #e = dict_helper_list(estados) 
        return make_response(estados, 200)      

    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401

# Recupera o estado pelo id
@statesRoute.route('/api/estados/<int:estado_id>', methods=['GET'])
@Auth.token_required
def get_estado_id(usuario_id: int, estado_id: int):
    try:
        estado = Estado.get_estado_id(usuario_id, estado_id)
        e = dict_helper_obj(estado) 
        return make_response(e, 200)      
               
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401       

# Adiciona um novo estado no Banco de Dados
@statesRoute.route('/api/estados/add', methods=['POST'])
@Auth.token_required
def add_estados(usuario_id: int):
    try:
        # Recupera o objeto passado como parametro
        aestado = request.get_json()        
        estado = Estado.add_estado(usuario_id, aestado)
        e = dict_helper_obj(estado)
        return jsonify(estado = e)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401     

# Edita um Estado já cadastrado no Banco de Dados
@statesRoute.route('/api/estados/update/<int:estado_id>', methods=['PUT'])
@Auth.token_required
def update_estado(usuario_id: int, estado_id: int):
    try:
        # Recupera o objeto passado como parametro
        uestado = request.get_json()
        estado = Estado.update_estado(usuario_id, estado_id, uestado)
        e = dict_helper_obj(estado)
        return jsonify(estado = e)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401