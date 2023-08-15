from config import parameters
from sqlalchemy import  Column
from flask import Flask, request, jsonify, make_response 
import jwt 
from datetime import datetime, timedelta 
import pytz
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

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Token (Base):
    __tablename__ = "TOKEN"

    token_id = Column(INTEGER, primary_key=True)
    data_criacao = Column(DATETIME, nullable=False)
    data_expiracao =  Column(DATETIME, nullable=False)
    token = Column(TEXT(250), nullable=False)
    usuario_id = Column(TEXT(128), nullable=False)
    chave_publica = Column(TEXT(100), nullable=False)
    expirado = Column(BOOLEAN, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"Tipo_Responsavel(tipo_Responsavel_id={self.tipo_responsavel_id!r},nome={self.nome!r})" #Precisa corrigir
    
    def __init__(self, data_criacao, data_expiracao, token, usuario_id, chave_publica, expirado):
        self.data_criacao = data_criacao
        self.data_expiracao = data_expiracao
        self.token = token
        self.usuario_id = usuario_id
        self.chave_publica = chave_publica
        self.expirado = expirado
    
    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):  
        return {            
            'token_id': self.token_id,
            'data_criacao': self.data_criacao,
            'data_expiracao': self.data_expiracao,
            'token': self.token,
            'usuario_id': str(self.usuario_id),
            'expirado': self.expirado,
            'chave_publica' : self.chave_publica
        }   

     # Gera o Token de Autenticação
    def add_token(usuario_id, chave_publica):
        # New Token  #'exp' : datetime.utcnow() + timedelta(minutes = 30) 
        n_token = jwt.encode({ 
                'chave_publica': chave_publica               
            }, parameters['SECRET_KEY'])     
        
        dt_criacao = datetime.now(pytz.timezone(parameters['TIMEZONE']))
        dt_expiracao = datetime.now(pytz.timezone(parameters['TIMEZONE'])) + timedelta(minutes = parameters['LOGOUT_MINUTES'])        
        
        token = Token(dt_criacao, dt_expiracao, n_token, usuario_id, chave_publica, False)
        
        session.add(token)        
        session.commit()  
        
        return n_token 
     
    # Valida o Token informado
    def valida_token(n_token):
        try:    
            # Recupera os dados do token do banco de dados
            sql = select(Token).where(Token.token == n_token)
            token = session.scalars(sql).one()

            # Se o token não existir
            if not token:
                raise BusinessException('Token Inválido')
            
            # Se o toke estiver expirado
            if token.expirado:
                raise BusinessException('Token Expirado')
            
            # Se a data de expiração for menor que a data atual
            if token.data_expiracao < datetime.now(pytz.timezone(parameters['TIMEZONE'])):
                raise BusinessException('Token Expirado')

            # Atualiza a data de expiração do token
            token.data_expiracao = datetime.now(pytz.timezone(parameters['TIMEZONE'])) + timedelta(minutes = parameters['LOGOUT_MINUTES'])              
            session.commit()  
                                
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')         