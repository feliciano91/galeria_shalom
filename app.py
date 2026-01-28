from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/teste')
def teste():
    return jsonify({"status": "backend funcionando"})

@app.route('/api/manicure/horarios/<data>')
def get_horarios_manicure(data):
    return jsonify({"data": data})

if __name__ == "__main__":
    app.run()
