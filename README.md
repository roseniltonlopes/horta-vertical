#  HORTA_API  
### Automação Inteligente para Horta Vertical

**HORTA_API** é o backend responsável pela automação de um sistema de **Horta Vertical Inteligente**.  
O projeto utiliza **Python + Flask** para expor uma API capaz de tomar decisões automáticas de irrigação com base em dados reais de previsão do tempo, além de se comunicar diretamente com um **Arduino**, responsável pelo controle físico da bomba d’água.

---

##  Funcionalidades Principais

###  Automação Inteligente  
A API consulta o **OpenWeatherMap** para obter previsões de chuva nas próximas horas.

###  Decisão Lógica  
-  **Se a previsão de chuva for alta:** a irrigação é *suspensa* para economizar água.  
-  **Caso contrário:** a API envia comando para **acionar a bomba**.

###  Comunicação Serial  
- Implementada com **PySerial**, permite enviar comandos diretos do Python para o Arduino.

###  Controle Físico  
- O Arduino recebe os comandos e aciona um **relé**, que controla a bomba d’água.
- LEDs indicam estados de irrigação no sistema físico (opcional).

###  Modo de Simulação  
Inclui o módulo **simulador_arduino.py**, que emula o comportamento do Arduino.  
Útil para testes quando o hardware não está disponível.

---

##  Tecnologias Utilizadas

| Categoria          | Tecnologia        | Função no Projeto                                   |
|-------------------|-------------------|------------------------------------------------------|
| Backend           | Python 3.10+      | Linguagem principal                                  |
| Framework         | Flask             | Criação dos endpoints da API                         |
| API Externa       | Requests          | Consumo da API OpenWeatherMap                        |
| Comunicação Serial| PySerial          | Ponte Python ↔ Arduino                               |
| Microcontrolador  | Arduino Uno/Nano  | Controle físico da bomba via relé                    |
| Configuração      | python-dotenv     | Carregamento de variáveis de ambiente (.env)         |

---

##  Estrutura Recomendada do Projeto
```bash
HORTA_API/
├── app.py
├── simulador_arduino.py
├── requirements.txt
├── .env
├── README.md
└── utils/
    ├── weather.py
    └── serial_controller.py
