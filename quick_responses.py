
from modules.file_system import load_json, save_json


def get_quick_responses() -> list:
    """Retorna a lista de respostas rápidas."""
    data = load_json("respostas")
    return data if isinstance(data, list) else []


def add_quick_response(titulo: str, texto: str):
    """Adiciona uma nova resposta rápida."""
    respostas = get_quick_responses()
    respostas.append({"titulo": titulo, "texto": texto})
    save_json("respostas", respostas)


def delete_quick_response(index: int):
    """Remove uma resposta rápida pelo índice."""
    respostas = get_quick_responses()
    if 0 <= index < len(respostas):
        respostas.pop(index)
        save_json("respostas", respostas)


def update_quick_response(index: int, titulo: str, texto: str):
    """Atualiza uma resposta rápida existente."""
    respostas = get_quick_responses()
    if 0 <= index < len(respostas):
        respostas[index] = {"titulo": titulo, "texto": texto}
        save_json("respostas", respostas)
