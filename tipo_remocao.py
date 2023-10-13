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

class Tipo_Remocao(Base):
    # Identifica a tabela no Banco de Dados
    __tablename__ = "TIPO_REMOCAO"

    # Propriedades da Classe
    tipo_remocao_id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(50))

    # Método de Representação
    def __repr__(self) -> str:
        return f"Tipo_Remocao(tipo_remocao_id={self.tipo_remocao_id!r}, nome={self.nome!r})"

    # Método de Inicialização
    def __init__(self, nome):
        self.nome = nome

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):
        return {
            "tipo_remocao_id": int(self.tipo_remocao_id),
            "nome": self.nome
        }

    # Retorna os tipos de remoção cadastrados
    def get_tipo_remocao(usuario_id):
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela tipo de remoção
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Tipo_Remocao')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização dos tipos de remoção')
            tipo_remocao = session.query(Tipo_Remocao).all()
            return tipo_remocao
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')
        
    # Retorna o tipo de remoção informado
    def get_tipo_remocao_id(usuario_id, tipo_remocao_id, permissao_pai: str = None):
        """
        Este método utiliza um conceito de permissão pai, quando invocado por uma outra classe.
        Facilita para não ter que dar outras permissões para o usuário
        Utiliza a permissão do método que a chamou
        """
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela tipo remoção
            acesso_liberado = False
            if permissao_pai:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, permissao_pai)
            else:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Tipo_Remocao')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização do tipo de remoção informado')
            # Retorna a cidade selecionada
            sql = select(Tipo_Remocao).where(Tipo_Remocao.tipo_remocao_id == tipo_remocao_id)
            tipo_remocao = session.scalars(sql).one()                                   
            if not tipo_remocao:
                raise BusinessException('Tipo de Remoção não encontrado')

            return tipo_remocao

        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')

    def add_tipo_remocao(usuario_id, atiporemocao):
        try:
            # Verifica se o usuário pode adicionar um novo veículo ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Criar_Tipo_Remocao')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para adicionar novos tipos de remoção')

            # Verifica se os campos estão preenchidos
            if atiporemocao['nome'] == '' or not atiporemocao['nome']:
                raise BusinessException('O nome é obrigatório')

            # Verifica se existe um tipo de remoção já cadastrado no banco de dados
            rows = session.query(Tipo_Remocao).where(Tipo_Remocao.nome == atiporemocao['nome']).count()
            if rows > 0:
                raise BusinessException('Tipo de remoção já cadastrado com este nome')

            novoTipo_Remocao = Tipo_Remocao(
                nome = atiporemocao['nome']
            )

            # Adiciona um novo Veículo
            session.add(novoTipo_Remocao)
            session.commit()
            return novoTipo_Remocao

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')

    # Atualiza um Veículo Tipo de Remoção
    def update_tipo_remocao(usuario_id, tipo_remocao_id, utiporemocao):
        try:
            # Verifica se o usuário pode adicionar um novo tipo de remocao ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Atualizar_Tipo_Remocao')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para editar os dados do tipo de remoção')

            # Verifica os códigos informados
            if int(utiporemocao['tipo_remocao_id']) != tipo_remocao_id:
                raise BusinessException('Erro na identificação do tipo da remoção')

            # Verifica se os campos estão preenchidos
            if utiporemocao['nome'] == '' or not utiporemocao['nome']:
                raise BusinessException('O nome é obrigatório')

            # Recupera os dados do tipo de remoção informado
            sql = select(Tipo_Remocao).where(Tipo_Remocao.tipo_remocao_id == utiporemocao['tipo_remocao_id'])
            tipo_remocao = session.scalars(sql).one()
            if not tipo_remocao:
                raise BusinessException('Tipo de remoção informado não encontrado')

            # Verifica se o nome do tipo de remoção foi alterado.
            # Se sim, precisa checar se já existe um cadastrado no sistema
            if tipo_remocao.nome != utiporemocao['nome']:
                rows = session.query(Tipo_Remocao).where(Tipo_Remocao.nome == utiporemocao['nome']).count()
                if rows > 0:
                    raise BusinessException('Tipo de remoção informado já cadastrado')

            # Atualiza o objeto a ser alterado
            tipo_remocao.nome = utiporemocao['nome']

            # Comita as alterações no banco de dados
            session.commit()
            return tipo_remocao

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')