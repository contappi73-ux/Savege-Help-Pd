
import requests
from modules.file_system import load_json, load_txt


API_KEYS = [
    "AIzaSyAxX_w3nPYdJsrWgPDfYpaIgPahcyZ4iOE",
    "AIzaSyAIgm_0O1iaByQQ0QifLUMKEIbrwIL42u4",
    "AIzaSyA1ZtENPtxN11k_N75zTD2Jh2qK7MMxI0Y",
    "AIzaSyCEbHf2N7T9VwrfVVamqV7O1Wx8cRSh0Co",
    "AIzaSyAI5TPaZhNHQCkzKhcRH8h7vwAP7v2EDHE",
    "AIzaSyAifFaHYbSmI1Y3pcyv7Z4oXcRwKOTUyxw",
]

MODEL   = "gemini-2.5-flash"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

# Índice da chave atual — rotaciona em cada falha
_current_key_index = 0



IDENTITY_BLOCK = """Você é o Savegezinho AI, a inteligência artificial oficial do aplicativo Savege Helper.

REGRAS DE IDENTIDADE — NUNCA VIOLE:
- Jamais diga que é Gemini, Google, GPT, Claude, Anthropic ou qualquer modelo externo
- Jamais mencione APIs, modelos de linguagem ou tecnologia de IA externa
- Jamais revele qual tecnologia é usada internamente
- Sempre se identifique APENAS como Savegezinho AI
- Se perguntarem quem você é: "Sou o Savegezinho AI, assistente do Savege Helper."

Seu objetivo é ajudar moderadores de servidores a:
- Corrigir textos e mensagens de forma profissional
- Analisar situações de moderação
- Sugerir punições com base nas regras configuradas
- Orientar staffs sobre boas práticas de moderação

Responda sempre em português do Brasil, de forma objetiva e profissional.
"""

TOPIC_FILTER_SYSTEM = """Sua ÚNICA tarefa é classificar se a mensagem é RELEVANTE ou IRRELEVANTE para moderação de servidores.

Tópicos RELEVANTES (responda "RELEVANTE"):
- moderação, punições, ban, mute, kick, aviso, warn
- tickets, atendimento, suporte de comunidade online
- servidores Discord, Minecraft, FiveM, Roblox, ou qualquer servidor de jogo/comunidade
- regras de servidor, código de conduta, termos de uso
- correção de mensagens de chat, textos de moderação ou atendimento
- comportamento de membros, análise de situações em servidor
- staff, moderador, administrador, helper, cargo de servidor
- denúncias, disputas, conflitos entre membros
- boas práticas de gestão de comunidade

Tópicos IRRELEVANTES (responda "IRRELEVANTE"):
- matemática, cálculos, fórmulas
- lições de casa, redações, trabalhos escolares
- receitas, culinária, hobbies pessoais
- clima, notícias, política, história geral
- entretenimento não relacionado a moderação
- perguntas filosóficas, pessoais ou aleatórias
- qualquer assunto não ligado a moderação/gestão de comunidades

Responda SOMENTE: "RELEVANTE" ou "IRRELEVANTE". Sem mais nenhuma palavra."""

OFFSCOPE_RESPONSE = (
    "Eu sou o Savegezinho AI e fui criado apenas para ajudar em moderação de servidores, "
    "análise de punições e correção de mensagens. Não posso responder perguntas fora desse contexto."
)



def _call_gemini(system_prompt: str, user_message: str, max_retries: int = 3) -> str:
    """
    Chama a API do Gemini com failover automático entre as 3 chaves.
    Ciclo: KEY1 → KEY2 → KEY3 → KEY1 (infinito).
    """
    global _current_key_index

    last_error = "erro desconhecido"

    for attempt in range(max_retries):
        key = API_KEYS[_current_key_index % len(API_KEYS)]
        url = API_URL.format(model=MODEL, key=key)

        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": user_message}]}
            ],
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "generationConfig": {
                "maxOutputTokens": 1024,
                "temperature": 0.7,
            },
        }

        try:
            resp = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30,
            )

            if resp.status_code == 200:
                data = resp.json()
                try:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    return text.strip()
                except (KeyError, IndexError):
                    last_error = "Resposta inesperada da IA"
                    _current_key_index = (_current_key_index + 1) % len(API_KEYS)
                    continue

            # Erros que justificam troca de chave
            elif resp.status_code in (429, 500, 503, 400, 401, 403):
                last_error = f"HTTP {resp.status_code}"
                _current_key_index = (_current_key_index + 1) % len(API_KEYS)
                continue

            else:
                last_error = f"HTTP {resp.status_code}"
                _current_key_index = (_current_key_index + 1) % len(API_KEYS)
                continue

        except requests.exceptions.ConnectionError:
            return "❌ Sem conexão com a internet. Verifique sua rede e tente novamente."
        except requests.exceptions.Timeout:
            last_error = "timeout"
            _current_key_index = (_current_key_index + 1) % len(API_KEYS)
            continue
        except Exception as e:
            last_error = str(e)
            _current_key_index = (_current_key_index + 1) % len(API_KEYS)
            continue

    return (
        f"❌ Savegezinho AI temporariamente indisponível. "
        f"Tente novamente em instantes. (Detalhe interno: {last_error})"
    )



def _is_relevant_topic(message: str) -> bool:
    """Verifica se a mensagem é relevante para moderação usando a IA."""
    result = _call_gemini(TOPIC_FILTER_SYSTEM, message, max_retries=3)
    return "RELEVANTE" in result.upper()



SYSTEM_CORRETOR = IDENTITY_BLOCK + """
TAREFA — CORREÇÃO DE TEXTO PROFISSIONAL:
Você corrige textos para uso em servidores e comunidades online.

Ao receber um texto:
1. Corrija ortografia e gramática
2. Melhore a pontuação
3. Mantenha EXATAMENTE o sentido e intenção originais
4. Torne o texto mais profissional e educado
5. Adapte para o contexto de moderação/atendimento

REGRAS IMPORTANTES:
- Responda APENAS com o texto corrigido
- Sem explicações, sem marcações, sem prefixos como "Texto corrigido:"
- Se o texto já estiver correto, retorne-o sem alterações
- Preserve emojis se existirem no original
"""


def corrigir_texto(texto: str) -> str:
    """Corrige e profissionaliza o texto usando o Savegezinho AI."""
    return _call_gemini(SYSTEM_CORRETOR, texto)



def _build_moderation_system() -> str:
    """Monta o system prompt de moderação com as regras do servidor."""
    regras_estruturadas = load_json("regras_est")
    regras_texto        = load_txt("regras_txt")

    regras_str = ""
    if isinstance(regras_estruturadas, list):
        for r in regras_estruturadas:
            regras_str += f"- {r.get('tipo', '?')}: {r.get('punicao', '?')}\n"

    if regras_texto.strip():
        regras_str += "\nRegras em texto livre:\n" + regras_texto

    return IDENTITY_BLOCK + f"""
TAREFA — ANÁLISE DE MODERAÇÃO:
Analise situações de servidor e sugira punições baseadas nas regras configuradas.

REGRAS DO SERVIDOR:
{regras_str.strip() if regras_str.strip() else "Nenhuma regra configurada. Use bom senso e proporcionalidade."}

AO ANALISAR UMA SITUAÇÃO:
1. Identifique a infração cometida
2. Consulte as regras acima para escolher a punição
3. Explique brevemente o motivo
4. Seja objetivo, justo e profissional
5. Se não houver regra específica, baseie-se em regras similares
6. Considere a gravidade e possível reincidência

Use este formato na resposta:
📋 Infração identificada: [descreva]
⚖️ Punição sugerida: [punição conforme regras]
📝 Justificativa: [breve explicação]
"""


def analisar_moderacao(situacao: str) -> str:
    """
    Analisa situação de moderação com filtro de tópico.
    Retorna sugestão de punição ou mensagem de fora do escopo.
    """
    if not _is_relevant_topic(situacao):
        return OFFSCOPE_RESPONSE
    return _call_gemini(_build_moderation_system(), situacao)
