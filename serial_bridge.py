import serial
import time
import requests
import os
from serial.tools import list_ports

PORTA_SERIAL = 'COM5' 
BAUDRATE = 115200 

# ---------------- CONFIGURAÇÃO DA SUA API FLASK ----------------
URL_SUA_API = "http://127.0.0.1:5000/api/v1/previsao" 

# ---------------- FUNÇÕES DE COMUNICAÇÃO ----------------

def consultar_sua_api():
    """Chama o endpoint Flask e retorna a resposta formatada para o Arduino."""
    print("-> Chamando a API Flask...")
    try:
        #Chamar o endpoint Flask
        resposta = requests.get(URL_SUA_API, timeout=10)
        resposta.raise_for_status() 
        dados = resposta.json()

        vai_chover = dados.get('vai_chover', False)
        
        if vai_chover:
            return "API:sim" 
        else:
            return "API:nao"

    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar a API Flask: {e}")
        return "API:erro"

def enviar_resposta(ser, resposta):
    """Envia a string de resposta para o Arduino via serial, seguida por quebra de linha."""
    ser.write(f"{resposta}\n".encode('utf-8'))
    print(f"<- Resposta enviada ao Arduino: {resposta}")

# ---------------- LOOP PRINCIPAL DO CLIENTE SERIAL ----------------

def main():
    try:
        ser = serial.Serial(PORTA_SERIAL, BAUDRATE, timeout=1)
        time.sleep(2) 
        print(f"Cliente Serial conectado em {PORTA_SERIAL} @ {BAUDRATE}. Monitorando comandos...")
        print("-" * 50)

    except serial.SerialException as e:
        print(f"ERRO: Não foi possível abrir a porta serial {PORTA_SERIAL}.")
        print("Verifique se o Arduino está conectado e a porta está correta.")
        print(e)
        return

    while True:  
        linha = ser.readline().decode('utf-8').strip()
        
        if linha == "pedir_previsao":
            print(f"[{time.strftime('%H:%M:%S')}] > Comando recebido do Arduino: {linha}")
            
            resposta_api = consultar_sua_api()
            
            enviar_resposta(ser, resposta_api)
        
        time.sleep(0.1)

if __name__ == "__main__":
    main()