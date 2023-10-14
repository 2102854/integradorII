"""
Módulo Permissoes
"""
from config import parameters
from sqlalchemy import  Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)
from sqlalchemy import create_engine, func
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op

from seguranca.usuario_permissao import Usuario_Permissao
from seguranca.business_exception import BusinessException


Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Permissao (Base):
    __tablename__ = "PERMISSAO"

    permissao_id = Column(INTEGER, primary_key=True)
    permissao = Column(VARCHAR(250), nullable=False)
    nome =  Column(VARCHAR(250), nullable=False)
    descricao = Column(VARCHAR(250), nullable=False)
    modulo = Column(VARCHAR(100), nullable=False)
    icon = Column(VARCHAR(50), nullable=False)

    def __repr__(self) -> str:
        return f"Usuario(permissao_id={self.permissao_id!r},permissao={self.permissao!r},nome={self.nome!r},\
            senha={self.descricao!r},modulo={self.modulo!r})"
    
    def __init__(self, permissao, nome, descricao, modulo, icon):
        self.permissao = permissao
        self.nome = nome
        self.descricao = descricao
        self.senha = modulo
        self.icon = icon
    
    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):  
        return {
            'permissao_id': str(self.permissao_id),
            'permissao': self.permissao,
            'nome': self.nome,
            'descricao': self.descricao,
            'modulo': self.modulo,
            'icon': self.icon
        }   

    # Verifica se o usuário possui a permissão informada
    def valida_permissao_usuario(usuario_id, permissao ):  

        # Retorna o id a permissão informadada 
        sql = select(Permissao).where(Permissao.permissao == permissao)
        p = session.scalars(sql).one()

        result = Usuario_Permissao.usuario_possui_permissao(usuario_id, p.permissao_id)
        return result    

    # Retorna todas as permissoes de usuários do sistema
    def get_permissoes(usuario_id):
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela usuário
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Atualizar_Usuarios')
            
            if not acesso_liberado:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Editar_Grupo')
            
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para visualização da lista de permissões')
            permissoes = session.query(Permissao).order_by(Permissao.modulo, Permissao.nome).all()  

            return permissoes 
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')    