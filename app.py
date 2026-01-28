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
from psycopg2.pool import SimpleConnectionPool

# ----------------------
# CONFIG BANCO (Render)
# ----------------------
app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)

@app.route("/test")
def test():
    cur = conn.cursor()
    cur.execute("SELECT 1")
    return jsonify({"status": "conectado com sucesso 🚀"})

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
            resultado.append({
                "nome": nome,
                "contato": contato,
                "horario": horario.strftime('%H:%M'),
                "pagamento": pagamento,
                "servico": servico
            })

        return jsonify(resultado)

    except Exception as e:
        print("ERRO /get_horarios:", e)
        return jsonify({"erro": "Erro ao buscar horários"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            close_db_connection(conn)



# =======================
# PODOLOGIA
# =======================
@app.route('/get_horariop/<data>')
def get_horariop(data):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT nome, contato, horario, pagamento, servico
            FROM agendamentospodologa
            WHERE data = %s
        """, (data,))

        agendamentos = cursor.fetchall()

        resultado = []
        for nome, contato, horario, pagamento, servico in agendamentos:
            resultado.append({
                "nome": nome,
                "contato": contato,
                "horario": horario.strftime('%H:%M'),
                "pagamento": pagamento,
                "servico": servico
            })

        return jsonify(resultado)

    except Exception as e:
        print("ERRO /get_horariop:", e)
        return jsonify({"erro": "Erro ao buscar horários"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            close_db_connection(conn)


# =======================
# HEALTH CHECK (Render)
# =======================
@app.route('/')
def health():
    return jsonify({"status": "API Galeria Shalom ONLINE 🚀"})


if __name__ == '__main__':
    app.run()
