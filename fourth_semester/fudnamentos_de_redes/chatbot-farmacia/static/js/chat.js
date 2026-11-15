const mensagens = document.getElementById("mensagens");
const form = document.getElementById("form");
const entrada = document.getElementById("entrada");
const enviar = document.getElementById("enviar");
const sugestoes = document.getElementById("sugestoes");

const CLASSE_USUARIO = "ml-auto max-w-[85%] rounded-2xl rounded-br-sm bg-pinho px-4 py-3 text-white";
const CLASSE_BOT = "max-w-[85%] rounded-2xl rounded-bl-sm border-l-4 border-rotulo bg-giz px-4 py-3";

function adicionar(texto, classe) {
  const div = document.createElement("div");
  div.className = classe;
  div.textContent = texto; // textContent evita injeção de HTML
  mensagens.appendChild(div);
  mensagens.scrollTop = mensagens.scrollHeight;
  return div;
}

function bloquear(estado) {
  entrada.disabled = estado;
  enviar.disabled = estado;
}

async function enviarMensagem(texto) {
  texto = texto.trim();
  if (!texto) return;

  adicionar(texto, CLASSE_USUARIO);
  entrada.value = "";
  bloquear(true);
  const digitando = adicionar("Digitando...", CLASSE_BOT + " text-tinta/60");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensagem: texto }),
    });
    const dados = await res.json();
    digitando.remove();
    adicionar(dados.resposta, CLASSE_BOT);
    if (dados.encerrar) return encerrarConversa();
  } catch {
    digitando.remove();
    adicionar("Não consegui falar com o servidor. Verifique se ele está rodando e tente de novo.", CLASSE_BOT);
  }
  bloquear(false);
  entrada.focus();
}

function encerrarConversa() {
  sugestoes.classList.add("hidden");
  const botao = document.createElement("button");
  botao.textContent = "Iniciar nova conversa";
  botao.className = "rounded-xl bg-rotulo px-4 py-2 font-semibold text-tinta hover:brightness-95";
  botao.onclick = () => location.reload();
  mensagens.appendChild(botao);
  mensagens.scrollTop = mensagens.scrollHeight;
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  enviarMensagem(entrada.value);
});

sugestoes.addEventListener("click", (e) => {
  const botao = e.target.closest("[data-sugestao]");
  if (botao && !entrada.disabled) enviarMensagem(botao.dataset.sugestao);
});

entrada.focus();
