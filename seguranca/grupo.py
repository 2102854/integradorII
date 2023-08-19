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
    nome = Column(VARCHAR(250), nullable=False)
    descricao = Column(VARCHAR(250), nullable=False)
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
    
    # Valida campos booleans passados em formulário
    def check_bool_field(b):
        if not b:
            return 0
        else:
            if b == False or b == 'False' or b== '0':
                return 0
            elif b == True or b == 'True' or b== '1':
                return 1

    # Retorna todos os grupos cadastrados
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

    # Retorna os grupos informado
    def get_grupo_id(usuario_id, grupo_id, permissao_pai: str=None):
        """
        Este método utiliza um conceito de permissão pai, quando invocado por uma outra classe.
        Facilita para não ter que dar outras permissões para o usuário
        Utiliza a permissão do método que a chamou
        """
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela grupos            
            acesso_liberado = False
            if permissao_pai:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, permissao_pai)
            else:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Grupos')
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para visualização dos grupos do sistema')
            
            # Retorna o grupo selecionado
            grupo = session.query(Grupo).where(Grupo.grupo_id == grupo_id).all()  
            if not grupo:                
                raise BusinessException('Grupo não encontrado')

            return grupo 
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')              
        
    def add_grupo(usuario_id, nome, descricao, admin, ativo):
        try:
            # Verifica se o usuário pode adicionar um novo grupo ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Adicionar_Grupo')
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para adicionar novos grupos')
            
            # Verifica se os campos estão preenchidos
            if nome == '' or  not nome:
                raise BusinessException('Nome do grupo é obrigatório')

            if descricao == '' or  not descricao:
                raise BusinessException('Descrição do grupo é obrigatório') 

            admin = Grupo.check_bool_field(admin)
            ativo = Grupo.check_bool_field(ativo)
                                 
            # Verifica se já existe um grupo cadastrado no banco de dados
            rows = session.query(Grupo).where(Grupo.nome == nome).count()   
            if rows > 0:
                raise BusinessException('Grupo já cadastrado no banco de dados')

            novoGrupo = Grupo(
                nome = nome,
                descricao = descricao,
                admin = int(admin),
                ativo = int(ativo)
            )

            # Adiciona um novo usuário
            session.add(novoGrupo)  
            session.commit()
            return novoGrupo
        
        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            print(e)
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')    

    # Atualiza um Grupo Existente - A Chamada se faz pelo objeto grupo
    def update_grupo(usuario_id, ugrupo):
        try:
            # Verifica se o usuário pode adicionar um novo grupo ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Editar_Grupo')
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para editar os dados de grupos')
            
            print(ugrupo)

            # Verifica se os campos estão preenchidos
            if ugrupo['nome'] == '' or  not ugrupo['nome']:
                raise BusinessException('Nome do grupo é obrigatório')

            if ugrupo['descricao'] == '' or  not ugrupo['descricao']:
                raise BusinessException('Descrição do grupo é obrigatório')

            ugrupo['admin'] = Grupo.check_bool_field(ugrupo['admin'])
            ugrupo['ativo'] = Grupo.check_bool_field(ugrupo['ativo'])                        
                                 
            # Recupera os dados do grupo informado
            sql = select(Grupo).where(Grupo.grupo_id == ugrupo['grupo_id'])
            grupo = session.scalars(sql).one()
            if not grupo:
                raise BusinessException('Grupo informado não encontrado')                
            
            # Verifica se o nome do grupo alterou, se sim, precisa checar se já existe um cadastrado no sistema
            if grupo.nome != ugrupo['nome']:
                rows = session.query(Grupo).where(
                    and_(
                        Grupo.nome == ugrupo['nome'],
                        Grupo.grupo_id != ugrupo['descricao']
                    )).count()
                if rows > 0:
                    raise BusinessException('Nome informado já cadastrado para outro grupo no banco de dados')

            # Atualiza o objeto a ser alterado
            grupo.nome = ugrupo['nome']
            grupo.descricao = ugrupo['descricao']
            grupo.admin = ugrupo['admin']
            grupo.ativo = ugrupo['ativo']

            # Comita as alterações no banco de dados            
            session.commit()
            return grupo
        
        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            print(e)
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')  