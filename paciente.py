from config import parameters
from sqlalchemy import Column
from sqlalchemy import create_engine, select, and_, func
from sqlalchemy.dialects.sqlite import (INTEGER, VARCHAR, DATETIME)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from config import parameters

from datetime import datetime, time
import pytz
from calendar import monthrange

from config import parameters
from cidade import Cidade
from seguranca.business_exception import BusinessException
from seguranca.permissoes import Permissao

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Paciente(Base):
    # Identifica a tabela no Banco de Dados
    __tablename__ = "PACIENTE"

    # Propriedades da Classe
    paciente_id = Column(INTEGER, primary_key=True)
    cidade_id = Column(INTEGER)
    nome = Column(VARCHAR(250))
    data_nasc = Column(DATETIME, nullable=False)
    tel_1 = Column(INTEGER)
    tel_2 = Column(INTEGER)
    logradouro = Column(VARCHAR(400))
    numero = Column(VARCHAR(20))
    complemento = Column(VARCHAR(50))
    cep = Column(VARCHAR(10))
    hygia = Column(VARCHAR(20))
    data_cadastro = Column(DATETIME, nullable=False)

    # Método de Representação
    def __repr__(self) -> str:
        return f"Paciente(paciente_id={self.paciente_id!r},cidade_id={self.cidade_id!r}, nome={self.nome!r}" \
               f"data_nasc={self.data_nasc!r},tel_1={self.tel_1!r}, tel_2={self.tel_2!r}" \
               f"logradouro={self.logradouro!r},numero={self.numero!r}, complemento={self.complemento!r}" \
               f"cep={self.cep!r},hygia={self.hygia!r},data_cadastro={self.data_cadastro!r})"

    # Método de Inicialização
    def __init__(self, cidade_id, nome, data_nasc, tel_1, tel_2, logradouro, numero, complemento, cep, hygia, data_cadastro):
        self.cidade_id = cidade_id
        self.nome = nome
        self.data_nasc = data_nasc
        self.tel_1 = tel_1
        self.tel_2 = tel_2
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.cep = cep
        self.hygia = hygia
        self.data_cadastro = data_cadastro

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):
        return {
            "paciente_id": int(self.paciente_id),
            "cidade_id": int(self.cidade_id),
            "nome": self.nome,
            "data_nasc": self.data_nasc,
            "tel_1":self.tel_1,
            "tel_2":self.tel_2,
            "logradouro":self.logradouro,
            "numero":self.numero,
            "complemento":self.complemento,
            "cep":self.cep,
            "hygia":self.hygia,
            "data_cadastro":self.data_cadastro 
        }
        
    def formata_data(d):
        # 1993-12-01T02:00:00.000Z
        r = []
        s1 = str(d).split('T')
        d1 = s1[0].split('-')
        
        for x in d1:
            r.append(int(x))
        dt = datetime(r[0], r[1], r[2])
        return dt 
           
         
    # Retorna o total de pacientes cadastrados no sistema
    def get_total_pacientes(usuario_id):
        # Verifica se o usuário pode ver o conteúdo da tabela de pacientes
        acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Pacientes')
        if not acesso_liberado:
            return 0
        else:
            total = session.query(func.count(Paciente.paciente_id)).scalar()
            return total
        
    def get_cadastrados_mes_corrente(usuario_id):
        # Verifica se o usuário pode ver o conteúdo da tabela de pacientes
        acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Pacientes')
        if not acesso_liberado:
            return 0
        else:
            
            #Calcula o primeiro dia do mês      
            hoje = datetime.today()
            inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=1 )
            fim_mes = hoje.replace(day=monthrange(hoje.year, hoje.month)[1], hour=23, minute=59, second=59)            
            total = session.query(func.count(Paciente.paciente_id)).filter(Paciente.data_cadastro.between(inicio_mes, fim_mes)).scalar()
            return total  
    
    def get_pacientes(usuario_id):
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela de pacientes
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Pacientes')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização dos pacientes')        
            
            listpaciente = []
            pacientes = session.query(Paciente, Cidade).join(Cidade, Paciente.cidade_id == Cidade.cidade_id).order_by(Paciente.nome).all()

            for paciente in pacientes:
                p =  {             
                    "paciente_id": int(paciente.Paciente.paciente_id),
                    "cidade_id": int(paciente.Cidade.cidade_id),
                    "cidade_nome": str(paciente.Cidade.nome),
                    "nome": str(paciente.Paciente.nome),
                    "data_nasc": datetime.isoformat(paciente.Paciente.data_nasc),
                    "tel_1": str(paciente.Paciente.tel_1),
                    "tel_2": str(paciente.Paciente.tel_2),
                    "logradouro": str(paciente.Paciente.logradouro),
                    "numero": str(paciente.Paciente.numero),
                    "complemento": str(paciente.Paciente.complemento),
                    "cep": str(paciente.Paciente.cep),
                    "hygia": str(paciente.Paciente.hygia),
                    "data_cadastro": datetime.isoformat(paciente.Paciente.data_cadastro)

                }   
                listpaciente.append(p)              
            
            return listpaciente
        
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')           
    
    # Retorna o Paciente informado
    def get_paciente_id(usuario_id, paciente_id, permissao_pai: str = None):
        """
        Este método utiliza um conceito de permissão pai, quando invocado por uma outra classe.
        Facilita para não ter que dar outras permissões para o usuário
        Utiliza a permissão do método que a chamou
        """
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela Paciente
            acesso_liberado = False
            if permissao_pai:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, permissao_pai)
            else:
                acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Pacientes')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização do Paciente informado')

            # Retorna o grupo selecionado
            paciente = session.query(Paciente).where(Paciente.paciente_id == paciente_id).all()
            if not paciente:
                raise BusinessException('Paciente não encontrado')

            return paciente

        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')

    def add_paciente(usuario_id, apaciente):
        try:
            # Verifica se o usuário pode adicionar um novo Paciente ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Criar_Pacientes')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para adicionar novos pacientes')

            # Verifica se os campos estão preenchidos
            if apaciente['cidade_id'] == '' or not apaciente['cidade_id']:
                raise BusinessException('A cidade é obrigatória')

            if apaciente['nome'] == '' or not apaciente['nome']:
                raise BusinessException('Nome do Paciente é obrigatório')

            if apaciente['data_nasc'] == '' or not apaciente['data_nasc']:
                raise BusinessException('Data de nascimento do Paciente é obrigatória')

            if apaciente['tel_1'] == '' or not apaciente['tel_1']:
                raise BusinessException('Telefone do Paciente é obrigatório')

            if apaciente['logradouro'] == '' or not apaciente['logradouro']:
                raise BusinessException('Logradouro do Paciente é obrigatório')

            if apaciente['numero'] == '' or not apaciente['numero']:
                raise BusinessException('Número do endereço do Paciente é obrigatório')

            if apaciente['hygia'] == '' or not apaciente['hygia']:
                raise BusinessException('Hygia do Paciente é obrigatório')

            # Verifica se a cidade informada existe no sistema -- Necessário criar a classe endereco
            cidade = Cidade.get_cidade_id(usuario_id, apaciente['cidade_id'], 'Pode_Criar_Paciente')
            if not cidade:
                raise BusinessException('Cidade informada não está cadastrado')

            # Verifica se existe um Paciente já cadastrado no banco de dados
            rows = session.query(Paciente).where(
                and_(
                    Paciente.hygia == apaciente['hygia']
                )).count()
            if rows > 0:
                raise BusinessException('Paciente já cadastrado com este número hygia')
            
            novoPaciente = Paciente(
                cidade_id=apaciente['cidade_id'],
                nome=apaciente['nome'].upper().strip(),
                data_nasc = Paciente.formata_data(apaciente['data_nasc']),
                tel_1 = apaciente['tel_1'],
                tel_2 = apaciente['tel_2'],
                logradouro = apaciente['logradouro'].upper().strip(),
                numero = apaciente['numero'].upper().strip(),
                complemento = apaciente['complemento'].upper().strip(),
                cep = apaciente['cep'].strip(),
                hygia = apaciente['hygia'].upper().strip(),
                data_cadastro =  Paciente.formata_data(datetime.isoformat(datetime.now(pytz.timezone(parameters['TIMEZONE']))))
            )

            # Adiciona um novo Paciente
            session.add(novoPaciente)
            session.commit()
            return novoPaciente

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')

            # Atualiza um Paciente Existente

    def update_paciente(usuario_id, upaciente):
        try:
            # Verifica se o usuário pode adicionar um novo paciente ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Atualizar_Pacientes')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para editar os dados do Paciente')

            # Verifica se os campos estão preenchidos
            if upaciente['cidade_id'] == '' or not upaciente['cidade_id']:
                raise BusinessException('A cidade é obrigatória')

            if upaciente['nome'] == '' or not upaciente['nome']:
                raise BusinessException('Nome do Paciente é obrigatório')

            if upaciente['data_nasc'] == '' or not upaciente['data_nasc']:
                raise BusinessException('Data de nascimento do Paciente é obrigatória')

            if upaciente['tel_1'] == '' or not upaciente['tel_1']:
                raise BusinessException('Telefone do Paciente é obrigatório')

            if upaciente['logradouro'] == '' or not upaciente['logradouro']:
                raise BusinessException('Logradouro do Paciente é obrigatório')

            if upaciente['numero'] == '' or not upaciente['numero']:
                raise BusinessException('Número do endereço do Paciente é obrigatório')

            if upaciente['hygia'] == '' or not upaciente['hygia']:
                raise BusinessException('Hygia do Paciente é obrigatório')

            # Recupera os dados do Paciente informado
            sql = select(Paciente).where(Paciente.paciente_id == upaciente['paciente_id'])
            paciente = session.scalars(sql).one()
            if not paciente:
                raise BusinessException('Paciente informado não encontrado')

            # Verifica se o nome do Paciente foi alterado.
            # Se sim, precisa checar se já existe um cadastrado no sistema
            if paciente.nome != upaciente['nome']:
                rows = session.query(Paciente).where(
                    and_(
                        Paciente.nome == upaciente['nome'],
                        Paciente.hygia == upaciente['hygia']
                    )).count()
                if rows > 0:
                    raise BusinessException('Nome e Hygia informado já cadastrado para outro Paciente')

            # Atualiza o objeto a ser alterado
            paciente.nome = upaciente['nome'].upper().strip()
            paciente.hygia = upaciente['hygia'].upper().strip()
            paciente.tel_1 = upaciente['tel_1']
            paciente.tel_2 = upaciente['tel_2']
            paciente.cidade_id = upaciente['cidade_id']
            paciente.data_nasc = upaciente['data_nasc']
            paciente.logradouro = upaciente['logradouro'].upper().strip()
            paciente.numero = upaciente['numero'].upper().strip()
            paciente.complemento = upaciente['complemento'].upper().strip(),
            paciente.cep = upaciente['cep'].strip(),

            # Comita as alterações no banco de dados
            session.commit()
            return paciente

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')
    
    # Exporta dados para o Dashboard
    def get_cadastros_ano(usuario_id):

        # Verifica se o usuário pode adicionar um novo paciente ao sistema
        acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Atualizar_Pacientes')
        if not acesso_liberado:
            return None        
        else: 
            cadastros_mes = []
            hoje = datetime.today()
            ano = hoje.year
            inicio_ano = hoje.replace(day=1, month=1, year=ano, hour=0, minute=0, second=1 )
            fim_ano = hoje.replace(day=31, month=12, year=ano, hour=23, minute=59, second=59)            
            total = session.query(func.strftime("%m", Paciente.data_cadastro), func.count(func.strftime("%m", Paciente.data_cadastro)))\
                .filter(Paciente.data_cadastro.between(inicio_ano, fim_ano))\
                .group_by(func.strftime("%m", Paciente.data_cadastro), func.strftime("%m", Paciente.data_cadastro)).all()
            
            for i in range(1,13):
                y = ''
                if i < 10:
                    y = f'0{i}'
                else:
                    y = str(i)
                
                #at = {f'{y}' : 0}
                at = 0
                
                for mes in total:
                  
                    if mes[0] == y:
                        #at = {f'{y}' : mes[1]}
                        at = mes[1]
                        
                cadastros_mes.append(at)
        
        return cadastros_mes            