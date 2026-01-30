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

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require",
        connect_timeout=5
    )

@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return "✅ Conectado ao PostgreSQL (Supabase) com sucesso!"
    except Exception as e:
        return f"❌ Erro ao conectar: {e}"




# ======================================
# ROTAS
# ======================================

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
        cursor.close()
        conn.close()

    data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")

    return jsonify({
        "status": "ok",
        "mensagem": "Agendamento confirmado",
        "data": data_formatada,
        "horario": horario,
        "pagamento": pagamento
    })


@app.route('/api/manicure/horarios/<data>')
def get_horarios_manicure(data):
    try:
        conn = psycopg2.connect(
            DATABASE_URL,
            sslmode="require",
            connect_timeout=5
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT horario
            FROM agendamentosmanicure
            WHERE data::text = %s
        """, (data,))

        horarios = cursor.fetchall()

        return jsonify([
            h[0] if isinstance(h[0], str) else h[0].strftime('%H:%M')
            for h in horarios
        ])

    except Exception as e:
        print("ERRO COMPLETO:", repr(e))
        return jsonify({
            "erro": str(e),
            "tipo": type(e).__name__
        }), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


# ======================================
# MAIN
# ======================================
if __name__ == '__main__':
    app.run(debug=True)
