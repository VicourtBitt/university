"""Servidor Flask: serve a página e expõe a API do chatbot."""
from flask import Flask, jsonify, render_template, request

from chatbot import Chatbot

app = Flask(__name__)
bot = Chatbot()


@app.get("/")
def index():
    return render_template("index.html", sugestoes=bot.sugestoes())


@app.post("/api/chat")
def chat():
    dados = request.get_json(silent=True) or {}
    mensagem = str(dados.get("mensagem", "")).strip()[:300]
    return jsonify(bot.responder(mensagem))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
