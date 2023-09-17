"""
Módulo Tipo Encaminhamento
"""
from sqlalchemy import Column
from sqlalchemy import create_engine, select, and_
from sqlalchemy.dialects.sqlite import (INTEGER, VARCHAR, FLOAT)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from config import parameters
from seguranca.business_exception import BusinessException
from seguranca.pemissoes import Permissao

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)


class Tipo_Encaminhamento(Base):
    # Identifica a tabela no Banco de Dados
    __tablename__ = "TIPO_ENCAMINHAMENTO"

    # Propriedades da Classe
    tipo_encaminhamento_id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(50))

    # Método de Representação
    def __repr__(self) -> str:
        return f"Tipo_Encaminhamento(tipo_encaminhamento_id={self.tipo_encaminhamento_id!r}, nome={self.nome!r})"

    # Método de Inicialização
    def __init__(self, nome):
        self.nome = nome

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):
        return {
            "tipo_encaminhamento_id": int(self.tipo_encaminhamento_id),
            "nome": self.nome
        }

    # Retorna os tipos de encaminhamento cadastrados
    def get_tipo_encaminhamento(usuario_id):
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela tipo de encaminhamento
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Tipo_Encaminhamento')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização dos tipos de encaminhamento')
            tipo_encaminhamento = session.query(Tipo_Encaminhamento).all()
            return tipo_encaminhamento
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')

    # Retorna o tipo de encaminhamento informado
    def get_tipo_encaminhamento_id(usuario_id, tipo_encaminhamento_id, permissao_pai: str = None):
        """
        Este método utiliza um conceito de permissão pai, quando invocado por uma outra classe.
        Facilita para não ter que dar outras permissões para o usuário
        Utiliza a permissão do método que a chamou
        """
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela tipo encaminhamento
            acesso_liberado = False
            if permissao_pai:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, permissao_pai)
            else:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Tipo_Encaminhamento')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização do tipo de encaminhamento informado')

            # Retorna o grupo selecionado
            tipo_encaminhamento = session.query(Tipo_Encaminhamento).where(Tipo_Encaminhamento.tipo_encaminhamento_id == tipo_encaminhamento_id).all()
            if not tipo_encaminhamento:
                raise BusinessException('Tipo de Encaminhamento não encontrado')

            return tipo_encaminhamento

        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')

    def add_tipo_encaminhamento(usuario_id, atipoencaminhamento):
        try:
            # Verifica se o usuário pode adicionar um novo encaminhamento ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Criar_Tipo_Encaminhamento')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para adicionar novos tipos de encaminhamento')

            # Verifica se os campos estão preenchidos
            if atipoencaminhamento['nome'] == '' or not atipoencaminhamento['nome']:
                raise BusinessException('O nome é obrigatório')


            # Verifica se existe um tipo de encaminhamento já cadastrado no banco de dados
            rows = session.query(Tipo_Encaminhamento).where(
                and_(
                    Tipo_Encaminhamento.nome == atipoencaminhamento['nome']
                )).count()
            if rows > 0:
                raise BusinessException('Tipo de encaminhamento já cadastrado com este nome')

            novoTipo_Encaminhamento = Tipo_Encaminhamento(
                nome = atipoencaminhamento['nome']
            )

            # Adiciona um novo Veículo
            session.add(novoTipo_Encaminhamento)
            session.commit()
            return novoTipo_Encaminhamento

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')

            # Atualiza um Tipo de Encaminhamento

    def update_tipo_encaminhamento(usuario_id, utipoencaminhamento):
        try:
            # Verifica se o usuário pode adicionar um novo tipo de remocao ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Atualizar_Tipo_Encaminhamento')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para editar os dados do tipo de encaminhamento')

            # Verifica se os campos estão preenchidos
            if utipoencaminhamento['nome'] == '' or not utipoencaminhamento['nome']:
                raise BusinessException('O nome é obrigatório')

                # Recupera os dados do tipo de encaminhamento informado
            sql = select(Tipo_Encaminhamento).where(Tipo_Encaminhamento.tipo_encaminhamento_id == utipoencaminhamento['tipo_encaminhamento_id'])
            tipo_encaminhamento = session.scalars(sql).one()
            if not tipo_encaminhamento:
                raise BusinessException('Tipo de encaminhamento informado não encontrado')

                # Verifica se o nome do tipo de encaminhamento foi alterado.
            # Se sim, precisa checar se já existe um cadastrado no sistema
            if tipo_encaminhamento.nome != utipoencaminhamento['nome']:
                rows = session.query(Tipo_Encaminhamento).where(
                    and_(
                        Tipo_Encaminhamento.nome == utipoencaminhamento['nome']
                    )).count()
                if rows > 0:
                    raise BusinessException('Tipo de encaminhamento informado já cadastrado')

                    # Atualiza o objeto a ser alterado
            tipo_encaminhamento.nome = utipoencaminhamento['nome']

            # Comita as alterações no banco de dados
            session.commit()
            return tipo_encaminhamento

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')