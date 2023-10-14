from sqlalchemy import Column
from sqlalchemy import create_engine, func, select, and_
from sqlalchemy.dialects.sqlite import (INTEGER, VARCHAR, DATETIME, FLOAT)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from config import parameters
from seguranca.business_exception import BusinessException
from seguranca.permissoes import Permissao

from paciente import Paciente
from hospital import Hospital
from tipo_encaminhamento import Tipo_Encaminhamento
from tipo_doenca import Tipo_Doenca
from tipo_remocao import Tipo_Remocao
from motorista import Motorista
from veiculo import Veiculo
from usuario import Usuario
from datetime import datetime, timedelta 
from calendar import monthrange
from flask import jsonify

Base = declarative_base()

# Mapeia o banco de dados
engine = create_engine(parameters['SQLALCHEMY_DATABASE_URI'], echo=True)
session = Session(engine)

class Agendamento(Base):
    # Identifica a tabela no Banco de Dados
    __tablename__ = "AGENDAMENTO"
    
    # Propriedades da Classe
    agendamento_id = Column(INTEGER, primary_key=True)
    paciente_id = Column(INTEGER)
    tipo_encaminhamento_id = Column(INTEGER)
    tipo_doenca_id = Column(INTEGER)
    tipo_remocao_id = Column(INTEGER)
    hospital_id = Column(INTEGER)
    veiculo_id = Column(INTEGER)
    usuario_id = Column(INTEGER)
    motorista_id = Column(INTEGER)
    responsavel_pac = Column(VARCHAR(250))
    data_remocao = Column(DATETIME)
    saida_prevista = Column(DATETIME)
    observacao = Column(VARCHAR(250))
    custo_ifd = Column(FLOAT)
    custo_estadia = Column(FLOAT)
    estado_geral_paciente = Column(VARCHAR(250))

    # Método de Representação
    def __repr__(self) -> str:
        return f"Agendamento(agendamento_id={self.agendamento_id!r},paciente_id={self.paciente_id!r}, tipo_encaminhamento_id={self.tipo_encaminhamento_id!r}\
            tipo_doenca_id={self.tipo_doenca_id!r},tipo_remocao_id={self.tipo_remocao_id!r}, hospital_id={self.hospital_id!r}, veiculo_id={self.veiculo_id!r}\
            usuario_id={self.usuario_id!r},motorista_id={self.motorista_id!r}, responsavel_pac={self.responsavel_pac!r}, data_remocao={self.data_remocao!r}\
            saida_prevista={self.saida_prevista!r},observacao={self.observacao!r}, custo_ifd={self.custo_ifd!r}, custo_estadia={self.custo_estadia!r}\
            estado_geral_paciente={self.estado_geral_paciente!r}\
            )"

    # Método de Inicialização
    def __init__(self, agendamento_id, paciente_id, tipo_encaminhamento_id, tipo_doenca_id, tipo_remocao_id, hospital_id, veiculo_id, usuario_id, motorista_id,\
        responsavel_pac, data_remocao, saida_prevista, observacao, custo_ifd, custo_estadia, estado_geral_paciente ):
        self.agendamento_id = agendamento_id
        self.paciente_id = paciente_id
        self.tipo_encaminhamento_id = tipo_encaminhamento_id
        self.tipo_doenca_id = tipo_doenca_id
        self.tipo_remocao_id = tipo_remocao_id
        self.hospital_id = hospital_id
        self.veiculo_id = veiculo_id
        self.usuario_id = usuario_id
        self.motorista_id = motorista_id
        self.responsavel_pac = responsavel_pac
        self.data_remocao = data_remocao
        self.saida_prevista = saida_prevista
        self.observacao = observacao
        self.custo_ifd = custo_ifd
        self.custo_estadia = custo_estadia
        self.estado_geral_paciente = estado_geral_paciente

    # Retorna o resultado da Classe em formato json
    def obj_to_dict(self):
        return {
            "agendamento_id": int(self.agendamento_id),
            "paciente_id": int(self.paciente_id),
            "tipo_encaminhamento_id": int(self.tipo_encaminhamento_id),
            "tipo_doenca_id": int(self.tipo_doenca_id),
            "tipo_remocao_id": int(self.tipo_remocao_id),
            "hospital_id": int(self.hospital_id),
            "veiculo_id": int(self.veiculo_id),
            "motorista_id": int(self.motorista_id),
            "responsavel_pac": self.responsavel_pac,
            "data_remocao": str(self.data_remocao),
            "saida_prevista": str(self.saida_prevista),            
            "observacao": self.observacao,
            "custo_ifd": self.custo_ifd,
            "custo_estadia": self.custo_estadia,
            "estado_geral_paciente": self.estado_geral_paciente
        }

    # Retorna o total de pacientes cadastrados no sistema
    def get_total_agendamento(usuario_id):
        # Verifica se o usuário pode ver o conteúdo da tabela hospital
        acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Agendamentos')
        if not acesso_liberado:
            return 0
        else:
            total = session.query(func.count(Agendamento.agendamento_id)).scalar()
            return total
    
    def get_last_agendamentos(usuario_id):        
        listAgendamentos = []
        # Verifica se o usuário pode ver o conteúdo da tabela hospital
        acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Agendamentos')
        if not acesso_liberado:
            return listAgendamentos
        else:           
            agendamentos = (session.query(Agendamento, Paciente, Hospital,Tipo_Encaminhamento )
                .join(Paciente, Agendamento.paciente_id == Paciente.paciente_id)
                .join(Hospital, Agendamento.hospital_id == Hospital.hospital_id)
                .order_by(Agendamento.agendamento_id.desc()).limit(10).all()
            )
            
            for agendamento in agendamentos:
                ag =  {
                    "agendamento_id": agendamento.Agendamento.agendamento_id,
                    "nome": agendamento.Paciente.nome,
                    "data_nascimento": datetime.isoformat(agendamento.Paciente.data_nasc),
                    "data_remocao": datetime.isoformat(agendamento.Agendamento.data_remocao),
                    "hospital": agendamento.Hospital.nome
                }   
                listAgendamentos.append(ag)   

        return listAgendamentos

    def get_agendamentos_ano(usuario_id):        
        acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Agendamentos')
        if not acesso_liberado:
            return None
        else: 
            atendimentos_mes = []
            hoje = datetime.today()
            ano = hoje.year
            inicio_ano = hoje.replace(day=1, month=1, year=ano, hour=0, minute=0, second=1 )
            fim_ano = hoje.replace(day=31, month=12, year=ano, hour=23, minute=59, second=59)            
            total = session.query(func.strftime("%m", Agendamento.data_remocao), func.count(func.strftime("%m", Agendamento.data_remocao)))\
                .filter(Agendamento.data_remocao.between(inicio_ano, fim_ano))\
                .group_by(func.strftime("%m", Agendamento.data_remocao), func.strftime("%m", Agendamento.data_remocao)).all()
            
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
                        
                atendimentos_mes.append(at)
        
        return atendimentos_mes

    #Retorna os agendamentos cadastrados
    def get_agendamentos(usuario_id):
        listAgendamentos = []
        try:
            # Verifica se o usuário pode ver o conteúdo da tabela de pacientes
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Visualizar_Agendamentos')
            if not acesso_liberado:
                raise BusinessException('Usuário não Possui permissão para visualização dos agendamentos')
            
            agendamentos = (
                session.query(
                    Agendamento, Paciente, Hospital, Tipo_Encaminhamento, Tipo_Doenca, Tipo_Remocao, 
                    Veiculo, Usuario, Motorista
                )
                .join(Paciente, Agendamento.paciente_id == Paciente.paciente_id)
                .join(Hospital, Agendamento.hospital_id == Hospital.hospital_id)
                .join(Tipo_Encaminhamento, Agendamento.tipo_encaminhamento_id ==  Tipo_Encaminhamento.tipo_encaminhamento_id)
                .join(Tipo_Doenca, Agendamento.tipo_doenca_id == Tipo_Doenca.tipo_doenca_id)
                .join(Tipo_Remocao, Agendamento.tipo_remocao_id == Tipo_Remocao.tipo_remocao_id)
                .join(Veiculo, Agendamento.veiculo_id == Veiculo.veiculo_id)
                .join(Usuario, Agendamento.usuario_id == Usuario.usuario_id)
                .join(Motorista, Agendamento.motorista_id == Motorista.motorista_id)
                .order_by(Agendamento.agendamento_id.desc()).all()
            )
            
            for agendamento in agendamentos:
                ag =  {
                    "agendamento_id": agendamento.Agendamento.agendamento_id,
                    "nome": agendamento.Paciente.nome,
                    "hygia": agendamento.Paciente.hygia,
                    "tel_1": agendamento.Paciente.tel_1,
                    "data_nascimento": datetime.isoformat(agendamento.Paciente.data_nasc),
                    "data_remocao": datetime.isoformat(agendamento.Agendamento.data_remocao),
                    "saida_prevista": datetime.isoformat(agendamento.Agendamento.saida_prevista),
                    "hospital": agendamento.Hospital.nome,
                    "tipo_encaminhamento": agendamento.Tipo_Encaminhamento.nome, 
                    "tipo_doenca": agendamento.Tipo_Doenca.nome, 
                    "tipo_remocao": agendamento.Tipo_Remocao.nome, 
                    "veiculo_modelo": agendamento.Veiculo.modelo,
                    "veiculo_placa": agendamento.Veiculo.placa,
                    "veiculo_capacidade": agendamento.Veiculo.capacidade,
                    "veiculo_media_consumo": agendamento.Veiculo.media_consumo,
                    "usuario": agendamento.Usuario.primeiro_nome + ' ' + agendamento.Usuario.sobrenome,
                    "motorista": agendamento.Motorista.nome,
                    "responsavel_pac": agendamento.Agendamento.responsavel_pac,
                    "estado_geral_paciente": agendamento.Agendamento.estado_geral_paciente,
                    "observacao": agendamento.Agendamento.observacao,
                    "custo_ifd": agendamento.Agendamento.custo_ifd,
                    "custo_estadia": agendamento.Agendamento.custo_estadia
                }   
                listAgendamentos.append(ag)      
            return listAgendamentos
        except BusinessException as err:
            raise Exception(err)
        except Exception:
            return Exception('Erro desconhecido')

    def add_agendamento(usuario_id, aagendamento):
        try:
            # Verifica se o usuário pode adicionar um novo agendamento ao sistema
            acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Criar_Agendamentos')
            if not acesso_liberado:
                raise BusinessException('Usuário não possui permissão para adicionar novos agendamentos')

            # Verifica se os campos estão preenchidos
            if aagendamento['paciente_id'] == '' or not aagendamento['paciente_id']:
                raise BusinessException('O paciente é obrigatório')

            if aagendamento['tipo_encaminhamento_id'] == '' or not aagendamento['tipo_encaminhamento_id']:
                raise BusinessException('Tipo de encaminhamento do Paciente é obrigatório')

            if aagendamento['tipo_doenca_id'] == '' or not aagendamento['tipo_doenca_id']:
                raise BusinessException('Tipo de doença do Paciente é obrigatória')

            if aagendamento['tipo_remocao_id'] == '' or not aagendamento['tipo_remocao_id']:
                raise BusinessException('Tipo de remoção do Paciente é obrigatório')

            if aagendamento['hospital_id'] == '' or not aagendamento['hospital_id']:
                raise BusinessException('Hospital do Paciente é obrigatório')

            if aagendamento['veiculo_id'] == '' or not aagendamento['veiculo_id']:
                raise BusinessException('O veículo é obrigatório')

            if aagendamento['responsavel_pac'] == '' or not aagendamento['responsavel_pac']:
                raise BusinessException('responsável pelo Paciente é obrigatório')

            if aagendamento['usuario_id'] == '' or not aagendamento['usuario_id']:
                raise BusinessException('Usuário é obrigatório')

            if aagendamento['motorista_id'] == '' or not aagendamento['motorista_id']:
                raise BusinessException('Motorista é obrigatório')

            if aagendamento['data_remocao'] == '' or not aagendamento['data_remocao']:
                raise BusinessException('Data de remoção do Paciente é obrigatória')

            if aagendamento['saida_prevista'] == '' or not aagendamento['saida_prevista']:
                raise BusinessException('Saida prevista do Paciente é obrigatória')

            if aagendamento['observacao'] == '' or not aagendamento['observacao']:
                raise BusinessException('Observção é obrigatória')

            if aagendamento['custo_ifd'] == '' or not aagendamento['custo_ifd']:
                raise BusinessException('Custo IFD é obrigatório')

            if aagendamento['custo_estadia'] == '' or not aagendamento['custo_estadia']:
                raise BusinessException('Custo estadia é obrigatório')

            # Verifica se o paciente informado existe no sistema
            paciente = Paciente.get_paciente_id(usuario_id, aagendamento['paciente_id'], 'Pode_Criar_Paciente')
            if not paciente:
                raise BusinessException('Paciente informado não está cadastrado')

            novoAgendamento = Agendamento(
                paciente_id=aagendamento['paciente_id'],
                tipo_encaminhamento_id=aagendamento['tipo_encaminhamento_id'],
                tipo_doenca_id=aagendamento['tipo_doenca_id'],
                tipo_remocao_id=aagendamento['tipo_remocao_id'],
                hospital_id=aagendamento['hospital_id'],
                veiculo_id=aagendamento['veiculo_id'],
                responsavel_pac=aagendamento['responsavel_pac'].upper().strip(),
                estado_geral_paciente=aagendamento['estado_geral_paciente'].upper().strip(),
                usuario_id=aagendamento['usuario_id'],
                motorista_id=aagendamento['motorista_id'],
                observacao = aagendamento['observacao'].upper().strip(),
                data_remocao = aagendamento['data_remocao'].strip(),
                saida_prevista=aagendamento['saida_prevista'].strip(),
                custo_ifd = aagendamento['custo_ifd'],
                custo_estadia=aagendamento['custo_estadia']
            )

            # Adiciona um novo Paciente
            session.add(novoAgendamento)
            session.commit()
            return novoAgendamento

        except BusinessException as err:
            raise Exception(err)
        except Exception as e:
            return Exception('Erro desconhecido')     