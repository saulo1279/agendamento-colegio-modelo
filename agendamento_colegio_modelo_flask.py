from flask import Flask, request, jsonify
import gspread
import openai
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Autenticação com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json
creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)

# ID da planilha (você pode mudar via variável de ambiente no Render)
spreadsheet_id = os.getenv("PLANILHA_ID")
sheet = client.open_by_key(spreadsheet_id).worksheet("Página1")

# Chave da OpenAI (opcional - pode estar em branco se ainda não estiver usando IA)
openai.api_key = os.getenv("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")

@app.route('/')
def home():
    return "API do Colégio Modelo funcionando! 🔥"

@app.route('/perguntar', methods=['POST'])
def perguntar():
    data = request.get_json()
    pergunta = data.get("pergunta")
    numero = data.get("numero")

    # Exemplo simples de checagem de agendamento
    visitas_disponiveis = sheet.get_all_records()

    resposta = "Olá! Recebemos sua pergunta, mas a IA ainda não está ativada."
    for linha in visitas_disponiveis:
        if linha["status"].lower() == "disponível":
            resposta = f"Temos vaga dia {linha['data']} às {linha['hora']} com {linha['profissional']}. Deseja confirmar?"
            break

    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
