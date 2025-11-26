from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)


LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")
API_KEY = os.getenv("OPENWEATHER_API_KEY")
LIMITE_CHANCE_CHUVA = float(os.getenv("LIMITE_CHANCE_CHUVA", 0.5))

URL_CLIMA = "http://api.openweathermap.org/data/2.5/forecast"


DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")


def conectar_pg():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


def inicializar_banco():
    conn = conectar_pg()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS historico_previsao (
            id SERIAL PRIMARY KEY,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            prob_chuva REAL,
            vai_chover BOOLEAN
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

inicializar_banco()


@app.route("/api/v1/previsao", methods=["GET"])
def previsao():
    try:
        parametros = {
            "lat": LATITUDE,
            "lon": LONGITUDE,
            "appid": API_KEY,
            "units": "metric"
        }

        resposta = requests.get(URL_CLIMA, params=parametros)
        resposta.raise_for_status()
        dados = resposta.json()

        max_prob_chuva = 0.0

        # Verifica primeiras 4 horas
        for i in range(4):
            if i < len(dados.get('list', [])):
                prob = dados['list'][i].get('pop', 0.0)
                max_prob_chuva = max(max_prob_chuva, prob)

        vai_chover = max_prob_chuva >= LIMITE_CHANCE_CHUVA

      
        conn = conectar_pg()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO historico_previsao (prob_chuva, vai_chover)
            VALUES (%s, %s)
        """, (max_prob_chuva, vai_chover))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "vai_chover": vai_chover,
            "probabilidade": round(max_prob_chuva, 2)
        })

    except Exception as e:
        print("ERRO DETECTADO:", e)
        return jsonify({"erro": str(e)}), 500


@app.route("/")
def home():
    return jsonify({"status": "API da Horta Online com PostgreSQL"})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
