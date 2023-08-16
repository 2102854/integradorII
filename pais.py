from config import parameters
from sqlalchemy import  Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)
from sqlalchemy import create_engine, func
from sqlalchemy import select
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
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 1)
            if not acesso_liberado:                
                raise BusinessException('Usuário não Possui permissão para visualização dos países')
            paises = session.query(Pais).all()   
            return paises 
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            # tratamento de erro desconhecido
            return Exception('Erro desconhecido')
      
    
    # Retorna os países cadastrados
    #def get_paise_by_id(self, id):
        #nome = request.args.get('nome', default = '', type = str)
    #    if nome == '':    
    #        paises = session.query(Pais).all()        
    #    else:
    #        paises = session.query(Pais).filter(ilike_op(Pais.nome,f'%{nome}%')).all()
    #    return render_template('paises.html',paises=paises) 

    # Retorna os países cadastrados
    #def get_paise_by_name(self, id):
        #nome = request.args.get('nome', default = '', type = str)
    #    if nome == '':    
    #        paises = session.query(Pais).all()        
    #    else:
    #        paises = session.query(Pais).filter(ilike_op(Pais.nome,f'%{nome}%')).all()
    #    return render_template('paises.html',paises=paises)          

    # Adiciona um novo País
    #def add():
    #    if request.method == 'POST':

    #        novoPais = Pais(request.form['nome'], request.form['sigla'])
    #        session.add(novoPais)        
    #        session.commit()        
    #        return redirect(url_for('paises'))    
        
    #    else:
    #        return render_template('form_cad_pais.html')
    
    # Edita um país    
    #def edit(pais_id):
        
    #    if request.method == 'POST':
            # Executa a alteração do país
    #        sql = select(Pais).where(Pais.pais_id == pais_id)
    #        result = session.scalars(sql).one()
    #        result.nome = request.form['nome']
    #        result.sigla = request.form['sigla']        
    #        session.commit() 

            # Volta para a página de países
    #        return redirect(url_for('paises'))
    #    else:

            # Pesquisa pelo Id do pais
    #        sql = select(Pais).where(Pais.pais_id == pais_id)
    #        result = session.scalars(sql).one()
    #        return render_template('form_edt_pais.html',pais_id=pais_id, nome=result.nome, sigla=result.sigla )