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

class AgendamentoManicure(db.Model):
    __tablename__ = 'agendamentomanicure'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    pagamento = db.Column(db.String(50))
    servico = db.Column(db.String(100))


class AgendamentoPodologia(db.Model):
    __tablename__ = 'agendamentopodologia'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    pagamento = db.Column(db.String(50))
    servico = db.Column(db.String(100))


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
    novo = AgendamentoManicure(
        nome=nome,
        contato=contato,
        data=datetime.strptime(data, '%Y-%m-%d'),
        horario=horario,
        pagamento=pagamento,
        servico=servico
    )
    
    db.session.add(novo)
    db.session.commit()

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

    # Converter data para DATE
    data_obj = datetime.strptime(data, '%Y-%m-%d').date()

    # Criar os 2 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    horarios.append(f"{hora:02d}:{minuto:02d}")

    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # 🔎 VERIFICAR SE ALGUM DOS HORÁRIOS JÁ EXISTE
    existe = AgendamentoManicure.query.filter(
        AgendamentoManicure.data == data_obj,
        AgendamentoManicure.horario.in_(horarios)
    ).first()

    if existe:
        return render_template('escolhernovohorario.html')

    # 💾 INSERIR OS HORÁRIOS
    for h in horarios:
        novo = AgendamentoManicure(
            nome=nome,
            contato=contato,
            data=data_obj,
            horario=h,
            pagamento=pagamento,
            servico=servico
        )
        db.session.add(novo)

    db.session.commit()

    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template(
        'confirmacao.html',
        data=data_formatada,
        horario=horario,
        pagamento=pagamento
    )


@app.route('/agenda3manicure', methods=['POST'])
def agenda3manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    data_obj = datetime.strptime(data, '%Y-%m-%d').date()

    # Criar os 3 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    for _ in range(3):
        horarios.append(f"{hora:02d}:{minuto:02d}")
        minuto += 30
        if minuto >= 60:
            minuto -= 60
            hora += 1

    # 🔎 Verificar se algum horário já existe
    existe = AgendamentoManicure.query.filter(
        AgendamentoManicure.data == data_obj,
        AgendamentoManicure.horario.in_(horarios)
    ).first()

    if existe:
        return render_template('escolhernovohorario.html')

    # 💾 Inserir os horários
    for h in horarios:
        novo = AgendamentoManicure(
            nome=nome,
            contato=contato,
            data=data_obj,
            horario=h,
            pagamento=pagamento,
            servico=servico
        )
        db.session.add(novo)

    db.session.commit()

    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template(
        'confirmacao.html',
        data=data_formatada,
        horarios=horarios,
        pagamento=pagamento
    )


@app.route('/agenda4manicure', methods=['POST'])
def agenda4manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    data_obj = datetime.strptime(data, '%Y-%m-%d').date()

    # Criar os 4 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    for _ in range(4):
        horarios.append(f"{hora:02d}:{minuto:02d}")
        minuto += 30
        if minuto >= 60:
            minuto -= 60
            hora += 1

    # 🔎 Verificar se algum horário já existe
    existe = AgendamentoManicure.query.filter(
        AgendamentoManicure.data == data_obj,
        AgendamentoManicure.horario.in_(horarios)
    ).first()

    if existe:
        return render_template('escolhernovohorario.html')

    # 💾 Inserir os horários
    for h in horarios:
        novo = AgendamentoManicure(
            nome=nome,
            contato=contato,
            data=data_obj,
            horario=h,
            pagamento=pagamento,
            servico=servico
        )
        db.session.add(novo)

    db.session.commit()

    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template(
        'confirmacao.html',
        data=data_formatada,
        horarios=horarios,
        pagamento=pagamento
    )


@app.route('/agenda5manicure', methods=['POST'])
def agenda5manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # 🔹 Gerar 10 horários (5 horas = 10 blocos de 30min)
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    for _ in range(10):
        horarios.append(f"{hora:02d}:{minuto:02d}")
        minuto += 30
        if minuto >= 60:
            minuto -= 60
            hora += 1

    # 🔍 Verificar conflito
    conflito = db.session.query(AgendamentoManicure).filter(
        AgendamentoManicure.data == data,
        AgendamentoManicure.horario.in_(horarios)
    ).count()

    if conflito > 0:
        return render_template('escolhernovohorario.html')

    # 💾 Inserir no banco
    for h in horarios:
        agendamento = AgendamentoManicure(
            nome=nome,
            contato=contato,
            data=data,
            horario=h,
            pagamento=pagamento,
            servico=servico
        )
        db.session.add(agendamento)

    db.session.commit()

    data_formatada = data.strftime('%d-%m-%Y')
    return render_template(
        'confirmacao.html',
        data=data_formatada,
        horarios=horarios,
        pagamento=pagamento
    )









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
    nome = request.form['nome']
    contato = request.form['contato']
    data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    agendamento = AgendamentoPodologia(
        nome=nome,
        contato=contato,
        data=data,
        horario=horario,
        pagamento=pagamento,
        servico=servico
    )

    db.session.add(agendamento)
    db.session.commit()

    data_formatada = data.strftime('%d-%m-%Y')
    return render_template(
        'confirmacao.html',
        data=data_formatada,
        horario=horario,
        pagamento=pagamento
    )


@app.route('/agenda2podologia', methods=['POST'])
def agenda2podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # 🔹 Gerar os 2 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    for _ in range(2):
        horarios.append(f"{hora:02d}:{minuto:02d}")
        minuto += 30
        if minuto >= 60:
            minuto -= 60
            hora += 1

    # 🔍 Verificar conflito
    conflito = db.session.query(AgendamentoPodologia).filter(
        AgendamentoPodologia.data == data,
        AgendamentoPodologia.horario.in_(horarios)
    ).count()

    if conflito > 0:
        return render_template('escolhernovohorario.html')

    # 💾 Inserir horários
    for h in horarios:
        agendamento = AgendamentoPodologia(
            nome=nome,
            contato=contato,
            data=data,
            horario=h,
            pagamento=pagamento,
            servico=servico
        )
        db.session.add(agendamento)

    db.session.commit()

    data_formatada = data.strftime('%d-%m-%Y')
    return render_template(
        'confirmacao.html',
        data=data_formatada,
        horario=horario,
        pagamento=pagamento
    )


@app.route('/agenda3podologia', methods=['POST'])
def agenda3podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # 🔹 Gerar 3 horários (30min)
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    for _ in range(3):
        horarios.append(f"{hora:02d}:{minuto:02d}")
        minuto += 30
        if minuto >= 60:
            minuto -= 60
            hora += 1

    # 🔍 Verificar conflito
    conflito = db.session.query(AgendamentoPodologia).filter(
        AgendamentoPodologia.data == data,
        AgendamentoPodologia.horario.in_(horarios)
    ).count()

    if conflito > 0:
        return render_template('escolhernovohorario.html')

    # 💾 Inserir horários
    for h in horarios:
        agendamento = AgendamentoPodologia(
            nome=nome,
            contato=contato,
            data=data,
            horario=h,
            pagamento=pagamento,
            servico=servico
        )
        db.session.add(agendamento)

    db.session.commit()

    data_formatada = data.strftime('%d-%m-%Y')
    return render_template(
        'confirmacao.html',
        data=data_formatada,
        horario=horario,
        pagamento=pagamento
    )


@app.route('/agenda4podologia', methods=['POST'])
def agenda4podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # 🔹 Gerar 4 horários (30min)
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    for _ in range(4):
        horarios.append(f"{hora:02d}:{minuto:02d}")
        minuto += 30
        if minuto >= 60:
            minuto -= 60
            hora += 1

    # 🔍 Verificar conflito
    conflito = db.session.query(AgendamentoPodologia).filter(
        AgendamentoPodologia.data == data,
        AgendamentoPodologia.horario.in_(horarios)
    ).count()

    if conflito > 0:
        return render_template('escolhernovohorario.html')

    # 💾 Inserir horários
    for h in horarios:
        agendamento = AgendamentoPodologia(
            nome=nome,
            contato=contato,
            data=data,
            horario=h,
            pagamento=pagamento,
            servico=servico
        )
        db.session.add(agendamento)

    db.session.commit()

    data_formatada = data.strftime('%d-%m-%Y')
    return render_template(
        'confirmacao.html',
        data=data_formatada,
        horario=horario,
        pagamento=pagamento
    )


@app.route('/agenda5podologia', methods=['POST'])
def agenda5podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    # 🔹 Gerar 10 horários (5 blocos de 30min)
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    for _ in range(10):
        horarios.append(f"{hora:02d}:{minuto:02d}")
        minuto += 30
        if minuto >= 60:
            minuto -= 60
            hora += 1

    # 🔍 Verificar conflito de horário
    conflito = db.session.query(AgendamentoPodologia).filter(
        AgendamentoPodologia.data == data,
        AgendamentoPodologia.horario.in_(horarios)
    ).count()

    if conflito > 0:
        return render_template('escolhernovohorario.html')

    # 💾 Inserir horários
    for h in horarios:
        agendamento = AgendamentoPodologia(
            nome=nome,
            contato=contato,
            data=data,
            horario=h,
            pagamento=pagamento,
            servico=servico
        )
        db.session.add(agendamento)

    db.session.commit()

    data_formatada = data.strftime('%d-%m-%Y')
    return render_template(
        'confirmacao.html',
        data=data_formatada,
        horario=horario,
        pagamento=pagamento
    )



#==========================================================================================================================
#==========================================================================================================================
@app.route('/agendado')
def agendado():
    return render_template('agendado.html')

@app.route('/get_horarios/<data>')
def get_horarios(data):
    data_obj = datetime.strptime(data, '%Y-%m-%d').date()

    agendamentos = AgendamentoManicure.query.filter_by(data=data_obj).all()

    lista = []
    for a in agendamentos:
        lista.append({
            "nome": a.nome,
            "contato": a.contato,
            "horario": a.horario,
            "pagamento": a.pagamento,
            "servico": a.servico
        })

    return jsonify(lista)

#---------------------------------------------------------------------------------------------------------------
@app.route('/agendadopodologia')
def agendadopodologia():
    return render_template('agendadopodologia.html')

@app.route('/get_horariop/<data>')
def get_horariop(data):
    data_obj = datetime.strptime(data, '%Y-%m-%d').date()

    agendamentos = AgendamentoPodologia.query.filter_by(data=data_obj).all()

    lista = []
    for a in agendamentos:
        lista.append({
            "nome": a.nome,
            "contato": a.contato,
            "horario": a.horario,
            "pagamento": a.pagamento,
            "servico": a.servico
        })

    return jsonify(lista)


#--------------------------------------- CANCELAR AGENDAMENTO---------------------------------------------------------------------
@app.route('/confirma_cancelamento')
def confirma_cancelamento():
    return render_template('confirmacancelamento.html')


@app.route('/cancelar_agendamento', methods=['POST'])
def cancelar_agendamento():
    data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    contato = request.form['contato']

    AgendamentoPodologia.query.filter_by(
        data=data,
        contato=contato
    ).delete()

    db.session.commit()

    flash("Agendamento cancelado com sucesso!", "success")
    return redirect(url_for('confirma_cancelamento'))
#==========================================================================================================================
#==========================================================================================================================

if __name__ == '__main__':
    if os.getenv("FLASK_ENV") == "development":
        with app.app_context():
            db.create_all()

    app.run(debug=True)
