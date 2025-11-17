from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Agora tudo vem do .env
LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")
API_KEY = os.getenv("OPENWEATHER_API_KEY")
LIMITE_CHANCE_CHUVA = float(os.getenv("LIMITE_CHANCE_CHUVA", 0.5))

URL_CLIMA = "http://api.openweathermap.org/data/2.5/forecast"

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

        for i in range(4):  
            if i < len(dados.get('list', [])):
                prob = dados['list'][i].get('pop', 0.0)
                max_prob_chuva = max(max_prob_chuva, prob)

        vai_chover = max_prob_chuva >= LIMITE_CHANCE_CHUVA

        return jsonify({
            "vai_chover": vai_chover,
            "probabilidade": round(max_prob_chuva, 2)
        })

    except Exception as e:
        print("ERRO DETECTADO NA API:", e) 
        return jsonify({
            "erro": "Falha ao consultar API do clima",
            "detalhe": str(e)
        }), 500


@app.route("/")
def home():
    return jsonify({"status": "API da Horta Online"})


if __name__ == "__main__":
    print("API KEY LIDA:", API_KEY)
    app.run(debug=False, host="0.0.0.0", port=5000)
