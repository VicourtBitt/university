"""Lógica do chatbot: base de perguntas/respostas e busca da melhor correspondência."""
import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

CAMINHO_PADRAO = Path(__file__).parent / "data" / "respostas.json"
FALLBACK = "Desculpe, não entendi sua pergunta. Pode reformular?"
LIMIAR = 0.72  # similaridade mínima para aceitar uma correspondência


def normalizar(texto: str) -> str:
    """Minúsculas, sem acentos e sem pontuação, para comparar perguntas."""
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return " ".join(texto.split())


class Chatbot:
    def __init__(self, caminho: Path = CAMINHO_PADRAO):
        with open(caminho, encoding="utf-8") as f:
            self.base = json.load(f)
        # Índice plano: (pergunta normalizada, item da base)
        self.indice = [(normalizar(p), item) for item in self.base for p in item["perguntas"]]

    def sugestoes(self) -> list[str]:
        return [i["perguntas"][0] for i in self.base if i.get("sugerir")]

    def responder(self, mensagem: str) -> dict:
        m = normalizar(mensagem)
        if not m:
            return {"resposta": "Digite uma pergunta para começar.", "encerrar": False}

        melhor, melhor_score = None, 0.0
        for pergunta, item in self.indice:
            score = SequenceMatcher(None, pergunta, m).ratio()
            if len(m) >= 4 and (pergunta in m or m in pergunta):
                score = max(score, 0.9)
            if score > melhor_score:
                melhor, melhor_score = item, score

        if melhor and melhor_score >= LIMIAR:
            return {"resposta": melhor["resposta"], "encerrar": melhor.get("encerrar", False)}
        return {"resposta": FALLBACK, "encerrar": False}
