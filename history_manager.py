
from datetime import datetime
from modules.file_system import load_json, save_json


def add_to_history(tipo: str, entrada: str, saida: str):
    """Adiciona uma entrada ao histórico."""
    historico = load_json("historico")
    if not isinstance(historico, list):
        historico = []

    entry = {
        "tipo": tipo,          # "correcao" ou "moderacao"
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "entrada": entrada,
        "saida": saida,
    }
    historico.insert(0, entry)  # mais recente primeiro

    # Limita a 200 entradas
    if len(historico) > 200:
        historico = historico[:200]

    save_json("historico", historico)


def get_history() -> list:
    """Retorna o histórico completo."""
    data = load_json("historico")
    return data if isinstance(data, list) else []


def clear_history():
    """Limpa todo o histórico."""
    save_json("historico", [])
