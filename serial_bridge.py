import requests
import time
import serial
import serial.tools.list_ports

# ======================================================
# CONFIGURAÇÕES DO SISTEMA
# ======================================================

API_URL = "http://127.0.0.1:5000/api/v1/previsao"
INTERVALO_CONSULTA = 3600  # 1 hora = 3600 segundos

# MODO TESTE — USE True SE NÃO TIVER ARDUINO CONECTADO
MODO_TESTE = False


# ======================================================
# FUNÇÃO: BUSCAR PORTA DO ARDUINO AUTOMATICAMENTE
# ======================================================

def encontrar_porta_arduino():
    print("Procurando Arduino nas portas COM...")

    portas = serial.tools.list_ports.comports()

    for porta in portas:
        if "Arduino" in porta.description or "CH340" in porta.description:
            print(f"Arduino encontrado em: {porta.device}")
            return porta.device

    print("Nenhum Arduino encontrado.")
    return None


# ======================================================
# COMUNICAÇÃO COM A API
# ======================================================

def consultar_api():
    try:
        resposta = requests.get(API_URL, timeout=5)
        dados = resposta.json()
        print(f"Previsão recebida: vai chover = {dados['vai_chover']} (probabilidade={dados['probabilidade']})")
        return dados

    except Exception as erro:
        print("Erro ao consultar a API:", erro)
        return None


# ======================================================
# MODO TESTE (SEM ARDUINO)
# ======================================================

def modo_simulacao():
    print("\nModo simulação ativado (sem Arduino).")
    print("O sistema consultará a API a cada 1 hora.\n")

    while True:
        dados = consultar_api()
        if dados:
            if dados["vai_chover"]:
                print("Simulação: Não irrigar (chuva prevista).")
            else:
                print("Simulação: Irrigar (sem chuva prevista).")

        print("Aguardando 1 hora para nova consulta...\n")
        time.sleep(INTERVALO_CONSULTA)


# ======================================================
# MODO COM ARDUINO REAL
# ======================================================

def modo_arduino():
    porta = encontrar_porta_arduino()

    if porta is None:
        print("\nNenhum Arduino detectado. Iniciando modo simulação...")
        modo_simulacao()
        return

    arduino = serial.Serial(porta, 9600, timeout=1)
    time.sleep(2)

    print("\nArduino conectado.")
    print("Sistema de irrigação iniciado.")
    print("Consultas automáticas a cada 1 hora.\n")

    while True:
        print("\nEnviando comando ao Arduino: pedir_previsao")
        arduino.write(b"pedir_previsao\n")
        time.sleep(1)

        resposta = arduino.readline().decode().strip()
        print("Resposta do Arduino:", resposta)

        dados = consultar_api()
        if dados is None:
            continue

        if dados["vai_chover"]:
            print("Enviando comando: API:sim (não irrigar)")
            arduino.write(b"API:sim\n")
        else:
            print("Enviando comando: API:nao (irrigar)")
            arduino.write(b"API:nao\n")

        print("Aguardando 1 hora para nova consulta...")
        time.sleep(INTERVALO_CONSULTA)


# ======================================================
# INÍCIO DO PROGRAMA
# ======================================================

if __name__ == "__main__":
    print("Iniciando sistema de irrigação...\n")

    if MODO_TESTE:
        modo_simulacao()
    else:
        modo_arduino()
