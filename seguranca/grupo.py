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

from seguranca.business_exception import BusinessException
from seguranca.pemissoes import Permissao

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Grupo (Base):
    __tablename__ = "GRUPO"

    grupo_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250), nullable=False)
    descricao = Column(TEXT(250), nullable=False)
    admin = Column(BOOLEAN, nullable=False, default=False)
    ativo = Column(BOOLEAN, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"Grupo(grupo_id={self.grupo_id!r},nome={self.nome!r},descricao={self.descricao!r},admin={self.admin!r},ativo={self.ativo!r})" 
    
    def __init__(self, nome, descricao, admin=False, ativo=True):
        self.nome = nome
        self.descricao = descricao
        self.admin = admin
        self.ativo = ativo
    
    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):  
        return {            
            'grupo_id': self.grupo_id,
            'nome': self.nome,
            'descricao': self.descricao,
            'admin': self.admin,
            'ativo': self.ativo
        }  
    
    # Retorna os grupos cadastrados
    def get_grupos(usuario_id):
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela grupos
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Grupos')
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para visualização da lista de grupos do sistema')
            grupos = session.query(Grupo).all()  

            return grupos 
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')    