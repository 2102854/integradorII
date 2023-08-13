from config import parameters
from flask import Flask, request, jsonify, make_response 
import jwt 
from datetime import datetime, timedelta 
from functools import wraps 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)
from sqlalchemy import create_engine, func
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op
from werkzeug.security import check_password_hash

from usuario import Usuario
from seguranca.business_exception import BusinessException

Base = declarative_base()

class Auth(Base): 
    def token_required(f): 
        @wraps(f) 
        def decorated(*args, **kwargs): 
            token = None
            if 'x-access-token' in request.headers: 
                token = request.headers['x-access-token'] 
            if not token: 
                return jsonify({'message' : 'Token is missing !!'}), 401
            try: 
                data = jwt.decode(token, parameters['SECRET_KEY']) 
                #current_user = User.query.filter_by(public_id = data['public_id']).first() 
                current_user = ''
            except: 
                return jsonify({'message' : 'Token is invalid !!'}), 401
        
            return  f(current_user, *args, **kwargs)     
        return decorated

    def login(email, senha): 
           
        # Verifica se as informações foram passadas corretamente para executar o login
        if not email or not senha: 
            raise BusinessException('E-mail ou Senha não é válido.')
            """
            return make_response( 
                'Could not verify', 
                401, 
                {'WWW-Authenticate' : 'Basic realm ="Login required !!"'} 
            ) 
            """        
        # Valida o e-mail informado
        if not Usuario.email_eh_valido(email):
            raise BusinessException('E-mail não é Válido')
    
        usuario = Usuario.get_usuario_by_email(email) 
        if not usuario:
            raise BusinessException('E-mail ou Senha não é válido.') 
            """
            return make_response( 
                'Could not verify', 
                401, 
                {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'} 
            ) 
            """
        # Valida a senha do Usuário
        if not check_password_hash(usuario.senha, senha): 
            raise BusinessException('E-mail ou Senha não é válido.')
        
        """
        token = jwt.encode({ 
                'public_id': user.public_id, 
                'exp' : datetime.utcnow() + timedelta(minutes = 30) 
            }, app.config['SECRET_KEY']) 
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201) 
        
        return make_response( 
            'Could not verify', 
            403, 
            {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'} 
        ) 
        """    