from sqlalchemy import Column
from sqlalchemy import create_engine, select, and_
from sqlalchemy.dialects.sqlite import (INTEGER, VARCHAR, FLOAT)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from config import parameters
from estado import Estado
from pais import Pais
from seguranca.business_exception import BusinessException
from seguranca.pemissoes import Permissao

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)


class Cidade(Base):
    # Identifica a tabela no Banco de Dados
    __tablename__ = "CIDADE"

    # Propriedades da Classe
    cidade_id = Column(INTEGER, primary_key=True)
    pais_id = Column(INTEGER)
    estado_id = Column(INTEGER)
    nome = Column(VARCHAR(250))
    distancia_km = Column(FLOAT)
    valor_pedagio = Column(FLOAT)

    # Método de Representação
    def __repr__(self) -> str:
        return f"Cidade(cidade_id={self.cidade_id!r}, pais_id={self.pais_id!r}, estado_id={self.estado_id!r}, nome={self.nome!r}, distancia_km={self.distancia_km!r}, valor_pedagio={self.valor_pedagio!r})"

    # Método de Inicialização - Construtor
    def __init__(self, pais_id, estado_id, nome, distancia_km, valor_pedagio):
        self.pais_id = pais_id
        self.estado_id = estado_id
        self.nome = nome
        self.distancia_km = distancia_km
        self.valor_pedagio = valor_pedagio

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):
        return {
            "cidade_id": int(self.cidade_id),
            "pais_id": int(self.pais_id),
            "estado_id": int(self.estado_id),
            "nome": self.nome,
            "distancia_km": self.distancia_km,
            "valor_pedagio": self.valor_pedagio
        }

    # Retorna os estados cadastrados
    def get_cidades(usuario_id):
        try:            
            # Verifica se o usuário pode ver o conteúdo da tabela países
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Cidades')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização dos cidades')
            
            listCidades = []
            cidades = (
                    session.query(Cidade, Estado, Pais)
                    .join(Estado, Cidade.estado_id == Estado.estado_id)
                    .join(Pais, Estado.pais_id == Pais.pais_id)
                    .order_by(Cidade.nome).all()
            )
            
            for cidade in cidades:
                c =  {
                    "cidade_id": int(cidade.Cidade.cidade_id),
                    "estado_id": int(cidade.Estado.estado_id),
                    "estado_nome": str(cidade.Estado.nome),
                    "pais_id": int(cidade.Pais.pais_id),
                    "pais_nome": str(cidade.Pais.nome),
                    "nome": cidade.Cidade.nome,
                    "distancia_km": float(cidade.Cidade.distancia_km),
                    "valor_pedagio": float(cidade.Cidade.valor_pedagio),
                }   
                listCidades.append(c)              
            return listCidades
        
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')

    # Retorna a Cidade informada
    def get_cidade_id(usuario_id, cidade_id, permissao_pai: str = None):
        """
        Este método utiliza um conceito de permissão pai, quando invocado por uma outra classe.
        Facilita para não ter que dar outras permissões para o usuário
        Utiliza a permissão do método que a chamou
        """
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela estado
            acesso_liberado = False
            if permissao_pai:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, permissao_pai)
            else:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Cidades')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização da cidade informada')

            # Retorna o grupo selecionado
            sql = select(Cidade).where(Cidade.cidade_id == cidade_id)
            cidade = session.scalars(sql).one()                         
            if not cidade:
                raise BusinessException('Cidade não encontrada')

            return cidade

        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')

    def add_cidade(usuario_id, acidade):
        try:
            # Verifica se o usuário pode adicionar uma nova cidade ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Criar_Cidades')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para adicionar novas cidades')

            # Verifica se os campos estão preenchidos
            if acidade['pais_id'] == '' or not acidade['pais_id']:
                raise BusinessException('O país é obrigatório')

            if acidade['estado_id'] == '' or not acidade['estado_id']:
                raise BusinessException('O estado é obrigatório')

            if acidade['nome'] == '' or not acidade['nome']:
                raise BusinessException('Nome da cidade é obrigatória')

            if float(acidade['distancia_km']) < 0 : #or acidade['distancia_km'] == ""
                raise BusinessException('A distância em km da cidade é obrigatória')

            if float(acidade['valor_pedagio']) < 0 : #or not float(acidade['valor_pedagio'])
                raise BusinessException('O valor do pedágio é obrigatório')

            # Verifica se o estado informado existe no sistema
            estado = Estado.get_estado_id(usuario_id, acidade['estado_id'], 'Pode_Criar_Cidade')
            if not estado:
                raise BusinessException('Estado informado não está cadastrado')

            # Verifica se já existe uma cidade cadastrada no banco de dados
            rows = session.query(Cidade).where(
                and_(
                    Cidade.estado_id == acidade['estado_id'],
                    Cidade.nome == acidade['nome']
                )).count()
            if rows > 0:
                raise BusinessException('Cidade já cadastrada com este nome')

            rows = session.query(Cidade).where(
                and_(
                    Cidade.estado_id == acidade['estado_id'],
                    Cidade.nome == acidade['nome']
                )).count()
            if rows > 0:
                raise BusinessException('Cidade já cadastrada com este nome')

            novaCidade = Cidade(
                pais_id = acidade['pais_id'],
                estado_id = acidade['estado_id'],
                nome = acidade['nome'].upper().strip(),
                distancia_km = float(acidade['distancia_km'].strip()),
                valor_pedagio = float(acidade['valor_pedagio'].strip())
            )

            # Adiciona uma nova Cidade
            session.add(novaCidade)
            session.commit()
            return novaCidade

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')

            # Atualiza uma Cidade Existente

    def update_cidade(usuario_id, cidade_id, ucidade):
        try:
            # Verifica se o usuário pode adicionar um novo estado ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Atualizar_Cidades')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para editar os dados da cidade')
           
            # Verifica os códigos informados
            if int(ucidade['cidade_id']) != cidade_id:
                raise BusinessException('Erro na identificação da cidade')                  

            # Verifica se os campos estão preenchidos
            if ucidade['cidade_id'] == '' or not ucidade['cidade_id']:
                raise BusinessException('A cidade é obrigatória')
            
            # Verifica se os campos estão preenchidos
            if ucidade['pais_id'] == '' or not ucidade['pais_id']:
                raise BusinessException('O país é obrigatório')            

            if ucidade['estado_id'] == '' or not ucidade['estado_id']:
                raise BusinessException('O estado é obrigatório')

            if ucidade['nome'] == '' or not ucidade['nome']:
                raise BusinessException('Nome da Cidade é obrigatório')

            if ucidade['distancia_km'] == '' or not ucidade['distancia_km']:
                raise BusinessException('A distância em km é obrigatória')

            if ucidade['valor_pedagio'] == '' or not ucidade['valor_pedagio']:
                raise BusinessException('O valor do pedágio é obrigatório')

            # Recupera os dados da cidade informada
            sql = select(Cidade).where(Cidade.cidade_id == ucidade['cidade_id'])
            cidade = session.scalars(sql).one()
            if not cidade:
                raise BusinessException('Cidade informada não encontrada')

            # Verifica se o nome do Cidade foi alterada.
            # Se sim, precisa checar se já existe um cadastrado no sistema
            if cidade.nome != ucidade['nome']:
                rows = session.query(Cidade).where(
                    and_(
                        Cidade.pais_id == ucidade['pais_id'],
                        Cidade.estado_id == ucidade['estado_id'],
                        Cidade.nome == ucidade['nome'],
                        Cidade.cidade_id != ucidade['cidade_id']
                    )).count()
                if rows > 0:
                    raise BusinessException('Nome informado já cadastrado para outra cidade')

            # Atualiza o objeto a ser alterado
            cidade.nome = ucidade['nome'].upper().strip()
            cidade.estado_id = ucidade['estado_id']
            cidade.pais_id = ucidade['pais_id']
            cidade.distancia_km = ucidade['distancia_km'].strip()
            cidade.valor_pedagio = ucidade['valor_pedagio'].strip()

            # Comita as alterações no banco de dados
            session.commit()
            return cidade

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')