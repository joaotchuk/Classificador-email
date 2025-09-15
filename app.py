from flask import Flask, render_template, request
import os
import logging
import requests

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

_local_classifier = None
_local_failed = False

def _get_local_classifier():
    global _local_classifier, _local_failed
    if _local_classifier is not None or _local_failed:
        return _local_classifier
    try:
        from transformers import pipeline
        _local_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        return _local_classifier
    except Exception as e:
        logging.exception("local classifier init failed")
        _local_failed = True
        return None

def _classify_with_local(text):
    clf = _get_local_classifier()
    if not clf:
        raise RuntimeError("local classifier not available")
    labels = ["Produtivo", "Improdutivo"]
    hypothesis_template = (
        "Este email deve ser considerado {}. "
        "- PRODUTIVO: quando solicita ajuda, pede suporte, traz problema, pede status ou ação concreta. "
        "- IMPRODUTIVO: quando é apenas agradecimento, felicitação, cumprimento ou mensagem sem necessidade de resposta."
    )
    out = clf(text, labels, hypothesis_template=hypothesis_template)
    return out["labels"][0]

def _classify_with_hf_api(text):
    token = os.getenv("HF_TOKEN") or os.getenv("HF_API_TOKEN") or os.getenv("HF_API_KEY")
    if not token:
        raise RuntimeError("Hugging Face token not set in HF_TOKEN/HF_API_TOKEN/HF_API_KEY")
    url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": ["Produtivo", "Improdutivo"],
            "hypothesis_template": (
                "Este email deve ser considerado {}. "
                "- PRODUTIVO: quando solicita ajuda, pede suporte, traz problema, pede status ou ação concreta. "
                "- IMPRODUTIVO: quando é apenas agradecimento, felicitação, cumprimento ou mensagem sem necessidade de resposta."
            )
        }
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"HF API error {resp.status_code}: {resp.text}")
    data = resp.json()
    if isinstance(data, dict) and data.get("error"):
        raise RuntimeError("HF API error: " + data.get("error", "unknown"))
    return data["labels"][0]

def classificar_email(texto_email):
    t = (texto_email or "").lower()
    palavras_produtivo = ["suporte", "ajuda", "problema", "erro", "conta", "acessar", "login", "senha", "status", "solicitação", "solicit"]
    palavras_improdutivo = ["obrigado", "agradeço", "feliz", "parabéns", "bom dia", "boa tarde", "boa noite", "abraços"]

    if any(p in t for p in palavras_produtivo):
        categoria = "Produtivo"
    elif any(p in t for p in palavras_improdutivo):
        categoria = "Improdutivo"
    else:
        try:
            categoria = _classify_with_local(texto_email)
        except Exception as e_local:
            logging.info("local classifier failed, falling back to HF API")
            try:
                categoria = _classify_with_hf_api(texto_email)
            except Exception as e_api:
                logging.exception("both classifiers failed")
                return "Indefinido", "Erro interno ao classificar. Verifique os logs do servidor."
    if categoria == "Produtivo":
        resposta = "✅ Entendido. Vamos processar sua solicitação e retornaremos em breve."
    else:
        resposta = "📩 Obrigado pela mensagem! Não é necessária ação adicional."
    return categoria, resposta

@app.route("/", methods=["GET", "POST"])
def index():
    email = None
    categoria = None
    resposta = None
    if request.method == "POST":
        email_texto = request.form.get("email_texto", "").strip()
        if email_texto:
            categoria, resposta = classificar_email(email_texto)
            email = email_texto
    return render_template("index.html", email=email, categoria=categoria, resposta=resposta)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

