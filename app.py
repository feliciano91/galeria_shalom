from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os


app = Flask(__name__)
app.secret_key = "sua_chave_secreta"

# ===== BANCO POSTGRES (Render) =====
database_url = os.getenv("DATABASE_URL")

# Correção obrigatória (Render às vezes usa postgres://)
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('home-page.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')  # Renderiza o formulário de login

@app.route('/login', methods=['POST'])
def logar():
    username = request.form['username']
    password = request.form['password']
    
    # Exemplo de validação simples
    if username == 'feliciano' and password == '123456':
        return render_template('agendado.html')  # Redireciona para a página agendada
    
    elif username == 'amanda' and password == '123456':
        return render_template('agendadopodologia.html')  # Redireciona para a página agendada
    
    elif username == 'silveria' and password == '123456':
        return render_template('confirmacao.html')  # Redireciona para a página agendada
    else:
        return render_template('login.html')

@app.route('/profissionalpodologia')
def profissionalpodologia():
    return render_template('profissionalpodologia.html')

@app.route('/podologia')
def podologia():
    return render_template('podologia.html')

@app.route('/podologa')
def podologa():
    return render_template('podologa.html')

@app.route('/esmalteria')
def esmalteria():
    return render_template('esmalteria.html')
@app.route('/manicure')
def manicure():
    return render_template('manicure.html')

@app.route('/confirmacao')
def confirmacao():
    return render_template('confirmacao.html')

@app.route('/escolhernovohorario')
def escolhernovohorario():
    return render_template('escolhernovohorario.html')

#===============================  MANICURE  ===============================================

@app.route('/m1agendamento')
def m1agendamento():
    return render_template('agenda1manicure.html')

@app.route('/m2agendamento')
def m2agendamento():
    return render_template('agenda2manicure.html')

@app.route('/m3agendamento')
def m3agendamento():
    return render_template('agenda3manicure.html')

@app.route('/m4agendamento')
def m4agendamento():
    return render_template('agenda4manicure.html')

@app.route('/m5agendamento')
def m5agendamento():
    return render_template('agenda5manicure.html')


#========================== AGENDAMENTO PARA MANICURE====================================================
@app.route('/agenda1manicure', methods=['POST'])
def agenda1manicure():
    # Pegando os dados do formulário
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # Inserir no banco de dados
    cursor = mysql.connection.cursor()
    query = "INSERT INTO agendamentomanicure (nome, contato, data, horario, pagamento, servico) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (nome, contato, data, horario, pagamento, servico))
    mysql.connection.commit()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    # Processando os dados e retornando a confirmação
    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda2manicure', methods=['POST'])
def agenda2manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # Criação de uma lista com os 2 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentomanicure WHERE data = %s AND horario IN (%s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return render_template('escolhernovohorario.html')

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentomanicure (nome, contato, data, horario, pagamento, servico) VALUES (%s, %s, %s, %s, %s, %s)"

        cursor.execute(query, (nome, contato, data, h, pagamento, servico))
    mysql.connection.commit()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda3manicure', methods=['POST'])
def agenda3manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # Criação de uma lista com os 3 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:  
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentomanicure WHERE data = %s AND horario IN (%s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return render_template('escolhernovohorario.html')

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentomanicure (nome, contato, data, horario, pagamento, servico) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento, servico))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horarios=horarios, pagamento=pagamento)


@app.route('/agenda4manicure', methods=['POST'])
def agenda4manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # Criação de uma lista com os 4 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+90min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentomanicure WHERE data = %s AND horario IN (%s, %s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2], horarios[3]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return render_template('escolhernovohorario.html')

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentomanicure (nome, contato, data, horario, pagamento, servico) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento, servico))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horarios=horarios, pagamento=pagamento)


@app.route('/agenda5manicure', methods=['POST'])
def agenda5manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # Criação de uma lista com os 4 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+90min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+120min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+150min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+180min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+210min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+240min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+270min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")


    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentomanicure WHERE data = %s AND horario IN (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2], horarios[3],horarios[4], horarios[5], horarios[6], horarios[7], horarios[8], horarios[9]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return render_template('escolhernovohorario.html')

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentomanicure (nome, contato, data, horario, pagamento, servico) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento, servico))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horarios=horarios, pagamento=pagamento)













#===============================  PODOLOGIA  ===============================================
@app.route('/p1agendamento')
def p1agendamento():
    return render_template('agenda1podologia.html')

@app.route('/p2agendamento')
def p2agendamento():
    return render_template('agenda2podologia.html')

@app.route('/p3agendamento')
def p3agendamento():
    return render_template('agenda3podologia.html')

@app.route('/p4agendamento')
def p4agendamento():
    return render_template('agenda4podologia.html')

@app.route('/p5agendamento')
def p5agendamento():
    return render_template('agenda5podologia.html')


#============================ AGENDAMENTO PARA PODOLOGIA ==================================================
@app.route('/agenda1podologia', methods=['POST'])
def agenda1podologia():
    # Pegando os dados do formulário
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']


    # Inserir no banco de dados
    cursor = mysql.connection.cursor()
    query = "INSERT INTO agendamentopodologia (nome, contato, data, horario, pagamento, servico) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (nome, contato, data, horario, pagamento, servico))
    mysql.connection.commit()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    # Processando os dados e retornando a confirmação
    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda2podologia', methods=['POST'])
def agenda2podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # Criação de uma lista com os 2 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentopodologia WHERE data = %s AND horario IN (%s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return render_template('escolhernovohorario.html')

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentopodologia (nome, contato, data, horario, pagamento, servico) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento, servico))
    mysql.connection.commit()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda3podologia', methods=['POST'])
def agenda3podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # Criação de uma lista com os 3 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:  
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentopodologia WHERE data = %s AND horario IN (%s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return render_template('escolhernovohorario.html')

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentopodologia (nome, contato, data, horario, pagamento, servico) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento, servico))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda4podologia', methods=['POST'])
def agenda4podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # Criação de uma lista com os 4 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+90min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentopodologia WHERE data = %s AND horario IN (%s, %s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2], horarios[3]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return render_template('escolhernovohorario.html')

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentopodologia (nome, contato, data, horario, pagamento, servico) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento, servico))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda5podologia', methods=['POST'])
def agenda5podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # Criação de uma lista com os 4 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+90min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+120min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+150min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+180min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+210min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+240min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+270min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")


    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentopodologia WHERE data = %s AND horario IN (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2], horarios[3],horarios[4], horarios[5], horarios[6], horarios[7], horarios[8], horarios[9]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return render_template('escolhernovohorario.html')

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentopodologia (nome, contato, data, horario, pagamento, servico) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento, servico))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)



#==========================================================================================================================
#==========================================================================================================================
@app.route('/agendado')
def agendado():
    return render_template('agendado.html')

@app.route('/get_horarios/<data>')
def get_horarios(data):
    # Conectar ao banco de dados
    cursor = mysql.connection.cursor()

    # Consulta agora traz os dados desejados
    query = """
        SELECT nome, contato, horario, pagamento, servico
        FROM agendamentomanicure
        WHERE data = %s
    """
    cursor.execute(query, (data,))
    agendamentos = cursor.fetchall()

    lista_agendamentos = []
    
    for agendamento in agendamentos:
        nome = agendamento[0]
        contato = agendamento[1]
        horario = agendamento[2]
        pagamento = agendamento[3]
        servico = agendamento[4]

        # Formata o horário
        if isinstance(horario, timedelta):
            horas = horario.seconds // 3600
            minutos = (horario.seconds % 3600) // 60
            horario_formatado = f"{horas:02}:{minutos:02}"
        else:
            horario_formatado = horario.strftime('%H:%M')

        # Adiciona ao resultado final
        lista_agendamentos.append({
            "nome": nome,
            "contato": contato,
            "horario": horario_formatado,
            "pagamento": pagamento,
            "servico": servico
        })

    cursor.close()  # Fecha o cursor

    return jsonify(lista_agendamentos)  # Retorna todos os dados em JSON

#---------------------------------------------------------------------------------------------------------------
@app.route('/agendadopodologia')
def agendadopodologia():
    return render_template('agendadopodologia.html')

@app.route('/get_horariop/<data>')
def get_horariop(data):
    # Conectar ao banco de dados
    cursor = mysql.connection.cursor()

    # Consulta agora traz os dados desejados
    query = """
        SELECT nome, contato, horario, pagamento, servico
        FROM agendamentopodologia
        WHERE data = %s
    """
    cursor.execute(query, (data,))

    agendamentos = cursor.fetchall()

    lista_agendamentos = []
    for agendamento in agendamentos:
        nome = agendamento[0]
        contato = agendamento[1]
        horario = agendamento[2]
        pagamento = agendamento[3]
        servico = agendamento[4]

        # Formata o horário
        if isinstance(horario, timedelta):
            horas = horario.seconds // 3600
            minutos = (horario.seconds % 3600) // 60
            horario_formatado = f"{horas:02}:{minutos:02}"
        else:
            horario_formatado = horario.strftime('%H:%M')

        # Adiciona ao resultado final
        lista_agendamentos.append({
            "nome": nome,
            "contato": contato,
            "horario": horario_formatado,
            "pagamento": pagamento,
            "servico": servico
        })

    cursor.close()  # Fecha o cursor

    return jsonify(lista_agendamentos)  # Retorna todos os dados em JSON


#--------------------------------------- CANCELAR AGENDAMENTO---------------------------------------------------------------------
@app.route('/confirma_cancelamento')
def confirma_cancelamento():
    return render_template('confirmacancelamento.html')


@app.route('/cancelar_agendamento', methods=['POST'])
def cancelar_agendamento():
    data = request.form['data']
    contato = request.form['contato']

    cursor = mysql.connection.cursor()
    query = """
        DELETE FROM agendamentopodologia
        WHERE data = %s AND contato = %s
    """
    cursor.execute(query, (data, contato))
    mysql.connection.commit()
    cursor.close()

    flash("Agendamento cancelado com sucesso!", "success")
    return redirect(url_for('confirma_cancelamento'))



#==========================================================================================================================
#==========================================================================================================================


if __name__ == '__main__':
    app.run(debug=True)



with app.app_context():
    db.create_all()
