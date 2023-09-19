from config import parameters
from sqlalchemy import  Column
import jwt 
from datetime import datetime, timedelta 
import pytz
from functools import wraps 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)
from sqlalchemy import create_engine, select, and_ , or_, update
from sqlalchemy.orm import Session
from typing import Callable
from cuid2 import cuid_wrapper

Base = declarative_base()
cuid_generator: Callable[[], str] = cuid_wrapper()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Token (Base):
    __tablename__ = "TOKEN"

    token_id = Column(INTEGER, primary_key=True)
    data_criacao = Column(DATETIME, nullable=False)
    data_expiracao =  Column(DATETIME, nullable=False)
    token = Column(VARCHAR(250), nullable=False)
    usuario_id = Column(VARCHAR(128), nullable=False)
    chave_publica = Column(VARCHAR(100), nullable=False)
    expirado = Column(BOOLEAN, nullable=False, default=False)
    session_key = Column(VARCHAR(4000), nullable=False)

    def __repr__(self) -> str:
        return f"Token(token_id={self.token_id!r},data_criacao={self.data_criacao!r},data_expiracao={self.data_expiracao!r},token={self.token!r},\
            usuario_id={self.usuario_id!r},chave_publica={self.chave_publica!r},expirado={self.expirado!r})" 
    
    def __init__(self, data_criacao, data_expiracao, token, usuario_id, chave_publica, expirado, session_key):
        self.data_criacao = data_criacao
        self.data_expiracao = data_expiracao
        self.token = token
        self.usuario_id = usuario_id
        self.chave_publica = chave_publica
        self.expirado = expirado
        self.session_key = session_key
    
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
        # Caso o usuário possui outros tokens, marca todos com expirado.        
        rows = session.query(Token).where(Token.usuario_id == usuario_id).count()
        if rows > 0:                
            u = (update(Token).where(
                        and_(
                            Token.usuario_id == usuario_id,
                            Token.expirado == False
                        )).values(expirado = True))
            
            session.execute(u)
            session.commit()

        # New Token
        try:
            n_token = jwt.encode({ 
                    'chave_publica': chave_publica,
                    'exp' : datetime.utcnow() + timedelta(hours= 8)              
                }, parameters['SECRET_KEY'], algorithm="HS256") 
         except Exception as e:
            raise Exception(err)    
        
        dt_criacao = datetime.now(pytz.timezone(parameters['TIMEZONE']))
        dt_expiracao = datetime.now(pytz.timezone(parameters['TIMEZONE'])) + timedelta(minutes = parameters['LOGOUT_MINUTES'])        
        
        #https://pypi.org/project/cuid2/#description
        session_key: str = cuid_generator()
        
        token = Token(dt_criacao, dt_expiracao, n_token, usuario_id, chave_publica, False, session_key)
        
        session.add(token)        
        session.commit()  
        
        return n_token, session_key 
    
    # Formata data para comparação
    def formata_data(d):
        r = []
        s1 = str(d).split()
        d1 = s1[0].split('-')
        
        for x in d1:
            r.append(int(x))

        t1 = s1[1].split(':')
        ss = t1[2].split('.')
        r.append(int(t1[0]))
        r.append(int(t1[1]))
        r.append(int(ss[0]))
        dt = datetime(r[0], r[1], r[2], r[3], r[4], r[5])
        return dt 


    # Valida o Token informado
    def valida_token(n_token):
        try:    
            token = None
            # Recupera os dados do token do banco de dados
            try:
                sql = select(Token).where(Token.token == n_token)
                token = session.scalars(sql).one()
            except:
                raise Exception('Token Inválido!')
            
            # Se o token não existir
            if not token:
                raise Exception('Token Inválido!')
                        
            # Se o toke estiver expirado
            if token.expirado:
                raise Exception('Token Expirado!')
            
            # Se a data de expiração for menor que a data atual
            dt_now = Token.formata_data(datetime.now(pytz.timezone(parameters['TIMEZONE'])))
            dt_exp = Token.formata_data(token.data_expiracao)

            if dt_exp < dt_now:
                token.expirado = True
                session.commit()                
                raise Exception('Token Expirado!')

            # Atualiza a data de expiração do token
            token.data_expiracao = datetime.now(pytz.timezone(parameters['TIMEZONE'])) + timedelta(minutes = parameters['LOGOUT_MINUTES'])              
            session.commit()  
                                
        except Exception as err:
            raise Exception(err) 
    
    def logout(ltoken):
      
        sql = select(Token).where(Token.token == ltoken)
        token_logout = session.scalars(sql).one()
        
        if not token_logout:
            return
        
        token_logout.expirado = True
        token_logout.data_expiracao = Token.formata_data(datetime.now(pytz.timezone(parameters['TIMEZONE'])))
        session.commit()  
        
        return 
        