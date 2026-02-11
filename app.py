from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import timedelta
from flask import request, redirect, url_for, flash
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Date, Time
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from datetime import datetime, time
from urllib.parse import urlencode


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

#========================== LOGIN ============================================

@app.route('/login', methods=['POST'])
def logar():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'feliciano' and password == '123456':
        return redirect("https://www.galeriashalom.com.br/agendado.html")
        
    elif username == 'amanda' and password == '123456':
        return redirect("https://www.galeriashalom.com.br/agendadopodologia.html")

    elif username == 'silveria' and password == '123456':
        return redirect("https://www.galeriashalom.com.br/agendado.html")

    else:
        return redirect("https://www.galeriashalom.com.br/login.html?erro=1")

#========================== AGENDAMENTO PARA MANICURE====================================================
@app.route('/agenda1manicure', methods=['POST'])
def agenda1manicure():
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
        SELECT nome, contato, horario, pagamento, servico
        FROM agendamentosmanicure
        WHERE DATE(data) = %s
    """, (data,))

    agendamentos = cursor.fetchall()

    lista_agendamentos = []

    for nome, contato, horario, pagamento, servico in agendamentos:
        lista_agendamentos.append({
            "nome": nome,
            "contato": contato,
            "horario": horario.strftime('%H:%M'),  # 🔥 SIMPLES
            "pagamento": pagamento,
            "servico": servico
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
        SELECT nome, contato, horario, pagamento, servico
        FROM agendamentospodologa
        WHERE data = %s
    """, (data,))


    agendamentos = cursor.fetchall()

    lista_agendamentosp = []

    for nome, contato, horario, pagamento, servico in agendamentos:
        lista_agendamentosp.append({
            "nome": nome,
            "contato": contato,
            "horario": horario.strftime('%H:%M'),  # 🔥 SIMPLES
            "pagamento": pagamento,
            "servico": servico
        })

    cursor.close()
    conn.close()

    return jsonify(lista_agendamentosp)


#--------------------------------------- CANCELAR AGENDAMENTO---------------------------------------------------------------------
@app.route('/cancelar_agendamento', methods=['POST'])
def cancelar_agendamento():
    data = request.form['data']
    contato = request.form['contato']

    cursor = None
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 🔍 Verifica se existe
        cursor.execute("""
            SELECT id
            FROM agendamentosmanicure
            WHERE data = %s AND contato = %s
        """, (data, contato))

        agendamento = cursor.fetchone()

        if not agendamento:
            flash("❌ Agendamento não encontrado.", "erro")
            return redirect(f"https://www.galeriashalom.com.br/agendado.html")

        # ❌ Cancela
        cursor.execute("""
            DELETE FROM agendamentosmanicure
            WHERE data = %s AND contato = %s
        """, (data, contato))

        conn.commit()
        flash("✅ Agendamento cancelado com sucesso!", "sucesso")

    except Exception as e:
        print("Erro:", e)
        flash("❌ Erro ao cancelar agendamento.", "erro")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
    return redirect(f"https://www.galeriashalom.com.br/confirmacancelamento.html")



@app.route('/cancelar_agendamentop', methods=['POST'])
def cancelar_agendamentop():
    data = request.form['data']
    contato = request.form['contato']

    cursor = None
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 🔍 Verifica se existe
        cursor.execute("""
            SELECT id
            FROM agendamentospodologa
            WHERE data = %s AND contato = %s
        """, (data, contato))

        agendamento = cursor.fetchone()

        if not agendamento:
            flash("❌ Agendamento não encontrado.", "erro")
            return redirect(f"https://www.galeriashalom.com.br/agendadopodologia.html")

        # ❌ Cancela
        cursor.execute("""
            DELETE FROM agendamentospodologa
            WHERE data = %s AND contato = %s
        """, (data, contato))

        conn.commit()
        flash("✅ Agendamento cancelado com sucesso!", "sucesso")

    except Exception as e:
        print("Erro:", e)
        flash("❌ Erro ao cancelar agendamento.", "erro")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
    return redirect(f"https://www.galeriashalom.com.br/confirmacancelamento.html")


#==========================================================================================================================
#==========================================================================================================================


if __name__ == '__main__':
    app.run(debug=True)
