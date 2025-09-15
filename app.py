import os
print(os.getenv("HF_API_TOKEN"))
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Token da Hugging Face - configure no Render como variável de ambiente
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

print("DEBUG TOKEN:", HF_API_TOKEN)

# Modelo multilíngue (funciona com português)
MODEL_ID = "nlptown/bert-base-multilingual-uncased-sentiment"

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}


def query(payload):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=20)
        return response.json()
    except Exception as e:
        print("Erro na requisição:", e)
        return {"error": str(e)}


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        email_text = request.form.get("email_text", "").strip()

        if not email_text:
            result = {
                "email": "",
                "categoria": "erro",
                "score": 0,
                "resposta": "⚠️ Por favor, insira um texto de e-mail.",
            }
            return render_template("index.html", **result)

        output = query({"inputs": email_text})
        print("DEBUG OUTPUT:", output)  # Debug no terminal

        # Se a API retornar erro
        if "error" in output:
            result = {
                "email": email_text,
                "categoria": "erro",
                "score": 0,
                "resposta": "⚠️ Houve um problema ao acessar a API de IA. Tente novamente.",
            }
            return render_template("index.html", **result)

        label = "unknown"
        score = 0

        if isinstance(output, list) and len(output) > 0:
            predictions = output[0] if isinstance(output[0], list) else output
            best = max(predictions, key=lambda x: x.get("score", 0))
            label = best.get("label", "unknown")
            score = best.get("score", 0)

        # Mapear as estrelas para Produtivo/Improdutivo
        if label in ["4 stars", "5 stars"]:
            categoria = "Produtivo"
            resposta = "✅ Este email parece relevante. Vale a pena responder ou priorizar."
        elif label in ["1 star", "2 stars", "3 stars"]:
            categoria = "Improdutivo"
            resposta = "🚫 Este email não traz informações úteis. Pode ser ignorado."
        else:
            categoria = "Indefinido"
            resposta = "❓ Não foi possível determinar se o email é produtivo."

        result = {
            "email": email_text,
            "categoria": categoria,
            "score": round(score, 3),
            "resposta": resposta,
        }

    return render_template("index.html", **(result or {}))


if __name__ == "__main__":
    app.run(debug=True)

