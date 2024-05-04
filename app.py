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
from reportsRoute import reportsRoute

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
app.register_blueprint(reportsRoute)

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

#página inicial
@app.route("/")
def index():
    return None 