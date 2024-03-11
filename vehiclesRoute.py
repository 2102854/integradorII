##########################################################
#                      Módulo Veículos                   #
# ########################################################

from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from veiculo import Veiculo
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

vehiclesRoute = Blueprint('vehiclesRoute', __name__)

#Abre a página de veículos
@vehiclesRoute.route("/api/veiculos")
@Auth.token_required
def get_veiculos(usuario_id: int):
    try:
        veiculo = Veiculo.get_veiculos(usuario_id)
        v = dict_helper_list(veiculo)
        return make_response(v, 200)    
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Recupera o veículo pelo id
@vehiclesRoute.route('/api/veiculos/<int:veiculo_id>', methods=['GET'])
@Auth.token_required
def get_veiculo_id(usuario_id: int, veiculo_id: int):
    try:
        veiculo = Veiculo.get_veiculo_id(usuario_id, veiculo_id)
        v = dict_helper_obj(veiculo) 
        return make_response(v, 200)    
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Adiciona um Veículo no Banco de Dados
@vehiclesRoute.route('/api/veiculos/add', methods=['POST'])
@Auth.token_required
def add_veiculo(usuario_id: int):
    try:
        # Recupera o objeto passado como parametro
        aveiculo = request.get_json()
        veiculo = Veiculo.add_veiculo(usuario_id, aveiculo)
        v = dict_helper_obj(veiculo)
        return jsonify(veiculo = v)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404

# Edita um Veículo já cadastrado no Banco de Dados
@vehiclesRoute.route('/api/veiculos/update/<int:veiculo_id>', methods=['PUT'])
@Auth.token_required
def update_veiculo(usuario_id: int, veiculo_id: int):
    try:
        # Recupera o objeto passado como parametroCD SCRIPTS
        uveiculo = request.get_json()
        veiculo = Veiculo.update_veiculo(usuario_id, veiculo_id, uveiculo)
        v = dict_helper_obj(veiculo)
        return jsonify(veiculo = v)
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401     