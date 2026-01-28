from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_cors import CORS
import psycopg2
from sqlalchemy.orm import declarative_base, sessionmaker
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from datetime import datetime
from datetime import timedelta
from datetime import time
import sqlite3
import os

app = Flask(__name__)

# 🔥 CORS – libera apenas seu domínio
CORS(app, resources={
    r"/get_*": {
        "origins": [
            "https://galeriashalom.com.br",
            "https://www.galeriashalom.com.br"
        ]
    }
})

# ----------------------
# CONFIG BANCO (Render)
# ----------------------
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require",
        connect_timeout=10
    )

# =======================

@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return "Conexão com banco OK 🚀"
    except Exception as e:
        return str(e), 500



# MANICURE
# =======================
@app.route('/get_horarios/<data>')
def get_horarios(data):
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT nome, contato, horario, pagamento, servico
            FROM agendamentosmanicure
            WHERE data = %s
        """, (data,))

        agendamentos = cursor.fetchall()
        resultado = []

        for nome, contato, horario, pagamento, servico in agendamentos:
            if horario is None:
                horario_formatado = None
            elif isinstance(horario, str):
                horario_formatado = horario[:5]
            else:
                horario_formatado = horario.strftime('%H:%M')

            resultado.append({
                "nome": nome,
                "contato": contato,
                "horario": horario_formatado,
                "pagamento": pagamento,
                "servico": servico
            })

        return jsonify(resultado)

    except Exception as e:
        print("ERRO /get_horarios:", e)
        return jsonify({"erro": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# =======================
# PODOLOGIA
# =======================
@app.route('/get_horariop/<data>')
def get_horariop(data):
    conn = None
    cursor = None

    try:
        # 🔹 Converte string da URL para DATE
        data_formatada = datetime.strptime(data, "%Y-%m-%d").date()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT nome, contato, horario, pagamento, servico
            FROM agendamentospodologa
            WHERE data = %s
        """, (data_formatada,))

        agendamentos = cursor.fetchall()

        resultado = []
        for nome, contato, horario, pagamento, servico in agendamentos:
            resultado.append({
                "nome": nome,
                "contato": contato,
                "horario": horario.strftime('%H:%M') if horario else None,
                "pagamento": pagamento,
                "servico": servico
            })

        return jsonify(resultado)

    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    except Exception as e:
        print("ERRO /get_horariop:", e)
        return jsonify({"erro": str(e)}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# =======================
# HEALTH CHECK (Render)
# =======================
@app.route('/')
def health():
    return jsonify({"status": "API Galeria Shalom ONLINE 🚀"})


if __name__ == '__main__':
    app.run()
