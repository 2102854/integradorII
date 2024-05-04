"""
Módulo De Relatórios
"""
import os
import locale
from flask import Blueprint, request, jsonify, make_response, send_file,  send_from_directory
from dict_helper import dict_helper_list, dict_helper_obj
#from pyreportjasper import PyReportJasper
from seguranca.autenticacao import Auth
from seguranca.business_exception import BusinessException
from seguranca.permissoes import Permissao

os.environ["JAVA_HOME"] ="C:\Progra~1\Java\jdk-21"
locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports')
reportsRoute = Blueprint('reportsRoute', __name__)

#Exibe o relatório R1
@reportsRoute.route("/r1")
#@Auth.token_required
#def generate_r1(usuario_id: int):
def generate_r1():
    try:  
        """
        # Verifica se o usuário pode gerar o relatório
        #acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Gerar_Relatórios')
        #if not acesso_liberado:
        #    raise BusinessException('Usuário não possui permissão para gerar relatórios')
                          
        input_file = os.path.join(REPORTS_DIR, 'Invoice.jrxml')
        output_file = os.path.join(REPORTS_DIR, 'Invoice')
        pyreportjasper = PyReportJasper()
        
        conn = {
            'dataFile': 'C:/temp/venv/reports/TFD360.jrdax',
            'database': 'integrador',
            'dbType': 'generic',
            'driver': 'org.sqlite.JDBC',            
            'jdbc_url': 'jdbc:sqlite:c:/temp/venv/integrador.db',
            'jdbc_dir': 'C:/temp/venv/reports/sqlitejdbc.jar'
        } 
           
        pyreportjasper.config(
            input_file,
            output_file,
            #db_connection=conn,
            output_formats=["pdf"]
        )
        
        pyreportjasper.process_report()

        if os.path.isfile(output_file):
            print('Report generated successfully!')  
        """      
        return send_from_directory('./reports', 'Invoice.pdf')        
        
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404
    
    
@reportsRoute.route("/r2")
#@Auth.token_required
#def registered_appointments(usuario_id: int):
def registered_appointments():
    try:  
        """
        # Verifica se o usuário pode gerar o relatório
        #acesso_liberado = Permissao.valida_permissao_usuario(usuario_id, 'Pode_Gerar_Relatórios')
        #if not acesso_liberado:
        #    raise BusinessException('Usuário não possui permissão para gerar relatórios')
                          
        input_file = os.path.join(REPORTS_DIR, 'agendamentos.jrxml')
        output_file = os.path.join(REPORTS_DIR, 'agendamentos')
        pyreportjasper = PyReportJasper()
        '''
        conn = {
            'driver': 'generic',
            'dbType': 'generic',
            'jdbc_url': 'jdbc:sqlite:c:/temp/venv/integrador.db',
            'database': 'integrador.db',
            'jdbc_dir': 'C:/temp/venv/reports/sqlitejdbc.jar'
        }    
        '''   
        pyreportjasper.config(
            input_file,
            output_file,
            #db_connection=conn,
            output_formats=["pdf"],
            parameters={'dt_inicio':'01/01/2023','dt_fim':'30/05/2025' }
        )
        
        pyreportjasper.process_report()

        if os.path.isfile(output_file):
            print('Report generated successfully!')  
        """      
        return send_from_directory('./reports', 'agendamentos.pdf')        
        
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404    
"""    
@reportsRoute.route("/r3")
#@Auth.token_required
#def generate_r1(usuario_id: int):
def generate_r3():
    try:  
        data_file = os.path.join(REPORTS_DIR, 'contacts.json')                          
        input_file = os.path.join(REPORTS_DIR, 'jsonql.jrxml')
        output_file = os.path.join(REPORTS_DIR, 'jsonql')        
        conn = {
            'driver': 'jsonql',
            'data_file': data_file,
            'json_query': 'contacts.person'
        }  
        pyreportjasper = PyReportJasper() 
        pyreportjasper.config(
            input_file,
            output_file,
            output_formats=["pdf"],
            db_connection=conn
        )
       
        pyreportjasper.process_report()

        if os.path.isfile(output_file):
            print('Report generated successfully!')  
              
        return send_from_directory('./reports', 'jsonql.pdf')        
        
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 404    
"""