"""
Módulo Dashboard
"""
from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from dashboard import Dashboard
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

dashboardRoute = Blueprint('dashboardRoute', __name__)

# Recupera as informações para apresentação no dashboard
@dashboardRoute.route('/api/dashboard', methods=['GET'])
@Auth.token_required
def get_dashboard(usuario_id):
    try:
        dashboard = Dashboard.get_dados(usuario_id)
        #return jsonify(paises = p) 
        return make_response(dashboard, 200)
                    
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401