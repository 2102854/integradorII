from sqlalchemy import Column
from sqlalchemy import create_engine, select, and_
from sqlalchemy.dialects.sqlite import (INTEGER, VARCHAR, FLOAT)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from config import parameters
from veiculo import Veiculo
from paciente import Paciente
from hospital import Hospital
from agendamento import Agendamento
from seguranca.business_exception import BusinessException
from seguranca.pemissoes import Permissao

import json
from datetime import datetime, timedelta 
from calendar import monthrange


class Dashboard():
    
    # Cria um retorno de dicionário de uma lista de objetos para retorno json
    def dict_helper_list(objlist):
        result = [item.obj_to_dict() for item in objlist]
        return result

    # Cria um retorno de dicionário de um objeto para retorno json
    def dict_helper_obj(obj):
        result = json.JSONDecoder().decode(json.dumps(obj.obj_to_dict(), indent = 2))
        return result

    
    # Retorna os dados principais para o Dashboard
    def get_dados(usuario_id):
        #Retorna os números totais para exibição
        agendamentos_ano = Agendamento.get_agendamentos_ano(usuario_id)
        cadastros_ano = Paciente.get_cadastros_ano(usuario_id)        
        total_pacientes = Paciente.get_total_pacientes(usuario_id)
        pacientes_cadastrados_mes_corrente = Paciente.get_cadastrados_mes_corrente(usuario_id)
        total_hospitais = Hospital.get_total_hospitais(usuario_id)
        total_agendamentos = Agendamento.get_total_agendamento(usuario_id)
        ultimos_agendamentos = Agendamento.get_last_agendamentos(usuario_id)
        total_veiculos = Veiculo.get_total_veiculos(usuario_id)

        result = {
            'total_pacientes': int(total_pacientes),
            'total_hospitais': int(total_hospitais),
            'total_agendamentos':int(total_agendamentos),
            'total_veiculos': int(total_veiculos),
            'pacientes_cadastrados_mes_corrente': int(pacientes_cadastrados_mes_corrente),
            'agendamentos_ano': agendamentos_ano,
            'cadastros_ano': cadastros_ano,
            'ultimos_agendamentos': ultimos_agendamentos,
        }

        return result