# Projeto integrador 3
# Grupo 5

# OBSERVAÇÕES GERAIS
# A app.py será a página principal de rotas e não deverá tratar das regras de negócios. Apenas registrar as rotas
# Cada tabela do bd deverá ter sua própria Classe (arquivo.py)

import locale

from flask import Flask
from flask import request, jsonify, make_response
from flask_cors import CORS 

from seguranca.authRoute import authRoute
from seguranca.groupsRoute import groupsRoute
from seguranca.permissionsRoute import permissionsRoute
from usersRoute import usersRoute
from dashboardRoute import dashboardRoute
from countriesRoute import countriesRoute
from statesRoute import statesRoute
from citiesRoute import citiesRoute
from hospitalRoute import hospitalRoute
from vehiclesRoute import vehiclesRoute
from patientsRoute import patientsRoute
from driversRoute import driversRoute
from removalTypesRoute import removalTypesRoute
from disease_typesRoute import diseaseTypesRoute
from patient_referralRoute import patient_referralRoute
from schedulingRoute import schedulingRoute


import os
os.environ["JAVA_HOME"] ="C:\Progra~1\Java\jdk-21"
from pyreportjasper import PyReportJasper
from flask import send_file,  send_from_directory

"""
import argparse
import io
import os
import sys
from rlextra.rml2pdf import rml2pdf

"""
"""
Config App
"""
# Configuração da aplicação
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True

# Habilita chamadas cors
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# blueprint register
app.register_blueprint(authRoute)
app.register_blueprint(permissionsRoute)
app.register_blueprint(dashboardRoute)
app.register_blueprint(countriesRoute)
app.register_blueprint(statesRoute)
app.register_blueprint(citiesRoute)
app.register_blueprint(hospitalRoute)
app.register_blueprint(vehiclesRoute)
app.register_blueprint(patientsRoute)
app.register_blueprint(driversRoute)
app.register_blueprint(removalTypesRoute)
app.register_blueprint(usersRoute)
app.register_blueprint(groupsRoute)
app.register_blueprint(diseaseTypesRoute)
app.register_blueprint(patient_referralRoute)
app.register_blueprint(schedulingRoute)

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

#página inicial
@app.route("/")
def index():
    return None

"""
@app.route("/r1")
def r1():
    with open("./rml/test01.rml", "r") as rml:
        rml2pdf.go(rml.read(), "./rml/test01.pdf")
        rml.close()
    return send_from_directory('./rml', 'test01.pdf')
"""
@app.route("/r1")
def r1():
    
    REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports')
    input_file = os.path.join(REPORTS_DIR, 'Invoice.jrxml')
    output_file = os.path.join(REPORTS_DIR, 'Invoice')
    pyreportjasper = PyReportJasper()
    pyreportjasper.config(
        input_file,
        output_file,
        output_formats=["pdf"]
    )
    pyreportjasper.process_report()

    if os.path.isfile(output_file):
        print('Report generated successfully!')    
    return send_from_directory('./reports', 'Invoice.pdf')