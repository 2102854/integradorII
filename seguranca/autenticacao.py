from config import parameters
from flask import request, jsonify, make_response
import jwt 
from functools import wraps 
from werkzeug.security import check_password_hash
from usuario import Usuario
from seguranca.business_exception import BusinessException
from seguranca.token import Token

class Auth(): 
    def token_required(f): 
        @wraps(f) 
        def decorated(*args, **kwargs): 
            token = None
            if 'x-access-token' in request.headers: 
                token = request.headers['x-access-token'] 
            if not token: 
                return jsonify({'message' : 'Token não informado'}), 401
            try: 
                # Valida o token informado
                Token.valida_token(token)
                
                # Decodifica o Token
                chave_publica = jwt.decode(token, parameters['SECRET_KEY']) 
                
                # Recupera os dados do usuário e executa validações
                usuario = Usuario.get_usuario_by_chave_publica(chave_publica)
                if not usuario:
                    return jsonify({'message' : 'Usuário Bloqueado!'}), 401
                if not usuario.ativo:
                    return jsonify({'message' : 'Usuário Bloqueado!'}), 401                
                
            except Exception as err: 
                return jsonify({'message' : err}), 401
        
            return  f(usuario.usuario_id, *args, **kwargs)    
         
        return decorated

    def login(email, senha): 
        try:           
            # Verifica se as informações foram passadas corretamente para executar o login
            print('aqui')
            if not email or not senha: 
                print('aqui1')
                return make_response('Não foi possível verificar', 401, {'WWW-Authenticate' : 'Basic realm =E-mail ou Senha não é válido'})
        
            # Valida o e-mail informado
            print('aqui2')
            if not Usuario.email_eh_valido(email):
                print('aqui3')
                return make_response('Não foi possível verificar', 401, {'WWW-Authenticate' : 'Basic realm =E-mail não é Válido'})
            
            print('aqui4')
            usuario = Usuario.get_usuario_by_email(email)             
            if not usuario:
                print('aqui5')
                return make_response('Não foi possível verificar', 401, {'WWW-Authenticate' : 'Basic realm =E-mail ou Senha não é válido'}) 

            # Valida a senha do Usuário
            if not check_password_hash(usuario.senha, senha): 
                return make_response('Não foi possível verificar', 401, {'WWW-Authenticate' : 'Basic realm =E-mail ou Senha não é válido'})
            
            # Gera o Token de Autenticação
            token = Token.add_token(usuario.usuario_id, usuario.chave_publica)

            return token 

        except Exception:
            return make_response('Não foi possível verificar', 401, {'WWW-Authenticate' : 'Basic realm =Erro desconhecido'})