Horta Vertical Inteligente — API + Automação Automática

Este projeto implementa um sistema de automação para uma horta vertical utilizando Python, Flask, Arduino e integração com a OpenWeather API.
A aplicação consulta automaticamente a previsão do tempo e decide se deve acionar ou não a irrigação da planta.

O Arduino recebe os comandos, aciona um relé conectado à bomba d’água e utiliza LEDs indicadores para mostrar o estado da irrigação.

Tecnologias Utilizadas

Python 3.10+

Flask

Requests

Python Dotenv

PySerial

Arduino Uno (ou Nano)

OpenWeather API (forecast 5-day/3-hour)

HTML para interface simples de testes

Estrutura do Projeto

horta_api/
│
├── app.py                # API Flask que consulta a previsão do tempo
├── serial_bridge.py      # Comunicação Arduino ↔ Python (modo real e simulado)
├── simulador_arduino.py  # Simula respostas caso o Arduino não esteja conectado
├── arduino/
│   └── horta_arduino.ino # Código do Arduino
│
├── index.html            # Interface simples local
├── requirements.txt      # Dependências do Python
├── .env.example          # Modelo do arquivo .env
└── .gitignore
