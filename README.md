# 🌱 Horta Vertical Inteligente — API + Automação

Projeto de automação para uma horta vertical que utiliza **Python**, **Flask**, **OpenWeather API** e **Arduino**.  
O sistema consulta a previsão do tempo e decide automaticamente se deve **regar ou não** as plantas.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **Flask**
- **Requests**
- **Dotenv**
- **Serial (pyserial)**
- **Arduino Uno/Nano**
- **OpenWeather API**
- **HTML + CSS + JavaScript**

---

## 📂 Estrutura do Projeto

horta_api/
│
├── app.py # API Flask que consulta o clima
├── serial_bridge.py # Comunicação com Arduino (modo real ou simulado)
├── index.html # Interface simples para testes
├── .gitignore
├── requirements.txt
└── .env.example # Exemplo de arquivo .env