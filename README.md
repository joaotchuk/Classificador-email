📧 Classificador de E-mails

Aplicação web que utiliza Inteligência Artificial (Hugging Face API) para classificar e-mails como:

✅ Produtivo

⚠️ Improdutivo

❌ Erro

E sugere automaticamente uma resposta ao e-mail analisado.

🚀 Tecnologias

Python 3

Flask

Hugging Face Inference API

Bootstrap 5


▶️ Como rodar localmente

Clonar o repositório

git clone https://github.com/seu-usuario/Classificador-email.git
cd Classificador-email


Criar ambiente virtual (opcional, mas recomendado)

python -m venv venv
source venv/bin/activate    Linux/Mac
venv\Scripts\activate       Windows


Instalar dependências

pip install -r requirements.txt


Configurar Token da Hugging Face
No terminal:

export HF_TOKEN=seu_token_aqui      Linux/Mac
set HF_TOKEN=seu_token_aqui         Windows PowerShell

Obs: (Configure o Token do Hugging Face

Você precisa de um token válido para acessar a API:

Crie uma conta em huggingface.co

Vá em Settings > Access Tokens

Gere um token de leitura

Configure-o no terminal: )

Executar aplicação

python app.py


Acessar no navegador
👉 http://127.0.0.1:10000