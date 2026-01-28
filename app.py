from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
#from flask_mysqldb import MySQL
from datetime import datetime  # Importando o módulo datetime
from datetime import timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import time
import sqlite3
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={
    r"/get_horarios/*": {
        "origins": "https://galeriashalom.com.br"
    }
})


# ----------------------
# Configuração do banco
# ----------------------
DATABASE_URL = (
    "postgresql://galeria_shalom_db_user:"
    "A9vUujpt3sM1D01UNz3x4fJi8QWnejTo@"
    "dpg-d55iorumcj7s73fcj4dg-a.oregon-postgres.render.com:5432/"
    "galeria_shalom_db"
    "?sslmode=require"
)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# ✅ A FUNÇÃO FICA AQUI (FORA DAS ROTAS)
def gerar_horarios():
    horarios = []
    for h in range(8, 18):  # 08:00 até 17:00
        horarios.append(time(h, 0))
    return horarios



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

#@app.route('/m5agendamento')
#def m5agendamento():
#    return render_template('agenda5manicure.html')


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
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO agendamentosmanicure
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    # Processando os dados e retornando a confirmação
    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda2manicure', methods=['POST'])
def agenda2manicure():
    # Pegando os dados do formulário
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        hora_base = datetime.strptime(horario, "%H:%M")
        hora_bloqueada = hora_base + timedelta(minutes=30)

        horario_bloqueado = hora_bloqueada.strftime("%H:%M")

        cursor.execute("""
            INSERT INTO agendamentosmanicure
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        cursor.execute("""
            INSERT INTO agendamentosmanicure
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático"))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    # Processando os dados e retornando a confirmação
    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda3manicure', methods=['POST'])
def agenda3manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 🔹 1. INSERE O AGENDAMENTO PRINCIPAL
        cursor.execute("""
            INSERT INTO agendamentosmanicure
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        # 🔹 2. BLOQUEIA 08:30 E 09:00
        hora_base = datetime.strptime(horario, "%H:%M")

        bloqueios = [
            hora_base + timedelta(minutes=30),
            hora_base + timedelta(minutes=60)
        ]

        for hb in bloqueios:
            horario_bloqueado = hb.strftime("%H:%M")

            cursor.execute("""
            INSERT INTO agendamentosmanicure
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático"))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda4manicure', methods=['POST'])
def agenda4manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 🔹 1. INSERE O AGENDAMENTO PRINCIPAL
        cursor.execute("""
            INSERT INTO agendamentosmanicure
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        # 🔹 2. BLOQUEIA 08:30 E 09:00
        hora_base = datetime.strptime(horario, "%H:%M")

        bloqueios = [
            hora_base + timedelta(minutes=30),
            hora_base + timedelta(minutes=60),
            hora_base + timedelta(minutes=90)
        ]

        for hb in bloqueios:
            horario_bloqueado = hb.strftime("%H:%M")

            cursor.execute("""
            INSERT INTO agendamentosmanicure
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático"))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)



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

#@app.route('/p5agendamento')
#def p5agendamento():
#    return render_template('agenda5podologia.html')


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
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO agendamentospodologa
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    # Processando os dados e retornando a confirmação
    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda2podologia', methods=['POST'])
def agenda2podologia():
    # Pegando os dados do formulário
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        hora_base = datetime.strptime(horario, "%H:%M")
        hora_bloqueada = hora_base + timedelta(minutes=30)

        horario_bloqueado = hora_bloqueada.strftime("%H:%M")

        cursor.execute("""
            INSERT INTO agendamentospodologa
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        cursor.execute("""
            INSERT INTO agendamentospodologa
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático"))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    # Processando os dados e retornando a confirmação
    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda3podologia', methods=['POST'])
def agenda3podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 🔹 1. INSERE O AGENDAMENTO PRINCIPAL
        cursor.execute("""
            INSERT INTO agendamentospodologa
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        # 🔹 2. BLOQUEIA 08:30 E 09:00
        hora_base = datetime.strptime(horario, "%H:%M")

        bloqueios = [
            hora_base + timedelta(minutes=30),
            hora_base + timedelta(minutes=60)
        ]

        for hb in bloqueios:
            horario_bloqueado = hb.strftime("%H:%M")

            cursor.execute("""
            INSERT INTO agendamentospodologa
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático"))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda4podologia', methods=['POST'])
def agenda4podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']
    servico = request.form['servico']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 🔹 1. INSERE O AGENDAMENTO PRINCIPAL
        cursor.execute("""
            INSERT INTO agendamentospodologa
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        # 🔹 2. BLOQUEIA 08:30 E 09:00
        hora_base = datetime.strptime(horario, "%H:%M")

        bloqueios = [
            hora_base + timedelta(minutes=30),
            hora_base + timedelta(minutes=60),
            hora_base + timedelta(minutes=90)
        ]

        for hb in bloqueios:
            horario_bloqueado = hb.strftime("%H:%M")

            cursor.execute("""
            INSERT INTO agendamentospodologa
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático"))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)



#==========================================================================================================================
#==========================================================================================================================
@app.route('/agendado')
def agendado():
    return render_template('agendado.html')

@app.route('/get_horarios/<data>')
def get_horarios(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome, contato, horario, pagamento, servico
        FROM agendamentosmanicure
        WHERE data = %s
    """, (data,))

    agendamentos = cursor.fetchall()

    lista_agendamentos = []

    for nome, contato, horario, pagamento, servico in agendamentos:
        lista_agendamentos.append({
            "nome": nome,
            "contato": contato,
            "horario": horario.strftime('%H:%M') if horario else None,
            "pagamento": pagamento,
            "servico": servico
        })


    cursor.close()
    conn.close()

    return jsonify(lista_agendamentos)


#---------------------------------------------------------------------------------------------------------------
@app.route('/agendadopodologia')
def agendadopodologia():
    return render_template('agendadopodologia.html')

@app.route('/get_horariop/<data>')
def get_horariop(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome, contato, horario, pagamento, servico
        FROM agendamentospodologa
        WHERE data = %s
    """, (data,))

    agendamentos = cursor.fetchall()

    lista_agendamentosp = []

    for nome, contato, horario, pagamento, servico in agendamentos:
        lista_agendamentos.append({
            "nome": nome,
            "contato": contato,
            "horario": horario.strftime('%H:%M') if horario else None,
            "pagamento": pagamento,
            "servico": servico
        })


    cursor.close()
    conn.close()

    return jsonify(lista_agendamentosp)


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
