from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from datetime import datetime

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
DATABASE_URL = (
    "postgresql://galeria_shalom_db_user:"
    "A9vUujpt3sM1D01UNz3x4fJi8QWnejTo@"
    "dpg-d55iorumcj7s73fcj4dg-a.oregon-postgres.render.com:5432/"
    "galeria_shalom_db"
    "?sslmode=require"
)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# =======================
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
