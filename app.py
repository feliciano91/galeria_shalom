import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from datetime import datetime, time

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://www.galeriashalom.com.br",
            "https://galeriashalom.com.br"
        ]
    }
})

DATABASE_URL = (
    "postgresql://postgres.mawrehqblzcaujuakxqp:FSamdGS912026@aws-1-us-east-1.pooler.supabase.com:5432/postgres"
)


# ======================================
# ROTAS
# ======================================

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
# ======================================
# MAIN
# ======================================
if __name__ == '__main__':
    app.run(debug=True)
