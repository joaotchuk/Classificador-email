from flask import Flask, render_template, request
from transformers import pipeline

# Inicializa o pipeline do Hugging Face
pipe = pipeline("sentiment-analysis")

app = Flask(__name__)

# Função de classificação com regras híbridas
def classificar_email(text):
    palavras_produtivas = [
        "enviar", "acesso", "preciso", "atualizar",
        "ajuda", "dificuldade", "solicitação", "suporte",
        "status", "problema", "erro", "funcionar"
    ]

    # Se encontrar uma palavra produtiva → classifica direto
    if any(p in text.lower() for p in palavras_produtivas):
        categoria = "Produtivo"
        resposta = "Obrigado pelo contato! Sua solicitação será analisada e retornaremos em breve."
        return categoria, resposta

    # Caso contrário, usa o modelo de sentimento
    resultado = pipe(text)[0]["label"]

    if resultado == "POSITIVE":
        categoria = "Improdutivo"
        resposta = "Agradecemos a sua mensagem!"
    else:
        categoria = "Improdutivo"
        resposta = "Mensagem recebida. Obrigado pelo contato!"
    
    return categoria, resposta


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email_text = request.form["email_text"]
        categoria, resposta = classificar_email(email_text)
        return render_template("index.html", email=email_text, categoria=categoria, resposta=resposta)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
