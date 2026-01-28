from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
#from flask_mysqldb import MySQL
from datetime import datetime  # Importando o módulo datetime
from datetime import timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import time
from flask import request, redirect, url_for, flash
import sqlite3
from flask_cors import CORS
from flask import Flask



app = Flask(__name__)

# 🔓 CORS CORRETO (sem barra no final)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://galeriashalom.com.br",
            "https://www.galeriashalom.com.br"
        ]
    }
})

# 🔑 Secret
app.secret_key = "123456"

# 🗄️ Banco Render
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

#===============================  MANICURE  ===============================================
@app.route('/api/teste')
def teste():
    return {"status": "backend funcionando"}


#========================== AGENDAMENTO PARA MANICURE====================================================
# ================== API MANICURE ==================
@app.route("/api/agenda1manicure", methods=["POST"])
def agenda1manicure():
    dados = request.get_json()

    if not dados:
        return jsonify({"status": "erro", "mensagem": "JSON inválido"}), 400

    nome = dados.get("nome")
    contato = dados.get("contato")
    data = dados.get("data")
    horario = dados.get("horario")
    pagamento = dados.get("pagamento")
    servico = dados.get("servico")

    if not all([nome, contato, data, horario, pagamento, servico]):
        return jsonify({
            "status": "erro",
            "mensagem": "Campos obrigatórios ausentes"
        }), 400

    conn = None
    cursor = None

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
        print("ERRO:", e)
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao salvar agendamento"
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")

    return jsonify({
        "status": "ok",
        "mensagem": "Agendamento confirmado",
        "data": data_formatada,
        "horario": horario,
        "pagamento": pagamento
    })


@app.route('/agenda2manicure', methods=['POST'])
def agenda2manicure():
    dados = request.get_json()

    nome = dados.get('nome')
    contato = dados.get('contato')
    data = dados.get('data')
    horario = dados.get('horario')
    pagamento = dados.get('pagamento')
    servico = dados.get('servico')

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
        """, (
            nome,
            contato,
            data,
            horario_bloqueado,
            "Bloqueado",
            "Bloqueio automático"
        ))

        conn.commit()

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao salvar agendamento"
        }), 500

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

    return jsonify({
        "status": "ok",
        "mensagem": "Agendamento confirmado com bloqueio automático",
        "data": data_formatada,
        "horario": horario,
        "horario_bloqueado": horario_bloqueado,
        "pagamento": pagamento
    })


@app.route('/agenda3manicure', methods=['POST'])
def agenda3manicure():
    dados = request.get_json()

    nome = dados.get('nome')
    contato = dados.get('contato')
    data = dados.get('data')
    horario = dados.get('horario')
    pagamento = dados.get('pagamento')
    servico = dados.get('servico')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1️⃣ Agendamento principal
        cursor.execute("""
            INSERT INTO agendamentosmanicure
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        # 2️⃣ Bloqueios (+30 e +60)
        hora_base = datetime.strptime(horario, "%H:%M")

        bloqueios = [
            hora_base + timedelta(minutes=30),
            hora_base + timedelta(minutes=60)
        ]

        horarios_bloqueados = []

        for hb in bloqueios:
            h = hb.strftime("%H:%M")
            horarios_bloqueados.append(h)

            cursor.execute("""
                INSERT INTO agendamentosmanicure
                (nome, contato, data, horario, pagamento, servico)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                nome,
                contato,
                data,
                h,
                "Bloqueado",
                "Bloqueio automático"
            ))

        conn.commit()

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao salvar agendamento"
        }), 500

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

    return jsonify({
        "status": "ok",
        "mensagem": "Agendamento confirmado",
        "data": data_formatada,
        "horario": horario,
        "horarios_bloqueados": horarios_bloqueados,
        "pagamento": pagamento
    })
    
    
@app.route('/agenda4manicure', methods=['POST'])
def agenda4manicure():
    dados = request.get_json()

    nome = dados.get('nome')
    contato = dados.get('contato')
    data = dados.get('data')
    horario = dados.get('horario')
    pagamento = dados.get('pagamento')
    servico = dados.get('servico')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1️⃣ Agendamento principal
        cursor.execute("""
            INSERT INTO agendamentosmanicure
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        # 2️⃣ Bloqueios (+30, +60, +90)
        hora_base = datetime.strptime(horario, "%H:%M")

        bloqueios = [
            hora_base + timedelta(minutes=30),
            hora_base + timedelta(minutes=60),
            hora_base + timedelta(minutes=90)
        ]

        horarios_bloqueados = []

        for hb in bloqueios:
            h = hb.strftime("%H:%M")
            horarios_bloqueados.append(h)

            cursor.execute("""
                INSERT INTO agendamentosmanicure
                (nome, contato, data, horario, pagamento, servico)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                nome,
                contato,
                data,
                h,
                "Bloqueado",
                "Bloqueio automático"
            ))

        conn.commit()

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao salvar agendamento"
        }), 500

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

    return jsonify({
        "status": "ok",
        "mensagem": "Agendamento confirmado",
        "data": data_formatada,
        "horario": horario,
        "horarios_bloqueados": horarios_bloqueados,
        "pagamento": pagamento
    })


#===============================  PODOLOGIA  ===============================================

#============================ AGENDAMENTO PARA PODOLOGIA ==================================================
@app.route('/agenda1podologia', methods=['POST'])
def agenda1podologia():
    dados = request.get_json()

    nome = dados.get('nome')
    contato = dados.get('contato')
    data = dados.get('data')
    horario = dados.get('horario')
    pagamento = dados.get('pagamento')
    servico = dados.get('servico')

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
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao salvar agendamento"
        }), 500

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

    return jsonify({
        "status": "ok",
        "mensagem": "Agendamento confirmado",
        "data": data_formatada,
        "horario": horario,
        "pagamento": pagamento
    })

@app.route('/agenda2podologia', methods=['POST'])
def agenda2podologia():
    dados = request.get_json()

    nome = dados.get('nome')
    contato = dados.get('contato')
    data = dados.get('data')
    horario = dados.get('horario')
    pagamento = dados.get('pagamento')
    servico = dados.get('servico')

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
        """, (
            nome,
            contato,
            data,
            horario_bloqueado,
            "Bloqueado",
            "Bloqueio automático"
        ))

        conn.commit()

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao salvar agendamento"
        }), 500

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

    return jsonify({
        "status": "ok",
        "mensagem": "Agendamento confirmado com bloqueio",
        "data": data_formatada,
        "horario": horario,
        "horario_bloqueado": horario_bloqueado,
        "pagamento": pagamento
    })


@app.route('/agenda3podologia', methods=['POST'])
def agenda3podologia():
    dados = request.get_json()

    nome = dados.get('nome')
    contato = dados.get('contato')
    data = dados.get('data')
    horario = dados.get('horario')
    pagamento = dados.get('pagamento')
    servico = dados.get('servico')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1️⃣ Agendamento principal
        cursor.execute("""
            INSERT INTO agendamentospodologa
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        # 2️⃣ Bloqueios (+30 e +60)
        hora_base = datetime.strptime(horario, "%H:%M")

        bloqueios = [
            hora_base + timedelta(minutes=30),
            hora_base + timedelta(minutes=60)
        ]

        horarios_bloqueados = []

        for hb in bloqueios:
            h = hb.strftime("%H:%M")
            horarios_bloqueados.append(h)

            cursor.execute("""
                INSERT INTO agendamentospodologa
                (nome, contato, data, horario, pagamento, servico)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                nome,
                contato,
                data,
                h,
                "Bloqueado",
                "Bloqueio automático"
            ))

        conn.commit()

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao salvar agendamento"
        }), 500

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

    return jsonify({
        "status": "ok",
        "mensagem": "Agendamento confirmado",
        "data": data_formatada,
        "horario": horario,
        "horarios_bloqueados": horarios_bloqueados,
        "pagamento": pagamento
    })

@app.route('/agenda4podologia', methods=['POST'])
def aagenda4podologia():
    dados = request.get_json()

    nome = dados.get('nome')
    contato = dados.get('contato')
    data = dados.get('data')
    horario = dados.get('horario')
    pagamento = dados.get('pagamento')
    servico = dados.get('servico')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1️⃣ Agendamento principal
        cursor.execute("""
            INSERT INTO agendamentospodologa
            (nome, contato, data, horario, pagamento, servico)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, contato, data, horario, pagamento, servico))

        # 2️⃣ Bloqueios (+30, +60, +90)
        hora_base = datetime.strptime(horario, "%H:%M")

        bloqueios = [
            hora_base + timedelta(minutes=30),
            hora_base + timedelta(minutes=60),
            hora_base + timedelta(minutes=90)
        ]

        horarios_bloqueados = []

        for hb in bloqueios:
            h = hb.strftime("%H:%M")
            horarios_bloqueados.append(h)

            cursor.execute("""
                INSERT INTO agendamentospodologa
                (nome, contato, data, horario, pagamento, servico)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                nome,
                contato,
                data,
                h,
                "Bloqueado",
                "Bloqueio automático"
            ))

        conn.commit()

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao salvar agendamento"
        }), 500

    finally:
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')

    return jsonify({
        "status": "ok",
        "mensagem": "Agendamento confirmado",
        "data": data_formatada,
        "horario": horario,
        "horarios_bloqueados": horarios_bloqueados,
        "pagamento": pagamento
    })


#==========================================================================================================================
#==========================================================================================================================

@app.route('/api/manicure/horarios/<data>')
def get_horarios_manicure(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT horario
        FROM agendamentosmanicure
        WHERE data = %s
    """, (data,))

    horarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify([
        h[0].strftime('%H:%M') for h in horarios
    ])

#---------------------------------------------------------------------------------------------------------------

@app.route('/api/podologia/horarios/<data>')
def get_horarios_podologia(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT horario
        FROM agendamentospodologa
        WHERE data = %s
    """, (data,))

    horarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify([
        h[0].strftime('%H:%M') for h in horarios
    ])


#--------------------------------------- CANCELAR AGENDAMENTO---------------------------------------------------------------------

@app.route('/api/podologia/cancelar', methods=['POST'])
def cancelar_agendamentop():
    data = request.json.get('data')
    contato = request.json.get('contato')

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
            return jsonify({
                "status": "erro",
                "mensagem": "Agendamento não encontrado"
            }), 404

        # ❌ Cancela
        cursor.execute("""
            DELETE FROM agendamentospodologa
            WHERE data = %s AND contato = %s
        """, (data, contato))

        conn.commit()

        return jsonify({
            "status": "ok",
            "mensagem": "Agendamento cancelado com sucesso"
        })

    except Exception as e:
        print("Erro:", e)
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao cancelar agendamento"
        }), 500

    finally:
        cursor.close()
        conn.close()



#==========================================================================================================================
#==========================================================================================================================


app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://www.galeriashalom.com.br",
            "https://galeriashalom.com.br"
        ]
    }
})

if __name__ == '__main__':
    app.run(debug=True)
