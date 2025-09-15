# 📧 Classificador de E-mails  

Aplicação web que utiliza **Inteligência Artificial** (Hugging Face API) para classificar e-mails como:  

- ✅ **Produtivo**  
- ⚠️ **Improdutivo**  
- ❌ **Erro**  

Além disso, o sistema sugere automaticamente uma resposta ao e-mail analisado.  

Acesse via web https://classificador-email-8t1f.onrender.com/

---

## 🚀 Tecnologias Utilizadas
- 🐍 **Python 3**  
- 🌐 **Flask**  
- 🤗 **Hugging Face Inference API**  
- 🎨 **Bootstrap 5**  

---

## ▶️ Como rodar localmente  

### 1. 📂 Clonar o repositório

Bash

git clone https://github.com/seu-usuario/Classificador-email.git

cd Classificador-email

### 2 Criar ambiente virtual (opcional, mas recomendado)

python -m venv venv
source venv/bin/activate     Linux/Mac

venv\Scripts\activate        Windows


### 3 Instalar dependências

pip install -r requirements.txt


### 4 Configurar Token da Hugging Face
No terminal:

export HF_TOKEN=seu_token_aqui       Linux/Mac

set HF_TOKEN=seu_token_aqui          Windows PowerShell

'''Obs: (Configure o Token do Hugging Face

Você precisa de um token válido para acessar a API:

Crie uma conta em huggingface.co

Vá em Settings > Access Tokens

Gere um token de leitura

Configure-o no terminal: )'''

### 5 Executar aplicação

python app.py


Acessar no navegador
👉 http://127.0.0.1:10000
