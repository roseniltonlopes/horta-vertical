import requests
import time
import sys

API_URL = "http://127.0.0.1:5000/api/v1/previsao"
TIMEOUT = 5

def checar_api():
    try:
        print("-> Solicitando:", API_URL)
        r = requests.get(API_URL, timeout=TIMEOUT)
        r.raise_for_status()
        dados = r.json()
        # valida campos esperados
        if "vai_chover" not in dados or "probabilidade" not in dados:
            print("[ERRO] Resposta inesperada da API:", dados)
            return False
        print("Resposta OK: vai_chover =", dados["vai_chover"], ", probabilidade =", dados["probabilidade"])
        return True
    except requests.exceptions.RequestException as e:
        print("[ERRO] Falha na requisição:", e)
        return False
    except ValueError as e:
        print("[ERRO] JSON inválido:", e)
        return False

def simulacao_comportamento(dados):
    # Simula o que o serial_bridge faria ao receber a resposta
    if dados["vai_chover"]:
        print("Simulação: decisão -> NÃO irrigar (API:sim)")
    else:
        print("Simulação: decisão -> IRRIGAR (API:nao)")

def main():
    print("=== Teste de integração API (modo simulado) ===")
    ok = checar_api()
    if not ok:
        print("Teste interrompido: verifique se a API está rodando (python app.py).")
        sys.exit(1)

    # busca os dados e simula ação
    dados = requests.get(API_URL, timeout=TIMEOUT).json()
    simulacao_comportamento(dados)

    print("\nTeste concluído com sucesso (modo simulado).")
    print("Se quiser testar o serial_bridge real, ative o Arduino e rode serial_bridge.py (MODO_TESTE=False).")

if __name__ == "__main__":
    main()
