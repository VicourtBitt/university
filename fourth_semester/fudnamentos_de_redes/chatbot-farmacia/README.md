# Chatbot Farmácia Vida

Chatbot simples (Flask + Tailwind CSS) que responde perguntas pré-cadastradas.
Cliente (navegador) e servidor (bot) se comunicam por HTTP/JSON, de forma síncrona.

## Como rodar
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Acesse http://localhost:5000

## Estrutura
- `app.py` – servidor Flask (rotas `/` e `POST /api/chat`)
- `chatbot.py` – lógica de busca da resposta (normalização + similaridade)
- `data/respostas.json` – perguntas e respostas cadastradas (edite para adicionar novas)
- `templates/index.html` – interface (Tailwind via CDN)
- `static/js/chat.js` – envio das mensagens ao servidor

Se a pergunta não for reconhecida, o bot responde: "Desculpe, não entendi sua pergunta. Pode reformular?".
Ao enviar "Sair", o bot se despede e a conversa é encerrada.
