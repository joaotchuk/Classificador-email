import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-1"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

app = Flask(__name__)

def classificar_email(email_texto):
    try:
        payload = {
            "inputs": email_texto,
            "parameters": {
                "candidate_labels": ["Produtivo", "Improdutivo"]
            }
        }
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        if "labels" in result:
            categoria = result["labels"][0]
            if categoria == "Produtivo":
                resposta = "✅ Obrigado pelo seu email! Vamos analisá-lo em breve."
            else:
                resposta = "📩 Obrigado pela mensagem! Não é necessária ação adicional."
        else:
            categoria = "Erro"
            resposta = f"⚠️ Erro na classificação: {result}"

        return categoria, resposta
    except Exception as e:
        return "Erro", f"⚠️ Erro na classificação: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email_texto = request.form["email_texto"]
        categoria, resposta = classificar_email(email_texto)
        return render_template("index.html", resultado={
            "email": email_texto,
            "categoria": categoria,
            "resposta": resposta
        })
    return render_template("index.html", resultado=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
