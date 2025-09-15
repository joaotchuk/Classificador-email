import os
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Pegue o token do Hugging Face via variável de ambiente
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Modelo escolhido na Hugging Face
MODEL_ID = "distilbert-base-uncased-finetuned-sst-2-english"

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}


def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        email_text = request.form["email_text"]

        output = query({"inputs": email_text})
        prediction = output[0][0]  # Pega a 1ª classe

        label = prediction["label"]
        score = prediction["score"]

        if "positive" in label.lower():
            categoria = "produtivo"
            resposta = "Esse e-mail parece importante. Vale a pena responder."
        else:
            categoria = "improdutivo"
            resposta = "Esse e-mail não é produtivo. Pode ser ignorado ou marcado."

        result = {
            "email": email_text,
            "categoria": categoria,
            "score": round(score, 3),
            "resposta": resposta,
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
