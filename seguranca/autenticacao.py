from config import parameters
from flask import request, jsonify, make_response
import jwt 
from functools import wraps 
from werkzeug.security import check_password_hash
from usuario import Usuario
from seguranca.business_exception import BusinessException
from seguranca.token import Token
from seguranca.usuario_permissao import Usuario_Permissao

class Auth(): 
    def token_required(f): 
        @wraps(f) 
        def decorated(*args, **kwargs): 
            token = None
            print(request.headers)
            if 'x-access-token' in request.headers: 
                token = request.headers['x-access-token'] 
            if not token:                 
                return jsonify({'message' : 'Token não informado'}), 401
            try: 
                
                # Valida o token informado
                Token.valida_token(token)   

                # Decodifica o Token
                payload = jwt.decode(token, parameters['SECRET_KEY'], algorithms=["HS256"]) 
                chave_publica = payload['chave_publica']

                # Recupera os dados do usuário e executa validações
                usuario = Usuario.get_usuario_by_chave_publica(chave_publica)
                if not usuario:
                    return jsonify({'message' : 'Usuário Bloqueado!'}), 401
                if not usuario.ativo:
                    return jsonify({'message' : 'Usuário Bloqueado!'}), 401                
                
            except Exception as err: 
                return jsonify({'message' : f'{err}'}), 401
        
            return  f(usuario.usuario_id, *args, **kwargs)    
         
        return decorated

    def login(email, senha): 
        success: bool = False
        msg: str = 'E-mail ou Senha não é válido'
        authorization = None
        try:
            
            # Verifica o IP do usuário que iniciou a sessão
            ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            print(ip)
                       
            # Verifica se as informações foram passadas corretamente para executar o login
            if not email or not senha:                 
                #return make_response('Não foi possível verificar', 401, {'WWW-Authenticate' : 'Basic realm =E-mail ou Senha não é válido'})
                return success, msg
            # Valida o e-mail informado    
            if not Usuario.email_eh_valido(email):        
                return success, msg, authorization
            
            usuario = Usuario.get_usuario_by_email(email)             
            if not usuario:
                return success, msg, authorization
            
            # Valida a senha do Usuário
            if not check_password_hash(usuario.senha, senha): 
                return success, msg, authorization
            
            # Gera o Token de Autenticação
            token, session_key = Token.add_token(usuario.usuario_id, usuario.chave_publica)
            
            # Recupera as permissões do usuário
            permissoes = []           
            results = Usuario.get_permissoes_usuario(usuario.usuario_id)            
            for r in results: 
                permissoes.append(r[0])
            
            authorization = {
                "token": token,
                "nome" : usuario.primeiro_nome + ' ' + usuario.sobrenome,
                "permissoes": permissoes,
                "session_key": session_key             
            }
            success = True
            msg = 'Login realizado com sucesso!'
            return success, msg, authorization 

        except Exception:
            msg = 'Erro desconhecido'
            return success, msg, authorization 