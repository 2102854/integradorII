from sqlalchemy import  Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import (BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, NUMERIC, JSON, SMALLINT, TEXT, TIME, TIMESTAMP, VARCHAR)

#############################
# Classes do banco de dados #
#############################

Base = declarative_base()

class Pais (Base):
    __tablename__ = "PAIS"

    pais_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250))
    sigla = Column(TEXT(3))

    def __repr__(self) -> str:
        return f"Pais(pais_id={self.pais_id!r}, nome={self.nome!r}, sigla={self.sigla!r})"
    
    def __init__(self, nome, sigla):
        self.nome = nome 
        self.sigla = sigla

class Estado (Base):
    __tablename__ = "ESTADO"

    estado_id = Column(INTEGER, primary_key=True)
    pais_id = Column(INTEGER)
    nome = Column(TEXT(250))
    sigla = Column(TEXT(3))

    def __repr__(self) -> str:
        return f"Estado(estado_id={self.estado_id!r}, pais_id={self.pais_id!r}, nome={self.nome!r}, sigla={self.sigla!r})"
    
    def __init__(self, pais_id, nome, sigla):
        self.pais_id = pais_id
        self.nome = nome
        self.sigla = sigla

class Cidade (Base):
    __tablename__ = "CIDADE"

    cidade_id = Column(INTEGER, primary_key=True)
    estado_id = Column(INTEGER, nullable=False)
    nome = Column(TEXT(250), nullable=False)
    distancia_km = Column(NUMERIC(10,2), nullable=False)
    valor_pedagio = Column(NUMERIC(10,2), nullable=False)
 
    def __repr__(self) -> str:
        return f"Cidade(cidade_id={self.cidade_id!r}, estado_id={self.estado_id!r}, nome={self.nome!r}, distancia_km={self.distancia_km!r}, valor_pedagio={self.valor_pedagio!r} )"
    
    def __init__(self, estado_id, nome, distancia_km, valor_pedagio):
        self.estado_id = estado_id
        self.nome = nome 
        self.distancia_km = distancia_km
        self.valor_pedagio = valor_pedagio

class Endereco (Base):
    __tablename__ = "ENDERECO"

    endereco_id = Column(INTEGER, primary_key=True)
    cidade_id = Column(INTEGER, nullable=False)
    logradouro = Column(TEXT(400), nullable=False)
    numero = Column(TEXT(20), nullable=False)
    complemento = Column(TEXT(50), nullable=False)
 
    def __repr__(self) -> str:
        return f"Endereco(endereco_id={self.endereco_id!r},cidade_id={self.cidade_id!r}, logradouro={self.logradouro!r}, numero={self.numero!r}, complemento={self.complemento!r})"
    
    def __init__(self, logradouro):
        self.nome = logradouro 

class Veiculo (Base):
    __tablename__ = "VEICULO"

    veiculo_id = Column(INTEGER, primary_key=True)
    modelo = Column(TEXT(250), nullable=False)
    placa = Column(TEXT(20), nullable=False)
    capacidade = Column(NUMERIC(3), nullable=False)
    media_consumo = Column(NUMERIC(10,2), nullable=False)

    def __repr__(self) -> str:
        return f"Veiculo(veiculo_id={self.veiculo_id!r},modelo={self.modelo!r},placa={self.placa!r},capacidade={self.capacidade!r}, media_consumo={self.media_consumo!r})"
    
    def __init__(self, modelo):
        self.nome = modelo 
     
class Hospital (Base):
    __tablename__ = "HOSPITAL"

    hospital_id = Column(INTEGER, primary_key=True)
    endereco_id = Column(INTEGER, nullable=False)
    nome = Column(TEXT(250), nullable=False)

    def __repr__(self) -> str:
        return f"Hospital(hospital_id={self.hospital_id!r}, nome={self.nome!r}, endereco_id={self.endereco_id!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Paciente (Base):
    __tablename__ = "PACIENTE"

    paciente_id = Column(INTEGER, primary_key=True)
    cidade_id = Column(INTEGER, nullable=False)
    hygia = Column(TEXT(20),nullable=False)
    nome = Column(TEXT(250), nullable=False)
    data_nasc = Column(TEXT(10), nullable=False)
    tel_1 = Column(TEXT(11), nullable=False)
    tel_2 = Column(TEXT(11), nullable=True)
    logradouro = Column(TEXT(400), nullable=False)
    numero = Column(TEXT(20), nullable=False)
    complemento = Column(TEXT(50), nullable=False)
    cep = Column(TEXT(10), nullable=False)

    def __repr__(self) -> str:
        return f"Paciente(paciente_id={self.paciente_id!r},cidade_id={self.cidade_id!r},hygia={self.hygia},nome={self.nome!r},data_nasc={self.data_nasc!r},tel_1={self.tel_1!r},tel_2={self.tel_2!r},logradouro={self.logradouro!r}, numero={self.numero!r}, complemento={self.complemento!r}, cep={self.cep!r})"
    
    def __init__(self, cidade_id, hygia, nome, data_nasc, tel_1, tel_2, logradouro, numero, complemento, cep):
        self.cidade_id = cidade_id
        self.hygia = hygia
        self.nome = nome 
        self.data_nasc = data_nasc
        self.tel_1 = tel_1
        self.tel_2 = tel_2
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.cep = cep
        
    # for build json format
    def obj_to_dict(self):  
        return {
            "paciente_id": str(self.paciente_id),
            "cidade_id": str(self.cidade_id),
            "hygia": self.hygia,
            "nome": self.nome,
            "data_nasc": self.data_nasc,
            "tel_1": self.tel_1,
            "tel_2": self.tel_2,
            "logradouro": self.logradouro,
            "numero": self.numero,
            "complemento": self.complemento,
            "cep": self.cep
        }        

class Usuario (Base):
    __tablename__ = "USUARIO"

    usuario_id = Column(INTEGER, primary_key=True)
    primeiro_nome = Column(TEXT(30), nullable=False)
    sobrenome =  Column(TEXT(100), nullable=False)
    username = Column(TEXT(150), nullable=False)
    senha = Column(TEXT(128), nullable=False)
    email = Column(TEXT(250), nullable=False)
    ativo = Column(BOOLEAN, nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Responsavel(tipo_Responsavel_id={self.tipo_responsavel_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Motorista (Base):
    __tablename__ = "MOTORISTA"

    motorista_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250), nullable=False)
    numero_habilitacao = Column(TEXT(50), nullable=False)
    carga_horaria = Column(NUMERIC(5, 2), nullable=False)

    def __repr__(self) -> str:
        return f"Responsavel(responsavel_id={self.motorista_id!r},nome={self.nome!r},numero_habilitacao={self.numero_habilitacao!r},carga_horaria={self.carga_horaria!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Tipo_Doenca (Base):
    __tablename__ = "TIPO_DOENCA"

    tipo_doenca_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Doenca(tipo_doenca_id={self.tipo_doenca_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Tipo_Encaminhamento (Base):
    __tablename__ = "TIPO_ENCAMINHAMENTO"

    tipo_encaminhamento_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Encaminhamento(tipo_encaminhamento_id={self.tipo_encaminhamento_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Tipo_Remocao (Base):
    __tablename__ = "TIPO_REMOCAO"

    tipo_remocao_id = Column(INTEGER, primary_key=True)
    nome = Column(TEXT(250), nullable=False)

    def __repr__(self) -> str:
        return f"Tipo_Remocao(tipo_remocao_id={self.tipo_remocao_id!r},nome={self.nome!r})"
    
    def __init__(self, nome):
        self.nome = nome 

class Agendamento (Base):
    __tablename__ = "AGENDAMENTO"

    agendamento_id = Column(INTEGER, primary_key=True)
    paciente_id = Column(INTEGER, nullable=False)
    tipo_encaminhamento_id = Column(INTEGER, nullable=False)
    tipo_doenca_id = Column(INTEGER, nullable=False)
    tipo_remocao_id = Column(INTEGER, nullable=False)
    hospital_id = Column(INTEGER, nullable=False)
    veiculo_id = Column(INTEGER, nullable=False)
    responsavel_pac = Column(TEXT(200), nullable=False)
    usuario_id = Column(INTEGER, nullable=True)
    motorista_id = Column(INTEGER, nullable=False)
    estado_geral_paciente = Column(TEXT(500), nullable=False)
    data_remocao = Column(TEXT(20), nullable=False)
    saida_prevista = Column(TEXT(20), nullable=False)
    observacao = Column(TEXT(500), nullable=False)
    custo_IFD = Column(NUMERIC(5, 2), nullable=False)
    custo_estadia = Column(NUMERIC(5, 2), nullable=False)   

    def __repr__(self) -> str:
        return (f"Agendamento(agendamento_id={self.agendamento_id!r},paciente_id={self.paciente_id!r}), responsavel_pac={self.responsavel_pac!r}),\
                tipo_encaminhamento_id={self.tipo_encaminhamento_id!r}),tipo_doenca_id={self.tipo_doenca_id!r}), tipo_remocao_id={self.tipo_remocao_id!r}),\
                hospital_id={self.hospital_id!r}), veiculo_id={self.veiculo_id!r}), estado_geral_paciente={self.estado_geral_paciente!r}),\
                data_remocao={self.data_remocao!r}), saida_prevista={self.saida_prevista!r}), observacao={self.observacao!r}), \
                custo_IFD={self.custo_IFD!r}), custo_estadia={self.custo_estadia!r}), motorista_id={self.motorista_id!r}), usuario_id={self.usuario_id!r})")
    
    def __init__(self, paciente_id, tipo_encaminhamento_id, tipo_doenca_id, tipo_remocao_id, hospital_id, veiculo_id, responsavel_pac, 
                 usuario_id, motorista_id, estado_geral_paciente, data_remocao, saida_prevista, observacao, custo_IFD, custo_estadia):  
        self.paciente_id = paciente_id
        self.tipo_encaminhamento_id = tipo_encaminhamento_id
        self.tipo_doenca_id = tipo_doenca_id
        self.tipo_remocao_id = tipo_remocao_id
        self.hospital_id = hospital_id
        self.veiculo_id = veiculo_id
        self.responsavel_pac = responsavel_pac
        self.usuario_id = usuario_id
        self.motorista_id = motorista_id
        self.estado_geral_paciente = estado_geral_paciente
        self.data_remocao = data_remocao
        self.saida_prevista = saida_prevista
        self.observacao = observacao 
        self.custo_IFD = custo_IFD
        self.custo_estadia = custo_estadia