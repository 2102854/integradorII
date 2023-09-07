from config import parameters
from sqlalchemy import  Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)
from sqlalchemy import create_engine, select, and_ , or_, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op

from seguranca.pemissoes import Permissao
from seguranca.business_exception import BusinessException

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Pais (Base):
   
    # Identifica a tabela no Banco de Dados
    __tablename__ = "PAIS"
 
    # Propriedades da Classe
    pais_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250))
    sigla = Column(TEXT(3))
    
    # Método de Representação
    def __repr__(self) -> str:
        return f"Pais(pais_id={self.pais_id!r}, nome={self.nome!r}, sigla={self.sigla!r})"
    
    # Método de Inicialização
    def __init__(self, nome, sigla):
        self.nome = nome 
        self.sigla = sigla

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):  
        return {
            "pais_id": str(self.pais_id),
            "nome": self.nome,
            "sigla": self.sigla
        }         

    # Retorna os países cadastrados
    def get_paises(usuario_id):
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela países
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Paises')
            if not acesso_liberado:                
                raise BusinessException('Usuário não Possui permissão para visualização dos países')
            paises = session.query(Pais).all()   
            return paises 
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')

    # Retorna o pais informado
    def get_pais_id(usuario_id, pais_id, permissao_pai: str=None):
        """
        Este método utiliza um conceito de permissão pai, quando invocado por uma outra classe.
        Facilita para não ter que dar outras permissões para o usuário
        Utiliza a permissão do método que a chamou
        """
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela pais            
            acesso_liberado = False
            if permissao_pai:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, permissao_pai)
            else:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Paises')
            if not acesso_liberado:                
                raise BusinessException('Usuário não Possui permissão para visualização dos país informado')
            
            # Retorna o grupo selecionado
            pais = session.query(Pais).where(Pais.pais_id == pais_id).all()  
            if not pais:                
                raise BusinessException('Pais não encontrado')

            return pais 
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido') 
    
    def add_pais(usuario_id, apais):
        try:
            # Verifica se o usuário pode adicionar um novo grupo ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Criar_Paises')
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para adicionar novos paises')
            
            # Verifica se os campos estão preenchidos
            if apais['nome'] == '' or  not apais['nome']:
                raise BusinessException('Nome do pais é obrigatório')

            if apais['sigla'] == '' or  not apais['sigla']:
                raise BusinessException('Sigla do país é obrigatório')
                             
            # Verifica se já existe um país já cadastrado no banco de dados
            rows = session.query(Pais).where(Pais.nome == apais['nome']).count()   
            if rows > 0:
                raise BusinessException('Pais já cadastrado no banco de dados com este nome')
            
            rows = session.query(Pais).where(Pais.sigla == apais['sigla']).count()   
            if rows > 0:
                raise BusinessException('Pais já cadastrado no banco de dados com esta sigla')            

            novoPais = Pais(
                nome = apais['nome'].upper(),
                sigla = apais['sigla'].upper()
            )

            # Adiciona um novo país
            session.add(novoPais)  
            session.commit()
            return novoPais
        
        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')                  

    # Atualiza um Pais Existente
    def update_pais(usuario_id, upais):
        try:
            # Verifica se o usuário pode adicionar um novo pais ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Editar_Pais')
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para editar os dados do pais')
            
            # Verifica se os campos estão preenchidos
            if upais['nome'] == '' or  not upais['nome']:
                raise BusinessException('Nome do pais é obrigatório')

            if upais['sigla'] == '' or  not upais['sigla']:
                raise BusinessException('Sigla do país é obrigatório')                     
                                 
            # Recupera os dados do pais informado
            sql = select(Pais).where(Pais.pais_id == upais['pais_id'])
            pais = session.scalars(sql).one()
            if not pais:
                raise BusinessException('Pais informado não encontrado')                
            
            # Verifica se o nome do Pais ou Sigla foi alterado.
            # Se sim, precisa checar se já existe um cadastrado no sistema
            if pais.nome != upais['nome']:
                rows = session.query(Pais).where(
                    and_(
                        Pais.nome == upais['nome'],
                        Pais.pais_id != upais['pais_id']
                    )).count()
                if rows > 0:
                    raise BusinessException('Nome informado já cadastrado para outro pais no banco de dados')

            if pais.sigla != upais['sigla']:
                rows = session.query(Pais).where(
                    and_(
                        Pais.nome == upais['sigla'],
                        Pais.pais_id != upais['pais_id']
                    )).count()
                if rows > 0:
                    raise BusinessException('Sigla informada já cadastrada para outro pais no banco de dados')                

            # Atualiza o objeto a ser alterado
            pais.nome = upais['nome']
            pais.sigla = upais['sigla']

            # Comita as alterações no banco de dados            
            session.commit()
            return pais
        
        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')          