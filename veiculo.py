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


class Veiculo(Base):
    # Identifica a tabela no Banco de Dados
    __tablename__ = "VEICULO"

    # Propriedades da Classe
    veiculo_id = Column(INTEGER, primary_key=True)
    modelo = Column(VARCHAR(250))
    placa = Column(VARCHAR(20))
    capacidade = Column(INTEGER)
    media_consumo = Column(FLOAT)

    # Método de Representação
    def __repr__(self) -> str:
        return f"Veiculo(veiculo_id={self.veiculo_id!r}, modelo={self.modelo!r}, placa={self.placa!r}, " \
               f"capacidade={self.capacidade!r}, media_consumo={self.media_consumo!r})"

    # Método de Inicialização
    def __init__(self, modelo, placa, capacidade, media_consumo):
        self.modelo = modelo
        self.placa = placa
        self.capacidade = capacidade
        self.media_consumo = media_consumo

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):
        return {
            "veiculo_id": int(self.veiculo_id),
            "modelo": self.modelo,
            "placa": self.placa,
            "capacidade": self.capacidade,
            "media_consumo": self.media_consumo
        }

    # Retorna os veículos cadastrados
    def get_veiculos(usuario_id):
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela veiculos
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Veiculos')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização dos veículos')
            veiculos = session.query(Veiculo).all()
            return veiculos
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')

    # Retorna o Veículo informado
    def get_veiculo_id(usuario_id, veiculo_id, permissao_pai: str = None):
        """
        Este método utiliza um conceito de permissão pai, quando invocado por uma outra classe.
        Facilita para não ter que dar outras permissões para o usuário
        Utiliza a permissão do método que a chamou
        """
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela veículo
            acesso_liberado = False
            if permissao_pai:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, permissao_pai)
            else:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Veiculos')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização do veículo informado')

            # Retorna o grupo selecionado
            veiculo = session.query(Veiculo).where(Veiculo.veiculo_id == veiculo_id).all()
            if not veiculo:
                raise BusinessException('Veículo não encontrado')

            return veiculo

        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')

    #Adiciona um novo veículo
    def add_veiculo(usuario_id, aveiculo):
        try:
            # Verifica se o usuário pode adicionar um novo veículo ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Criar_Veiculos')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para adicionar novos veículos')

            # Verifica se os campos estão preenchidos
            if aveiculo['modelo'] == '' or not aveiculo['modelo']:
                raise BusinessException('O modelo é obrigatório')

            if aveiculo['placa'] == '' or not aveiculo['placa']:
                raise BusinessException('A placa é obrigatória')

            if aveiculo['capacidade'] == '' or not aveiculo['capacidade']:
                raise BusinessException('A capacidade do veículo é obrigatória')

            if float(aveiculo['media_consumo']) < 0 : #== '' or not aveiculo['media_consumo']
                raise BusinessException('A média de consumo do veículo é obrigatória')


            # Verifica se existe um veiculo já cadastrado no banco de dados
            rows = session.query(Veiculo).where(
                and_(
                    Veiculo.placa == aveiculo['placa']
                )).count()
            if rows > 0:
                raise BusinessException('Veículo já cadastrado com esta placa')

            novoVeiculo = Veiculo(
                modelo = aveiculo['modelo'],
                placa = aveiculo['placa'],
                capacidade = aveiculo['capacidade'],
                media_consumo = aveiculo['media_consumo']
            )

            # Adiciona um novo Veículo
            session.add(novoVeiculo)
            session.commit()
            return novoVeiculo

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')

    # Atualiza um Veículo Existente
    def update_veiculo(usuario_id, uveiculo):
        try:
            # Verifica se o usuário pode adicionar um novo veículo ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Atualizar_Veiculos')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para editar os dados do veículo')

            # Verifica se os campos estão preenchidos
            if uveiculo['modelo'] == '' or not uveiculo['modelo']:
                raise BusinessException('O modelo é obrigatório')

            if uveiculo['placa'] == '' or not uveiculo['placa']:
                raise BusinessException('A placa é obrigatória')

            if uveiculo['capacidade'] == '' or not uveiculo['capacidade']:
                raise BusinessException('A capacidade do veículo é obrigatória')

            if float(uveiculo['media_consumo']) < 0 : #== '' or not uveiculo['media_consumo']
                raise BusinessException('A media de consumo do veículo é obrigatória')

            # Recupera os dados do veículo informado
            sql = select(Veiculo).where(Veiculo.veiculo_id == uveiculo['veiculo_id'])
            veiculo = session.scalars(sql).one()
            if not veiculo:
                raise BusinessException('Veículo informado não encontrado')

            # Verifica se o nome do Veículo ou Sigla foi alterado.
            # Se sim, precisa checar se já existe um cadastrado no sistema
            if veiculo.placa != uveiculo['placa']:
                rows = session.query(Veiculo).where(
                    and_(
                        Veiculo.placa == uveiculo['[placa]']
                    )).count()
                if rows > 0:
                    raise BusinessException('Placa informada já cadastrada para outro veículo')

            # Atualiza o objeto a ser alterado
            veiculo.modelo = uveiculo['modelo']
            veiculo.placa = uveiculo['placa']
            veiculo.capacidade = uveiculo['capacidade']
            veiculo.media_consumo = uveiculo['media_consumo']

            # Comita as alterações no banco de dados
            session.commit()
            return veiculo

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')