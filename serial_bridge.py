import time
import requests

API_URL = "http://127.0.0.1:5000/api/v1/previsao"

print("🔧 Modo teste sem Arduino iniciado!")

while True:
    print("\n[SIMULAÇÃO] Enviando comando 'pedir_previsao'...")
    time.sleep(2)

    try:
        r = requests.get(API_URL).json()
        vai = r["vai_chover"]

        print("Resposta da API → Vai chover?", vai)

    except Exception as e:
        print("Erro ao consultar API:", e)

    time.sleep(5)
