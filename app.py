from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# 🔹 Carrega o classificador Hugging Face
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classificar_email(texto_email):
    labels = ["Produtivo", "Improdutivo"]

    hypothesis_template = (
        "Este email deve ser classificado como {} "
        "apenas se corresponder exatamente à definição: "
        "- PRODUTIVO: quando pede atualização, solicita ação, ou requer resposta objetiva. "
        "- IMPRODUTIVO: quando é felicitação, agradecimento, cumprimento ou mensagem sem ação."
    )

    resultado = classifier(texto_email, labels, hypothesis_template=hypothesis_template)
    categoria = resultado["labels"][0]

    # 🔹 Resposta sugerida
    if categoria == "Produtivo":
        resposta = "✅ Entendido. Vamos processar sua solicitação e retornaremos em breve."
    else:
        resposta = "📩 Obrigado pela mensagem! Não é necessária ação adicional."

    return categoria, resposta


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        email_texto = request.form["email_texto"]
        categoria, resposta = classificar_email(email_texto)
        resultado = {
            "email": email_texto,
            "categoria": categoria,
            "resposta": resposta
        }
    return render_template("index.html", resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)


