from config import parameters
from sqlalchemy import  Column
from functools import wraps 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)
from sqlalchemy import create_engine, select, and_ , or_, update
from sqlalchemy.orm import Session

from seguranca.business_exception import BusinessException
from seguranca.permissoes import Permissao
from seguranca.grupo import Grupo

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Grupo_Permissao (Base):
    __tablename__ = "GRUPO_PERMISSOES"

    grupopermissao_id = Column(INTEGER, primary_key=True)
    grupo_id = Column(INTEGER)
    permissao_id = Column(INTEGER)

    def __repr__(self) -> str:
        return f"Grupo_Permissao(grupopermissao_id={self.grupopermissao_id!r},grupo_id={self.grupo_id!r},permissao_id={self.permissao_id!r})" 
    
    def __init__(self, grupo_id, permissao_id):
        self.grupo_id = grupo_id
        self.permissao_id = permissao_id
    
    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):  
        return { 
            'grupopermissao_id':self.grupopermissao_id,           
            'grupo_id': self.grupo_id,
            'permissao_id': self.permissao_id
        }  

    # Recupera as permissões associadas ao grupo
    def get_permissoes_do_grupo(usuario_id, grupo_id, permissao_pai: str=None):

        # Verifica se o usuário pode ver o conteúdo da tabela Grupo_Permissao
        acesso_liberado = False       
        if permissao_pai:
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, permissao_pai)
        else:
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Permissoes_de_Grupos')        
        if not acesso_liberado:                
            raise BusinessException('Usuário não possui permissão para visualização da lista de permissões associadas ao grupo informado')
        
        # Verifica se o grupo existe
        grupo = Grupo.get_grupo_id(usuario_id, grupo_id, 'Pode_Visualizar_Permissoes_de_Grupos')
        if not grupo:                
            raise BusinessException('Grupo não encontrado')        
        
        # Recupera as permissões do grupo
        result = session.query(Grupo_Permissao).where(Grupo_Permissao.grupo_id == grupo_id).all()   
        if not result:                
            raise BusinessException('Grupo não possui permissões')           

        """
        result = session.query(Grupo_Permissao, Permissao)\
                    .filter(Grupo_Permissao.grupo_id == grupo_id)\
                    .join(Permissao, Permissao.permissao_id==Grupo_Permissao.permissao_id)\
                    .all()
        """        
        return result
