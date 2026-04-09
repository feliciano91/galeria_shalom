from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import timedelta
from flask import request, redirect, url_for, flash
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Date, Time
import os
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from datetime import datetime, time
from urllib.parse import urlencode

grupo_id = str(uuid.uuid4())
app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://www.galeriashalom.com.br",
            "https://galeriashalom.com.br"
        ]
    }
})

# Configuração do banco
DATABASE_URL = "postgresql://postgres.mawrehqblzcaujuakxqp:FSamdGS912026@aws-1-us-east-1.pooler.supabase.com:5432/postgres"

conn = psycopg2.connect(
    DATABASE_URL,
    sslmode="require"
)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

#========================== HEALTH ============================================
@app.route("/health")
def health():
    return "ok", 200





@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT NOW();")
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        return f"Banco conectado! {resultado}"

    except Exception as e:
        return f"Erro: {e}"
#========================== LOGIN ============================================

usuarios = {
    "feliciano": {
        "teste1": "https://www.galeriashalom.com.br/agendado.html",
        "teste2": "https://www.galeriashalom.com.br/agendadopodologia.html"
    },
    "yasmin": {
        "102030": "https://www.galeriashalom.com.br/agendado.html"
    },
    "amanda": {
        "101112": "https://www.galeriashalom.com.br/agendadopodologia.html"
    }
}

@app.route('/login', methods=['POST'])
def logar():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in usuarios:
        if password in usuarios[username]:
            return redirect(usuarios[username][password])

    return redirect("https://www.galeriashalom.com.br/login.html?erro=1")

#========================== AGENDAMENTO PARA MANICURE====================================================
@app.route('/agenda1manicure', methods=['POST'])
def agenda1manicure():
    grupo_id = str(uuid.uuid4())
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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico, grupo_id))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento", 500

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(
        data, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    params = urlencode({
        "data": data_formatada,
        "horario": horario,
        "pagamento": pagamento
    })

    return redirect(
        f"https://www.galeriashalom.com.br/confirmacao.html?{params}"
    )

@app.route('/agenda2manicure', methods=['POST'])
def agenda2manicure():
    grupo_id = str(uuid.uuid4())
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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico, grupo_id))

        cursor.execute("""
            INSERT INTO agendamentosmanicure
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático", grupo_id))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    # Converter a string da data para um objeto datetime
    data_formatada = datetime.strptime(
        data, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    params = urlencode({
        "data": data_formatada,
        "horario": horario,
        "pagamento": pagamento
    })

    return redirect(
        f"https://www.galeriashalom.com.br/confirmacao.html?{params}"
    )
    
@app.route('/agenda3manicure', methods=['POST'])
def agenda3manicure():
    grupo_id = str(uuid.uuid4())
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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico, grupo_id))

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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático", grupo_id))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(
        data, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    params = urlencode({
        "data": data_formatada,
        "horario": horario,
        "pagamento": pagamento
    })

    return redirect(
        f"https://www.galeriashalom.com.br/confirmacao.html?{params}"
    )

@app.route('/agenda4manicure', methods=['POST'])
def agenda4manicure():
    grupo_id = str(uuid.uuid4())
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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico, grupo_id))

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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático", grupo_id))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(
        data, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    params = urlencode({
        "data": data_formatada,
        "horario": horario,
        "pagamento": pagamento
    })

    return redirect(
        f"https://www.galeriashalom.com.br/confirmacao.html?{params}"
    )

#============================ AGENDAMENTO PARA PODOLOGIA ==================================================
@app.route('/agenda1podologia', methods=['POST'])
def agenda1podologia():
    grupo_id = str(uuid.uuid4())
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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico, grupo_id))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento", 500

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(
        data, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    params = urlencode({
        "data": data_formatada,
        "horario": horario,
        "pagamento": pagamento
    })

    return redirect(
        f"https://www.galeriashalom.com.br/confirmacao1.html?{params}"
    )

@app.route('/agenda2podologia', methods=['POST'])
def agenda2podologia():
    grupo_id = str(uuid.uuid4())
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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico, grupo_id))

        cursor.execute("""
            INSERT INTO agendamentospodologa
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático", grupo_id))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    # Converter a string da data para um objeto datetime
    data_formatada = datetime.strptime(
        data, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    params = urlencode({
        "data": data_formatada,
        "horario": horario,
        "pagamento": pagamento
    })

    return redirect(
        f"https://www.galeriashalom.com.br/confirmacao1.html?{params}"
    )
    
@app.route('/agenda3podologia', methods=['POST'])
def agenda3podologia():
    grupo_id = str(uuid.uuid4())
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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico, grupo_id))

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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático", grupo_id))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    # Converter a string da data para um objeto datetime
    data_formatada = datetime.strptime(
        data, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    params = urlencode({
        "data": data_formatada,
        "horario": horario,
        "pagamento": pagamento
    })

    return redirect(
        f"https://www.galeriashalom.com.br/confirmacao1.html?{params}"
    )
    
@app.route('/agenda4podologia', methods=['POST'])
def agenda4podologia():
    grupo_id = str(uuid.uuid4())
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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico, grupo_id))

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
            (nome, contato, data, horario, pagamento, servico, grupo_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario_bloqueado, "Bloqueado", "Bloqueio automático", grupo_id))

        conn.commit()

    except Exception as e:
        print("Erro:", e)
        return "Erro ao salvar agendamento"

    finally:
        cursor.close()
        conn.close()

    # Converter a string da data para um objeto datetime
    data_formatada = datetime.strptime(
        data, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")
    
    params = urlencode({
        "data": data_formatada,
        "horario": horario,
        "pagamento": pagamento
    })
    
    return redirect(
        f"https://www.galeriashalom.com.br/confirmacao1.html?{params}"
    )

#==========================================================================================================================
#==========================================================================================================================

@app.route('/api/get_horarios/<data>')
def get_horarios(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome, contato, horario, pagamento, servico, grupo_id
        FROM agendamentosmanicure
        WHERE data = %s
    """, (data,))


    agendamento = cursor.fetchall()

    lista_agendamentos = []

    for nome, contato, horario, pagamento, servico, grupo_id in agendamento:
        lista_agendamentos.append({
            "nome": nome,
            "contato": contato,
            "horario": horario.strftime('%H:%M'),  # 🔥 SIMPLES
            "pagamento": pagamento,
            "servico": servico,
            "grupo_id": grupo_id
        })

    cursor.close()
    conn.close()

    return jsonify(lista_agendamentos)


#--------------------------------------------------------------------------------------------------------------

@app.route('/api/get_horariop/<data>')
def get_horariop(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome, contato, horario, pagamento, servico, grupo_id
        FROM agendamentospodologa
        WHERE data = %s
    """, (data,))


    agendamentos = cursor.fetchall()

    lista_agendamentosp = []

    for nome, contato, horario, pagamento, servico, grupo_id in agendamentos:
        lista_agendamentosp.append({
            "nome": nome,
            "contato": contato,
            "horario": horario.strftime('%H:%M'),  # 🔥 SIMPLES
            "pagamento": pagamento,
            "servico": servico,
            "grupo_id": grupo_id
        })

    cursor.close()
    conn.close()

    return jsonify(lista_agendamentosp)


#--------------------------------------- CANCELAR AGENDAMENTO---------------------------------------------------------------------

@app.route('/api/excluir_agendamento', methods=['POST'])
def excluir_agendamento():
    dados = request.get_json()
    grupo_id = dados.get('grupo_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM agendamentosmanicure
            WHERE grupo_id = %s
        """, (grupo_id,))

        conn.commit()

        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

#--------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/api/excluir_agendamentop', methods=['POST'])
def excluir_agendamentop():
    dados = request.get_json()
    grupo_id = dados.get('grupo_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM agendamentospodologa
            WHERE grupo_id = %s
        """, (grupo_id,))

        conn.commit()

        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
#==========================================================================================================================
#==========================================================================================================================


if __name__ == '__main__':
    app.run(debug=True)
