# Projeto integrador 2
# Grupo 5

# OBSERVAÇÕES GERAIS
# A app.py será a página principal de rotas e não deverá tratar das regras de negócios. Apenas validar autenticação e parametros recebidos
# Cada tabela do bd deverá ter sua própria Classe (arquivo.py)
# Verificar a necessidade de criar classes separadas nos casos de herança (especialização ou generalização)


# Referencias
import locale
#from datetime import date, datetime, time
#from babel.dates import format_date, format_datetime, format_time
#https://babel.pocoo.org/en/latest/dates.html
from models import Estado, Cidade, Veiculo, Hospital, Paciente, Motorista, Usuario, Tipo_Doenca, Tipo_Encaminhamento, Tipo_Remocao, Agendamento
from pais import Pais
from usuario import Usuario
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, make_response
from sqlalchemy import create_engine, func
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op

from seguranca.business_exception import BusinessException
from seguranca.autenticacao import Auth
from seguranca.token import Token


# Configuração da aplicação
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True


# Cria o dicionário da Classe para retorno json
def dict_helper(objlist):
    result = [item.obj_to_dict() for item in objlist]
    return result

locale.setlocale( locale.LC_ALL,'pt_BR.UTF-8' )

# Mapeia o banco de dados -- DEVE SER RETIRADO DAQUI
engine = create_engine("sqlite:///integrador.db", echo=True)
session = Session(engine)

#Cria um filtro para o Jinja2 para formatar a data
@app.template_filter()
def format_datetime(value):
    v = str(value).split('T')
    v_d = str(v[0]).split('-')
    v_date = v_d[2] + "/" + v_d[1] + "/" + v_d[0]
    v_time = v[1]
    return v_date + ' ' + v_time

@app.template_filter()
def format_real(value):
    v = str(value)
    v = v.replace(".", ",")
    return v

#página inicial
@app.route("/")
def index():

    #Conta o número de Hospitais cadastrados
    num_hospitais = session.query(func.count(Hospital.hospital_id)).scalar()
    num_pacientes = session.query(func.count(Paciente.paciente_id)).scalar()
    num_agendamentos = session.query(func.count(Agendamento.agendamento_id)).scalar()

    #Carrega a lista de hospitais 
    sql = select(Hospital).order_by(Hospital.hospital_id.desc())
    hospitais = session.scalars(sql)

    lt_hospitais = []
    num_hos = 0

    for hospital in hospitais:
        num_hos = num_hos + 1
        
        lt_hospitais.append(hospital.nome)
        if num_hos > 3:
            break

    if num_hos < 4:
        for x in range(4 - num_hos):
            lt_hospitais.append("..")    

    #Carrega a lista de pacientes 
    sql = select(Paciente).order_by(Paciente.paciente_id.desc())
    pacientes = session.scalars(sql)   
    
    lt_pacientes = []
    num_pac = 0
    
    for paciente in pacientes:
        num_pac = num_pac + 1
        
        lt_pacientes.append(paciente.nome)
        if num_pac > 3:
            break

    if num_pac < 4:
        for x in range(4 - num_pac):
            lt_pacientes.append("..")

    #Carrega a lista de agendamentos 
    agendamentos = session.query(Agendamento, Paciente ).order_by(Agendamento.agendamento_id.desc()).join(Paciente, Agendamento.paciente_id == Paciente.paciente_id).all() 

    lt_agendamentos = []
    num_age = 0

    for agendamento in agendamentos:
        num_age = num_age + 1
        
        lt_agendamentos.append(agendamento.Paciente.nome)
        if num_age > 3:
            break

    if num_age < 4:
        for x in range(4 - num_age):
            lt_agendamentos.append("..")               

    return render_template('index.html', hospitais=num_hospitais, pacientes=num_pacientes, agendamentos=num_agendamentos,
                          lt_hospitais=lt_hospitais, lt_pacientes=lt_pacientes, lt_agendamentos=lt_agendamentos)

# Realiza a autenticação do usuário
@app.route('/login', methods=['POST'])
def login():    
    # Verifica se existe um token na chamada
    token = None
    if 'x-access-token' in request.headers:
        try: 
            token = request.headers['x-access-token'] 
            Token.valida_token(token)
            return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
        except Exception as err:
            return make_response('Não foi possível verificar', 401, {'WWW-Authenticate' : 'Basic realm =Token inválido'})  
    else:
        try:
            # Executa a validação dos dados informados
            token = Auth.login(request.form['email'], request.form['senha'])
            return make_response(jsonify({'token' : token}), 201)
        except Exception as err:
            return make_response('Dados incorretos', 401, {'WWW-Authenticate' : 'Basic realm =Dados incorretos'}) 
        
# Recupera todos os Países Cadastrados no Banco de Dados
@app.route('/paises', methods=['GET'])
@Auth.token_required
def get_paises(usuario_id):
    try:
        paises = Pais.get_paises(usuario_id)
        p = dict_helper(paises) 
        return jsonify(paises = p)            
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401

# Recupera todos os Usuários Cadastrados no Banco de Dados
@app.route('/usuarios', methods=['GET'])
@Auth.token_required
def get_usuarios(usuario_id):
    try:
        usuarios = Usuario.get_usuarios(usuario_id)
        u = dict_helper(usuarios) 
        return jsonify(usuarios = u)            
    except Exception as err:
        response = jsonify({'message err': f'{err}'})
        return response, 401
    

"""
return make_response( 
    'Could not verify', 
    401, 
    {'WWW-Authenticate' : 'Basic realm ="Login required !!"'} 
) 


 return make_response(jsonify({'token' : token.decode('UTF-8')}), 201) 
""" 

    #return render_template('paises.html',paises=paises)

    #nome = request.args.get('nome', default = '', type = str)
    #if nome == '':    
    #    paises = session.query(Pais).all()        
    #else:
    #    paises = session.query(Pais).filter(ilike_op(Pais.nome,f'%{nome}%')).all()
    #return render_template('paises.html',paises=paises)

#Abre a página de cadastro de países
#@app.route('/paises/novo/', methods=('GET', 'POST'))
#def pais_add():
#    if request.method == 'POST':

#        novoPais = Pais(request.form['nome'], request.form['sigla'])
#        session.add(novoPais)        
#        session.commit()        
#        return redirect(url_for('paises'))    
    
#    else:
#        return render_template('form_cad_pais.html')
    
#Abre a página de edição de países    
#@app.route('/paises/editar/<pais_id>', methods=('GET', 'POST'))
#def pais_edit(pais_id):
#    
#    if request.method == 'POST':
        # Executa a alteração do país
#        sql = select(Pais).where(Pais.pais_id == pais_id)
#        result = session.scalars(sql).one()
#        result.nome = request.form['nome']
#        result.sigla = request.form['sigla']        
#       session.commit() 

        # Volta para a página de países
#        return redirect(url_for('paises'))
#    else:

        # Pesquisa pelo Id do pais
#        sql = select(Pais).where(Pais.pais_id == pais_id)
#        result = session.scalars(sql).one()
#        return render_template('form_edt_pais.html',pais_id=pais_id, nome=result.nome, sigla=result.sigla )
    
#Abre a página de estados

@app.route("/estados")
def estados():    
    nome = request.args.get('nome', default = '', type = str)
    if nome == '':    
        sql = session.query(Estado, Pais).join(Estado, Estado.pais_id == Pais.pais_id).all()        
    else:
        sql = session.query(Estado, Pais).filter(ilike_op(Estado.nome,f'%{nome}%')).join(Estado, Estado.pais_id == Pais.pais_id).all()
    return render_template('estados.html', results=sql)

"""
#Abre a página de cidades
@app.route("/cidades")
def cidades():    
    #sql = session.query(Cidade, Estado).join(Estado, Cidade.estado_id == Estado.estado_id).all()
    nome = request.args.get('nome', default = '', type = str)
    if nome == '':    
        sql = session.query(Cidade, Estado).join(Estado, Cidade.estado_id == Estado.estado_id).all()       
    else:
        sql = session.query(Cidade, Estado).filter(ilike_op(Cidade.nome,f'%{nome}%')).join(Estado, Cidade.estado_id == Estado.estado_id).all()  
    return render_template('cidades.html', results=sql)

#Abre a página de pacientes
@app.route("/pacientes")
def pacientes():
    #http://127.0.0.1:5000/pacientes?nome=rosa
    #nome = request.args.get('nome', default = '', type = str)
    #if nome == '':    
    sql = session.query(Paciente, Cidade).join(Cidade, Paciente.cidade_id == Cidade.cidade_id).all()        
    #else:
    #sql = session.query(Paciente, Cidade).filter(ilike_op(Paciente.nome,f'%{nome}%')).join(Cidade, Paciente.cidade_id == Cidade.cidade_id).all()
    return render_template('pacientes.html', results=sql)

#https://medium.com/@mhd0416/flask-sqlalchemy-object-to-json-84c515d3c11c
# Retorna a lista de pacientes em formato json
@app.route("/pacientes/lst")
def getPacientes():
    sql = session.query(Paciente).all()
    p = dict_helper(sql) 
    return jsonify(pacientes = p)

#Abre a página de cadastro de pacientes
@app.route('/pacientes/novo/', methods=('GET', 'POST'))
def pacientes_add():
    if request.method == 'POST':      
        
        novoPaciente = Paciente (
            request.form['cidade'],
            request.form['hygia'],
            request.form['nome'].upper(), 
            request.form['data_nasc'], 
            request.form['tel_1'], 
            request.form['tel_2'], 
            request.form['logradouro'].upper(), 
            request.form['numero'], 
            request.form['complemento'].upper(), 
            request.form['cep']
        )
        session.add(novoPaciente)        
        session.commit()        
        return redirect(url_for('pacientes'))    
    
    else:
        cidades = session.query(Cidade).all()
        return render_template('form_cad_paciente.html', cidades=cidades)
    
#Abre a página de edição de pacientes
@app.route('/pacientes/editar/<paciente_id>', methods=('GET', 'POST'))
def pacientes_edit(paciente_id):
    if request.method == 'POST':      
        sql = select(Paciente).where(Paciente.paciente_id == paciente_id)
        paciente = session.scalars(sql).one()

        paciente.cidade_id = request.form['cidade']
        paciente.hygia = request.form['hygia']
        paciente.nome = request.form['nome'].upper()
        paciente.data_nasc = request.form['data_nasc'] 
        paciente.tel_1 = request.form['tel_1']
        paciente.tel_2 = request.form['tel_2'] 
        paciente.logradouro = request.form['logradouro'].upper() 
        paciente.numero = request.form['numero']
        paciente.complemento = request.form['complemento'].upper()
        paciente.cep = request.form['cep']     
        session.commit()

        return redirect(url_for('pacientes'))    
    
    else:
        cidades = session.query(Cidade).all()
        sql = select(Paciente).where(Paciente.paciente_id == paciente_id)
        paciente = session.scalars(sql).one()
        return render_template('form_edit_paciente.html', cidades=cidades, paciente = paciente)
 
#Abre a página de pacientes
@app.route("/agendamentos")
def agendamentos():  
    sql = (session.query(Agendamento, Paciente, Hospital, Veiculo, Motorista).order_by(Agendamento.agendamento_id.desc()) 
     .join(Paciente, Agendamento.paciente_id == Paciente.paciente_id) 
     .join(Hospital, Agendamento.hospital_id == Hospital.hospital_id) 
     .join(Veiculo, Agendamento.veiculo_id == Veiculo.veiculo_id) 
     .join(Motorista, Agendamento.motorista_id ==  Motorista.motorista_id).all())

    return render_template('agendamentos.html', results=sql)

#Abre a página de agendamento de pacientes
@app.route('/agendamentos/novo/', methods=('GET', 'POST'))
def agendamentos_add():
    if request.method == 'POST':      
        novoAgendamento = Agendamento (
            request.form['paciente_id'],           
            request.form['encaminhamento'], 
            request.form['doenca'],
            request.form['remocao'],
            request.form['hospital_id'],
            request.form['veiculo'],
            request.form['responsavel_pac'].upper(),
            request.form['usuario_id'],
            request.form['motorista'],
            request.form['estado_geral_paciente'].upper(),  
            request.form['data_remocao'], 
            request.form['saida_prevista'], 
            request.form['observacao'].upper(), 
            request.form['custo_IFD'],
            request.form['custo_estadia']          
        )
        session.add(novoAgendamento)        
        session.commit()        
        return redirect(url_for('agendamentos'))    
    
    else:
        tipo_encaminhamentos = session.query(Tipo_Encaminhamento).order_by(Tipo_Encaminhamento.nome).all()
        tipo_doencas = session.query(Tipo_Doenca).order_by(Tipo_Doenca.nome).all()
        tipo_remocoes = session.query(Tipo_Remocao).order_by(Tipo_Remocao.nome).all()
        veiculos = session.query(Veiculo).order_by(Veiculo.modelo).all()
        motoristas = session.query(Motorista).order_by(Motorista.nome).all()
        usuarios = session.query(Usuario).order_by(Usuario.primeiro_nome).all() 
        pacientes = session.query(Paciente).order_by(Paciente.nome).all() 
        hospitais = session.query(Hospital).order_by(Hospital.nome).all() 
        return render_template('form_cad_agendamento.html', tipo_encaminhamentos=tipo_encaminhamentos, 
                               tipo_doencas=tipo_doencas,tipo_remocoes=tipo_remocoes,veiculos=veiculos, 
                               motoristas=motoristas, usuarios=usuarios, pacientes=pacientes,
                               hospitais = hospitais)

#Abre a página de edição de agendamento
@app.route('/agendamentos/editar/<agendamento_id>', methods=('GET', 'POST'))
def agendamentos_edit(agendamento_id):
    if request.method == 'POST':      
        sql = select(Agendamento).where(Agendamento.agendamento_id == agendamento_id)
        agendamento = session.scalars(sql).one()
        agendamento.paciente_id = request.form['paciente_id']
        agendamento.tipo_encaminhamento_id = request.form['encaminhamento']
        agendamento.tipo_doenca_id = request.form['doenca']
        agendamento.tipo_remocao_id = request.form['remocao']
        agendamento.hospital_id = request.form['hospital_id']
        agendamento.veiculo_id = request.form['veiculo']
        agendamento.responsavel_pac = request.form['responsavel_pac'].upper()
        agendamento.usuario_id = request.form['usuario_id']
        agendamento.motorista_id = request.form['motorista']
        agendamento.estado_geral_paciente = request.form['estado_geral_paciente'].upper()
        agendamento.data_remocao = request.form['data_remocao']
        agendamento.saida_prevista = request.form['saida_prevista']
        agendamento.observacao = request.form['observacao'].upper()
        agendamento.custo_IFD = request.form['custo_IFD']
        agendamento.custo_estadia = request.form['custo_estadia']  
        session.commit()
        return redirect(url_for('agendamentos'))    
    else:
        #Carrega as informações dos combos e seletores
        tipo_encaminhamentos = session.query(Tipo_Encaminhamento).order_by(Tipo_Encaminhamento.nome).all()
        tipo_doencas = session.query(Tipo_Doenca).order_by(Tipo_Doenca.nome).all()
        tipo_remocoes = session.query(Tipo_Remocao).order_by(Tipo_Remocao.nome).all()
        veiculos = session.query(Veiculo).order_by(Veiculo.modelo).all()
        motoristas = session.query(Motorista).order_by(Motorista.nome).all()
        usuarios = session.query(Usuario).order_by(Usuario.primeiro_nome).all() 
        pacientes = session.query(Paciente).order_by(Paciente.nome).all() 
        hospitais = session.query(Hospital).order_by(Hospital.nome).all() 

        sql = select(Agendamento).where(Agendamento.agendamento_id == agendamento_id)
        agendamento = session.scalars(sql).one()
        return render_template('form_edt_agendamento.html', tipo_encaminhamentos=tipo_encaminhamentos, 
                               tipo_doencas=tipo_doencas,tipo_remocoes=tipo_remocoes,veiculos=veiculos, 
                               motoristas=motoristas, usuarios=usuarios, pacientes=pacientes,
                               hospitais = hospitais, agendamento = agendamento )

"""