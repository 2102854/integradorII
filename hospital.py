from sqlalchemy import Column
from sqlalchemy import create_engine, func, select, and_
from sqlalchemy.dialects.sqlite import (INTEGER, VARCHAR)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op


from config import parameters
from seguranca.business_exception import BusinessException
from seguranca.pemissoes import Permissao

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)


class Hospital(Base):
    # Identifica a tabela no Banco de Dados
    __tablename__ = "HOSPITAL"

    # Propriedades da Classe
    hospital_id = Column(INTEGER, primary_key=True)
    endereco_id = Column(INTEGER)
    nome = Column(VARCHAR(250))

    # Método de Representação
    def __repr__(self) -> str:
        return f"Hospital(hospital_id={self.hospital_id!r},endereco_id={self.endereco_id!r}, nome={self.nome!r})"

    # Método de Inicialização
    def __init__(self, endereco_id, nome):
        self.endereco_id = endereco_id
        self.nome = nome

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):
        return {
            "hospital_id": int(self.hospital_id),
            "endereco_id": int(self.endereco_id),
            "nome": self.nome
        }

    # Retorna o total de pacientes cadastrados no sistema
    def get_total_hospitais(usuario_id):
        # Verifica se o usuário pode ver o conteúdo da tabela hospital
        acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Hospitais')
        if not acesso_liberado:
            return 0
        else:
            total = session.query(func.count(Hospital.hospital_id)).scalar()
            return total

    # Retorna os hospitais cadastrados
    def get_hospitais(usuario_id):
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela de hospitais
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Hospitais')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização dos hospitais')
            hospital = session.query(Hospital).all()
            return hospital
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')

    # Retorna o Hospital informado
    def get_hospital_id(usuario_id, hospital_id, permissao_pai: str = None):
        """
        Este método utiliza um conceito de permissão pai, quando invocado por uma outra classe.
        Facilita para não ter que dar outras permissões para o usuário
        Utiliza a permissão do método que a chamou
        """
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela hospital
            acesso_liberado = False
            if permissao_pai:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, permissao_pai)
            else:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Hospitais')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização do hospital informado')

            # Retorna o grupo selecionado
            hospital = session.query(Hospital).where(Hospital.hospital_id == hospital_id).all()
            if not hospital:
                raise BusinessException('Hospital não encontrado')

            return hospital

        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')

    def add_hospital(usuario_id, ahospital):
        try:
            # Verifica se o usuário pode adicionar um novo hospital ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Criar_Hospitais')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para adicionar novos hospitais')

            # Verifica se os campos estão preenchidos
            if ahospital['endereco_id'] == '' or not ahospital['endereco_id']:
                raise BusinessException('O endereco é obrigatório')

            if ahospital['nome'] == '' or not ahospital['nome']:
                raise BusinessException('Nome do hospital é obrigatório')

            # Verifica se já existe um hospital já cadastrado no banco de dados
            rows = session.query(Hospital).where(
                and_(
                    Hospital.endereco_id == ahospital['endereco_id'],
                    Hospital.nome == ahospital['nome']
                )).count()
            if rows > 0:
                raise BusinessException('Hospital já cadastrado com este nome')

            novoHospital = Hospital(
                endereco_id=ahospital['endereco_id'],
                nome=ahospital['nome']
            )

            # Adiciona um novo Estado
            session.add(novoHospital)
            session.commit()
            return novoHospital

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')

            # Atualiza um Hospital Existente

    def update_hospital(usuario_id, uhospital):
        try:
            # Verifica se o usuário pode adicionar um novo pais ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Atualizar_Hospitais')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para editar os dados do hospital')

            # Verifica se os campos estão preenchidos
            if uhospital['endereco_id'] == '' or not uhospital['endereco_id']:
                raise BusinessException('O endereço é obrigatório')

            if uhospital['nome'] == '' or not uhospital['nome']:
                raise BusinessException('Nome do hospital é obrigatório')

                # Recupera os dados do hospital informado
            sql = select(Hospital).where(Hospital.hospital_id == uhospital['hospital_id'])
            hospital = session.scalars(sql).one()
            if not hospital:
                raise BusinessException('Hospital informado não encontrado')

                # Verifica se o nome do Hospital foi alterado.
            # Se sim, precisa checar se já existe um cadastrado no sistema
            if hospital.nome != uhospital['nome']:
                rows = session.query(Hospital).where(
                    and_(
                        Hospital.endereco_id == uhospital['endereco_id'],
                        Hospital.nome == uhospital['nome']
                    )).count()
                if rows > 0:
                    raise BusinessException('Nome informado já cadastrado para outro hospital')

            # Atualiza o objeto a ser alterado
            hospital.nome = uhospital['nome'].upper().strip()
            hospital.endereco_id = uhospital['endereco_id']

            # Comita as alterações no banco de dados
            session.commit()
            return hospital

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')