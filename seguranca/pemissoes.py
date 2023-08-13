from config import parameters
from sqlalchemy import  Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)
from sqlalchemy import create_engine, func
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op

from seguranca.usuario_permissao import Usuario_Permissao

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Permissao ():

    # Verifica se o usuário possui a permissão informada
    def valida_permissao_usuario(usuario_id, permissao_id ):        
        result = Usuario_Permissao.usuario_possui_permissao(usuario_id, permissao_id)
        return result    
