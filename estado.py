from config import parameters
from sqlalchemy import  Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)
from sqlalchemy import create_engine, select, and_ , or_, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op

from pais import Pais
from seguranca.pemissoes import Permissao
from seguranca.business_exception import BusinessException

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Estado (Base):
   
    # Identifica a tabela no Banco de Dados
    __tablename__ = "ESTADO"
 
    # Propriedades da Classe
    estado_id = Column(INTEGER, primary_key=True)
    pais_id = Column(INTEGER)
    nome = Column(VARCHAR(250))
    sigla = Column(VARCHAR(3))
    
    # Método de Representação
    def __repr__(self) -> str:
        return f"Estado(estado_id={self.estado_id!r},pais_id={self.pais_id!r}, nome={self.nome!r}, sigla={self.sigla!r})"
    
    # Método de Inicialização
    def __init__(self, pais_id, nome, sigla):
        self.pais_id = pais_id
        self.nome = nome 
        self.sigla = sigla

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):  
        return {
            "estado_id": int(self.estado_id),
            "pais_id": int(self.pais_id),
            "nome": self.nome,
            "sigla": self.sigla
        }         

    # Retorna os países cadastrados
    def get_estados(usuario_id):
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela países
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Estados')
            if not acesso_liberado:                
                raise BusinessException('Usuário não Possui permissão para visualização dos estados')
            estados = session.query(Estado).all()   
            return estados 
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')

    # Retorna o Estado informado
    def get_estado_id(usuario_id, estado_id, permissao_pai: str=None):
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
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Estados')
            if not acesso_liberado:                
                raise BusinessException('Usuário não Possui permissão para visualização do estado informado')
            
            # Retorna o grupo selecionado
            sql = select(Estado).where(Estado.estado_id == estado_id)
            estado = session.scalars(sql).one() 
            if not estado:                
                raise BusinessException('Estado não encontrado')                

            return estado 
        
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido') 
    
    def add_estado(usuario_id, aestado):
        try:
            # Verifica se o usuário pode adicionar um novo estado ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Criar_Estados')
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para adicionar novos estados')
            
            # Verifica se os campos estão preenchidos
            if aestado['pais_id'] == '' or  not aestado['pais_id']:
                raise BusinessException('O pais é obrigatório')
            
            if aestado['nome'] == '' or  not aestado['nome']:
                raise BusinessException('Nome do pais é obrigatório')

            if aestado['sigla'] == '' or  not aestado['sigla']:
                raise BusinessException('Sigla do país é obrigatório')
            
            # Verifica se o pais informado existe no sistema
            pais = Pais.get_pais_id(usuario_id, aestado['pais_id'], 'Pode_Criar_Estados')
            if not pais:
                raise BusinessException('País informado não está cadastrado')
                             
            # Verifica se já existe um estado já cadastrado no banco de dados
            rows = session.query(Estado).where(
                and_(
                    Estado.pais_id == aestado['pais_id'],
                    Estado.nome == aestado['nome']
                )).count()   
            if rows > 0:
                raise BusinessException('Estado já cadastrado com este nome')
            
            rows = session.query(Estado).where(
                and_(
                    Estado.pais_id == aestado['pais_id'],
                    Estado.sigla == aestado['sigla']
                )).count()   
            if rows > 0:
                raise BusinessException('Estado já cadastrado com este nome')            
            
            novoEstado = Estado(
                pais_id = int(aestado['pais_id']),
                nome = aestado['nome'].upper().strip(),
                sigla = aestado['sigla'].upper().strip()
            )

            # Adiciona um novo Estado
            session.add(novoEstado)  
            session.commit()
            return novoEstado
        
        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')                  

    # Atualiza um Estado Existente
    def update_estado(usuario_id, estado_id, uestado):
        try:
            # Verifica se o usuário pode adicionar um novo pais ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Atualizar_Estados')
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para editar os dados do estado')

            # Verifica os códigos informados
            if int(uestado['estado_id']) != estado_id:
                raise BusinessException('Erro na identificação do estado')            
            
            # Verifica se os campos estão preenchidos
            if uestado['pais_id'] == '' or  not uestado['pais_id']:
                raise BusinessException('O pais é obrigatório')
            
            if uestado['nome'] == '' or  not uestado['nome']:
                raise BusinessException('Nome do pais é obrigatório')

            if uestado['sigla'] == '' or  not uestado['sigla']:
                raise BusinessException('Sigla do país é obrigatório')                    
                                 
            # Recupera os dados do estado informado
            sql = select(Estado).where(Estado.estado_id == uestado['estado_id'])
            estado = session.scalars(sql).one()
            if not estado:
                raise BusinessException('Estado informado não encontrado')                
            
            # Verifica se o nome do Estado ou Sigla foi alterado.
            # Se sim, precisa checar se já existe um cadastrado no sistema
            if estado.nome != uestado['nome']:
                rows = session.query(Estado).where(
                    and_(
                        Estado.pais_id == uestado['pais_id'],
                        Estado.nome == uestado['nome'],
                        Estado.estado_id!= uestado['estado_id']
                    )).count()
                if rows > 0:
                    raise BusinessException('Nome informado já cadastrado para outro estado')

            if estado.sigla != uestado['sigla']:
                rows = session.query(Estado).where(
                    and_(
                        Estado.pais_id == uestado['pais_id'],
                        Estado.sigla == uestado['sigla'],
                        Estado.estado_id!= uestado['estado_id']
                    )).count()
                if rows > 0:
                    raise BusinessException('Sigla informada já cadastrada para outro estado')                

            # Atualiza o objeto a ser alterado
            estado.nome = uestado['nome'].upper().strip()
            estado.sigla = uestado['sigla'].upper().strip()
            estado.pais_id = uestado['pais_id']

            # Comita as alterações no banco de dados            
            session.commit()
            return estado
        
        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')