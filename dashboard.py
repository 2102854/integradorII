from sqlalchemy import Column
from sqlalchemy import create_engine, select, and_
from sqlalchemy.dialects.sqlite import (INTEGER, VARCHAR, FLOAT)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from config import parameters
from estado import Estado
from paciente import Paciente
from hospital import Hospital
from agendamento import Agendamento
from seguranca.business_exception import BusinessException
from seguranca.pemissoes import Permissao

class Dashboard():
    
    # Retorna os dados principais para o Dashboard
    def get_dados(usuario_id):
        
        #Retorna os números totais para exibição
        total_pacientes = Paciente.get_total_pacientes(usuario_id)
        total_hospitais = Hospital.get_total_hospitais(usuario_id)
        total_agendamentos = Agendamento.get_total_agendamento(usuario_id)
        
        result = {
            'total_pacientes': total_pacientes,
            'total_hospitais': total_hospitais,
            'total_agendamentos' :total_agendamentos
        }

        return result