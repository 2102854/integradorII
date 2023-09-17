"""
Módulo Tipo de Doenças
"""
from sqlalchemy import Column
from sqlalchemy import create_engine, select, and_
from sqlalchemy.dialects.sqlite import (INTEGER, VARCHAR)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from config import parameters
from seguranca.business_exception import BusinessException
from seguranca.pemissoes import Permissao

Base = declarative_base()

#Banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Tipo_Doenca (Base):

    #tabela db
    __tablename__ = "TIPO_DOENCA"

    tipo_doenca_id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Doenca(tipo_doenca_id={self.tipo_doenca_id!r},nome={self.nome!r})"

    def __init__(self, nome):
        self.nome = nome

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):  
        return {
            "tipo_doenca_id": str(self.tipo_doenca_id),
            "nome": self.nome
        }   

    #Retorna todos as doenças
    def get_tipoDoenca(usuario_id):
        try:
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Vizualizar_Tipo_de_Doenca')
            if not acesso_liberado:
                raise BusinessException('Usuário com permissão negada')
            doencas = session.query(Tipo_Doenca).all()
            return doencas
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')

    #Doença por pesquisa
    def get_tipoDoenca_id(usuario_id,  tipo_doenca_id, permissao_pai: str=None):
        """
        Este método utiliza um conceito de permissão pai, quando invocado por uma outra classe.
        Facilita para não ter que dar outras permissões para o usuário
        Utiliza a permissão do método que a chamou
        """        
        try:
            acesso_liberado = False
            if permissao_pai:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, permissao_pai)
            else:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Vizualizar_Tipo_de_Doenca')
                if not acesso_liberado:
                    raise BusinessException('Usuário não possui permissão para vizualizar os tipos de doença')

                #Retorno
                sql = select(Tipo_Doenca).where(Tipo_Doenca.tipo_doenca_id == tipo_doenca_id)
                doenca = session.scalars(sql).one()
                if not doenca:
                    raise BusinessException('Tipos de doenca não encontrados')
                return doenca
            
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')

    def add_tipoDoenca(usuario_id, atipoDoenca):
        try:
            # Verifica se o usuário pode adicionar um novo tipo de doença
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Criar_Tipo_Doenca')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para adicionar novas doenças')

            #Verifica se o nome foi preenchido
            if atipoDoenca['nome'] == '' or not atipoDoenca['nome']:
                raise BusinessException('Campo obrigatório')
            
            # Verifica se já existe este tipo de doença já está cadastrado no banco de dados
            rows = session.query(Tipo_Doenca).where(Tipo_Doenca.nome == atipoDoenca['nome']).count()
            if rows > 0:
                raise BusinessException('Tipo de Doença já registrado')

            novoTipoDoenca = Tipo_Doenca(
                nome = atipoDoenca['nome']
            )

            #Adiciona no banco de dados
            session.add(novoTipoDoenca)
            session.commit()
            
            return novoTipoDoenca

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')

    def update_tipoDoenca(usuario_id, tipo_doenca_id, utipoDoenca):
        try:
            # Verifica se o usuário pode alterar o tipo de doença 
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Editar_Tipo_Doenca')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para editar os dados dos tipos de doença')

            # Verifica os códigos informados
            if int(utipoDoenca['tipo_doenca_id']) != tipo_doenca_id:
                raise BusinessException('Erro na identificação do tipo de doença')    

            # Verifica se os campos estão preenchidos
            if utipoDoenca['nome'] == '' or not utipoDoenca['nome']:
                raise BusinessException('Nome do tipo de doença é obrigatório')

            # Recupera os dados do tipo de doença informado
            sql = select(Tipo_Doenca).where(Tipo_Doenca.tipo_doenca_id == utipoDoenca['tipo_doenca_id'])
            tipoDoenca = session.scalar(sql).one()
            if not tipoDoenca:
                raise BusinessException('Tipo de doença não encontrado')

            # Verifica se já existe um tipo de doença cadastrado no sistema
            if tipoDoenca.nome != utipoDoenca['nome']:
                rows = session.query(Tipo_Doenca).where(
                    and_(
                        Tipo_Doenca.nome == utipoDoenca['nome'],
                        Tipo_Doenca.tipo_doenca_id != utipoDoenca['tipo_doenca_id']
                    )
                ).count()
                if rows > 0:
                    raise BusinessException('Tipo informado já cadastrado para outra doença no banco de dados')

            # Atualiza o objeto a ser alterado
            tipoDoenca.nome = utipoDoenca['nome']

            # Comita as alterações no banco de dados
            session.commit()
            return tipoDoenca

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')
