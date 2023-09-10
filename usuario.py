
from config import parameters
from sqlalchemy import  Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)
from sqlalchemy import create_engine, func
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op
from werkzeug.security import generate_password_hash, check_password_hash

from seguranca.pemissoes import Permissao
from seguranca.usuario_permissao import Usuario_Permissao
from seguranca.business_exception import BusinessException
import uuid
import re 

regex = '[a-z0-9!#$%&’*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&’*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?'

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Usuario (Base):
    __tablename__ = "USUARIO"

    usuario_id = Column(INTEGER, primary_key=True)
    primeiro_nome = Column(TEXT(30), nullable=False)
    sobrenome =  Column(TEXT(100), nullable=False)
    username = Column(TEXT(150), nullable=False)
    senha = Column(VARCHAR(500), nullable=False)
    email = Column(VARCHAR(250), nullable=False)
    ativo = Column(BOOLEAN, nullable=False)
    chave_publica = Column(TEXT(100), nullable=False)

    def __repr__(self) -> str:
        return f"Usuario(usuario_id={self.usuario_id!r},primeiro_nome={self.primeiro_nome!r},sobrenome={self.sobrenome!r},\
            senha={self.senha!r},email={self.ativo!r},email={self.ativo!r},email={self.chave_publica!r})"
    
    def __init__(self, primeiro_nome, sobrenome, username, senha, email, ativo):
        self.primeiro_nome = primeiro_nome
        self.sobrenome = sobrenome
        self.username = username
        self.senha = senha
        self.email = email
        self.ativo = ativo
    
    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):  
        return {
            'usuario_id': str(self.usuario_id),
            'primeiro_nome': self.primeiro_nome,
            'sobrenome': self.sobrenome,
            'username': self.username,
            'senha': self.senha,
            'email': self.email,
            'ativo': self.ativo,
            'chave_publica' : self.chave_publica
        }   
    
    # Validador de e-mail
    def email_eh_valido(email):  
        if(re.search(regex,email)):  
            return True   
        else:  
            return False           
    
    # Retorna os usuários cadastrados
    def get_usuarios(usuario_id):
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela usuário
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Usuarios')
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para visualização da lista de usuários')
            usuarios = session.query(Usuario).all()  
            #Usuario.update_usuarios()

            return usuarios 
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')

    # Retorna os dados do usuário informado
    def get_usuario_id(usuario_id, id, permissao_pai: str=None):
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
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Usuarios')
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para visualização de dados de usuários')
            
            # Retorna o grupo selecionado
            grupo = session.query(Usuario).where(Usuario.usuario_id == id).all()  
            if not grupo:                
                raise BusinessException('Usuário não encontrado')

            return grupo 
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido') 


    def add_usuarios(usuario_id, primeiro_nome, sobrenome, senha, email):
        try:
            # Verifica se o usuário pode adicionar um novo usuario usuário
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Adicionar_Usuarios')
            if not acesso_liberado:                
                raise BusinessException('Usuário não possui permissão para adicionar novos usuários')
            
            # Verifica se os campos estão preenchidos
            if primeiro_nome == '' or  not primeiro_nome:
                raise BusinessException('Primeiro nome é obrigatório')

            if sobrenome == '' or  not sobrenome:
                raise BusinessException('Sobrenome é obrigatório')            
            
            if senha == '' or  not senha:
                raise BusinessException('Senha é obrigatório')  

            if email == '' or  not email:
                raise BusinessException('E-mail é obrigatório')  

            if Usuario.email_eh_valido(email):
                raise BusinessException('E-mail não é Válido')                       

            # Verifica se já existe um e-mail cadastrado no banco de dados
            rows = session.query(Usuario).where(Usuario.email == email).count()   
            if rows > 0:
                raise BusinessException('E-mail já cadastrado no banco de dados')

            # Gera o username do usuário
            n = sobrenome.split()
            x = len(n)

            username = ''
            rows = 0
            for l in primeiro_nome:
                pn = pn.join(l)
                username = pn + '.' + n[x -1]
                # Verifcar se este username já existe no banco de dados
                rows = session.query(Usuario).where(Usuario.username == username).count()
                if rows == 0:
                    break

            novoUsuario = Usuario(
                primeiro_nome = primeiro_nome.upper().strip(),
                sobrenome = sobrenome.upper().strip(),
                username = username,
                email = email.upper(),
                ativo = True,
                senha = generate_password_hash(senha), # Criptografa a senha do usuário
                chave_publica = str(uuid.uuid4()) # Gera uma chave de identificador único para o usuário
            )

            # Adiciona um novo usuário
            session.add(novoUsuario)        
            session.commit()     
            return 'ok'
        
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')    
    
    # Retorna os dados do usuário pelo parametro e-mail
    def get_usuario_by_email(email):
        sql = select(Usuario).where(Usuario.email == email)
        usuario = session.scalars(sql).one()
        return usuario

    # Retorna os dados do usuário pela chave pública
    def get_usuario_by_chave_publica(chave_publica):
        sql = select(Usuario).where(Usuario.chave_publica == chave_publica)
        usuario = session.scalars(sql).one()
        return usuario    

    def update_usuarios():
        sql = select(Usuario).where(Usuario.usuario_id == 3)
        usuario = session.scalars(sql).one()
                
        usuario.chave_publica = str(uuid.uuid4())    
        session.commit()    
    # Exemplo para criptografia de senha
    # usuario.senha = generate_password_hash(usuario.senha)
    # v = check_password_hash(usuario.senha, '123456')

    # Retorna as permissões do usuário
    def get_permissoes_usuario(usuario_id):

        permissoes = session.query(Permissao.permissao)\
            .join(Usuario_Permissao, Permissao.permissao_id == Usuario_Permissao.permissao_id)\
            .where(Usuario_Permissao.usuario_id == usuario_id)\
            .order_by(Permissao.permissao).all()
        return permissoes    