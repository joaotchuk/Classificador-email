from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classificar_email(texto_email):
    texto_lower = texto_email.lower()

    palavras_produtivo = ["suporte", "ajuda", "problema", "erro", "conta", "acessar", "login", "senha", "status", "solicitação","fatura","conta"]
    palavras_improdutivo = ["obrigado", "agradeço", "feliz", "parabéns", "bom dia", "boa tarde", "boa noite"]

    if any(p in texto_lower for p in palavras_produtivo):
        categoria = "Produtivo"
    elif any(p in texto_lower for p in palavras_improdutivo):
        categoria = "Improdutivo"
    else:
        labels = ["Produtivo", "Improdutivo"]
        hypothesis_template = (
            "Este email deve ser considerado {}. "
            "- PRODUTIVO: quando solicita ajuda, pede suporte, traz problema, pede status ou ação concreta. "
            "- IMPRODUTIVO: quando é apenas agradecimento, felicitação, cumprimento ou mensagem sem necessidade de resposta."
        )
        resultado = classifier(texto_email, labels, hypothesis_template=hypothesis_template)
        categoria = resultado["labels"][0]

    if categoria == "Produtivo":
        resposta = "✅ Entendido. Vamos processar sua solicitação e retornaremos em breve."
    else:
        resposta = "📩 Obrigado pela mensagem! Não é necessária ação adicional."

    return categoria, resposta


@app.route("/", methods=["GET", "POST"])
def index():
    email = categoria = resposta = None
    if request.method == "POST":
        email_texto = request.form["email_texto"]
        categoria, resposta = classificar_email(email_texto)
        email = email_texto
    return render_template("index.html", email=email, categoria=categoria, resposta=resposta)


if __name__ == "__main__":
    app.run(debug=True)

