##########################################################
#                    Módulo Segurança                    #
# ######################################################## 

from flask import Blueprint
import locale
from dict_helper import dict_helper_list, dict_helper_obj
from seguranca.autenticacao import Auth
from seguranca.token import Token
from flask import request, jsonify, make_response

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

authRoute = Blueprint('authRoute', __name__)


# Realiza o logout do usuário
@authRoute.route('/api/logout', methods=['PUT'])
def logout():
    json_request = request.get_json() 
    Token.logout(json_request['token'])
    response = jsonify({'message': 'logout ok'})
    return response, 204                


# Realiza a autenticação do usuário
@authRoute.route('/api/login', methods=['POST'])
def login():    
    token = None
    if 'x-access-token' in request.headers:
        try: 
            token = request.headers['x-access-token'] 
            Token.valida_token(token)
            return make_response(jsonify({'token' : token.decode('UTF-8')}), 200)
        except Exception as err:
            return make_response('Não foi possível verificar', 401, {'WWW-Authenticate' : 'Basic realm =Token inválido'})  
    else:
        try:
            success: bool = False
            msg: str = None
                    
            if request.headers['Content-Type'] == 'application/json':
                # Executa a validação dos dados informados via json request
                json_request = request.get_json()                 
                success, msg, authorization = Auth.login(json_request['email'], json_request['senha'])
            else:    
                # Executa a validação dos dados informados via body form
                success, msg, authorization = Auth.login(request.form['email'], request.form['senha'])
            
            if success:
                return make_response(authorization, 200)
            else:
                response = jsonify({'message err': f'{msg}'})
                return response, 401                
                
        except Exception as err:
            return make_response('Dados incorretos', 401, {'WWW-Authenticate' : 'Basic realm =Dados incorretos'}) 
        
# Verifica se o token permanece válido
@authRoute.route('/api/token_validate', methods=['GET','POST'])
def tokenValidate():  
    token = None
    if 'x-access-token' in request.headers:
        try: 
            token = request.headers['x-access-token'] 
            Token.valida_token(token)
            response = jsonify({'token' : 'VALIDO'})
            return response, 200   
           
        except Exception as err:
            response = jsonify({'message err': f'{err}'})
            return response, 401   
          