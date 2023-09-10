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


class Motorista(Base):
    # Identifica a tabela no Banco de Dados
    __tablename__ = "MOTORISTA"

    # Propriedades da Classe
    motorista_id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(50))
    numero_habilitacao = Column(VARCHAR(250))
    carga_horaria = Column(FLOAT)

    # Método de Representação
    def __repr__(self) -> str:
        return f"Motorista(motorista_id={self.motorista_id!r}, nome={self.nome!r}, " \
               f"numero_habilitacao={self.numero_habilitacao!r}, carga_horaria={self.carga_horaria!r})"

    # Método de Inicialização
    def __init__(self, nome, numero_habilitacao, carga_horaria):
        self.nome = nome
        self.numero_habilitacao = numero_habilitacao
        self.carga_horaria = carga_horaria

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):
        return {
            "motorista_id": int(self.motorista_id),
            "nome": self.nome,
            "numero_habilitacao": self.numero_habilitacao,
            "carga_horaria": self.carga_horaria
        }

    # Retorna os motoristas cadastrados
    def get_motoristas(usuario_id):
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela motoristas
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Motoristas')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização dos motoristas')
            motoristas = session.query(Motorista).all()
            return motoristas
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')

    # Retorna o Motorista informado
    def get_motorista_id(usuario_id, motorista_id, permissao_pai: str = None):
        """
        Este método utiliza um conceito de permissão pai, quando invocado por uma outra classe.
        Facilita para não ter que dar outras permissões para o usuário
        Utiliza a permissão do método que a chamou
        """
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela motorista
            acesso_liberado = False
            if permissao_pai:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, permissao_pai)
            else:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Motoristas')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização do motorista informado')

            # Retorna o grupo selecionado
            motorista = session.query(Motorista).where(Motorista.motorista_id == motorista_id).all()
            if not motorista:
                raise BusinessException('Motorista não encontrado')

            return motorista

        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')

    def add_motorista(usuario_id, amotorista):
        try:
            # Verifica se o usuário pode adicionar um novo motorista ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Criar_Motoristas')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para adicionar novos motoristas')

            # Verifica se os campos estão preenchidos

            if amotorista['nome'] == '' or not amotorista['nome']:
                raise BusinessException('O nome é obrigatório')

            if amotorista['numero_habilitacao'] == '' or not amotorista['numero_habilitacao']:
                raise BusinessException('O número da habilitação do motorista é obrigatória')

            if float(amotorista['carga_horaria']) < 0 : #== '' or not amotorista['media_consumo']
                raise BusinessException('A carga horária do motorista é obrigatória')

            # Verifica se existe um motorista já cadastrado no banco de dados
            rows = session.query(Motorista).where(
                and_(
                    Motorista.numero_habilitacao == amotorista['numero_habilitacao']
                )).count()
            if rows > 0:
                raise BusinessException('Motorista já cadastrado com esta CNH')

            novoMotorista = Motorista(
                nome = amotorista['nome'].upper().strip(),
                numero_habilitacao = amotorista['numero_habilitacao'].strip(),
                carga_horaria = amotorista['carga_horaria'].strip()
            )

            # Adiciona um novo Motorista
            session.add(novoMotorista)
            session.commit()
            return novoMotorista

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')

            # Atualiza um Motorista Existente

    def update_motorista(usuario_id, umotorista):
        try:
            # Verifica se o usuário pode adicionar um novo motorista ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Atualizar_Motoristas')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para editar os dados do motorista')

            # Verifica se os campos estão preenchidos
            if umotorista['nome'] == '' or not umotorista['nome']:
                raise BusinessException('O nome é obrigatório')

            if umotorista['numero_habilitacao'] == '' or not umotorista['numero_habilitacao']:
                raise BusinessException('O número da habilitação é obrigatória')

            if float(umotorista['carga_horaria']) < 0 : #== '' or not umotorista['media_consumo']
                raise BusinessException('A carga horária do motorista é obrigatória')

            # Recupera os dados do motorista informado
            sql = select(Motorista).where(Motorista.motorista_id == umotorista['motorista_id'])
            motorista = session.scalars(sql).one()
            if not motorista:
                raise BusinessException('Motorista informado não encontrado')

            # Verifica se o nome do Motorista ou CNH foi alterado.
            # Se sim, precisa checar se já existe um cadastrado no sistema
            if motorista.nome != umotorista['nome']:
                rows = session.query(Motorista).where(
                    and_(
                        Motorista.numero_habilitacao == umotorista['numero_habilitacao'],
                        Motorista.nome == umotorista['nome']
                    )).count()
                if rows > 0:
                    raise BusinessException('Número de CNH informada já cadastrada para outro motorista')

            # Atualiza o objeto a ser alterado
            motorista.nome = umotorista['nome'].upper().strip()
            motorista.numero_habilitacao = umotorista['numero_habilitacao'].strip()
            motorista.carga_horaria = umotorista['carga_horaria'].strip()

            # Comita as alterações no banco de dados
            session.commit()
            return motorista

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')