from config import parameters
from sqlalchemy import  Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)
from sqlalchemy import create_engine, func
from sqlalchemy import select, and_ , or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Usuario_Permissao (Base):
   
    # Identifica a tabela no Banco de Dados
    __tablename__ = "USUARIO_PERMISSAO"
 
    # Propriedades da Classe
    usuariopermissao_id = Column(INTEGER, primary_key=True)
    usuario_id = Column(INTEGER)
    permissao_id = Column(INTEGER)

    # Método de Representação
    def __repr__(self) -> str:
        return f"Usuario_Permissao(usuariopermissao_id={self.usuariopermissao_id!r}, usuario_id={self.usuario_id!r}, permissao_id={self.permissao_id!r})"
    
    # Método de Inicialização
    def __init__(self, usuario_id, permissao_id):
        self.usuario_id = usuario_id 
        self.permissao_id = permissao_id

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):  
        return {
            "usuariopermissao_id": str(self.usuariopermissao_id),
            "usuario_id": self.usuario_id,
            "permissao_id": self.permissao_id
        }         

    # Retorna se o usuário possui a permissão requerida
    def usuario_possui_permissao(usuario, permissao_id):   

        rows = session.query(Usuario_Permissao).where(
                and_(
                    Usuario_Permissao.usuario_id == usuario,
                    Usuario_Permissao.permissao_id == permissao_id)
                ).count()   
        if rows == 0:
            return False
        else: 
            return True