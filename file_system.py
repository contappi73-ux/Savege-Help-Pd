
import os
import json
import ctypes
import sys
import shutil

# Diretório base de configuração (Documents/config)
CONFIG_DIR = os.path.join(os.path.expanduser("~"), "Documents", "config")

# Mapeamento de arquivos
ARQUIVOS = {
    "respostas": "respostas_rapidas.json",
    "historico":  "historico.json",
    "regras_est": "regras_estruturadas.json",
    "regras_txt": "regras_texto_livre.txt",
    "config":     "app_config.json",
}


def get_path(chave: str) -> str:
    """Retorna o caminho completo de um arquivo pelo nome da chave."""
    return os.path.join(CONFIG_DIR, ARQUIVOS[chave])


def get_asset_path(filename: str) -> str:
    """Retorna o caminho para assets — procura em múltiplos locais."""
    try:
        from modules.asset_helper import get_bundled_asset
        return get_bundled_asset(filename)
    except ImportError:
        # Fallback se asset_helper não existir
        pass
    
    # Tenta diretórios padrão
    local = os.path.join(CONFIG_DIR, filename)
    if os.path.exists(local):
        return local
    
    # Procura na pasta do executável ou script
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base, filename)


def _hide_folder_windows(path: str):
    """Marca pasta como oculta no Windows."""
    try:
        if sys.platform == "win32":
            ctypes.windll.kernel32.SetFileAttributesW(path, 0x02)
    except Exception:
        pass


def _create_default_json(path: str, default):
    """Cria arquivo JSON com valor padrão se não existir."""
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=2)


def _create_default_txt(path: str, default: str = ""):
    """Cria arquivo de texto com conteúdo padrão se não existir."""
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(default)


def init_file_system():
    """Inicializa o sistema de arquivos do aplicativo."""
    # Cria a pasta config se não existir
    os.makedirs(CONFIG_DIR, exist_ok=True)
    _hide_folder_windows(CONFIG_DIR)

    # Respostas rápidas
    _create_default_json(get_path("respostas"), [])

    # Histórico
    _create_default_json(get_path("historico"), [])

    # Regras estruturadas
    default_regras = [
        {"tipo": "insulto leve",  "punicao": "aviso"},
        {"tipo": "insulto grave", "punicao": "mute 24h"},
        {"tipo": "spam",          "punicao": "mute 1 hora"},
        {"tipo": "racismo",       "punicao": "ban permanente"},
    ]
    _create_default_json(get_path("regras_est"), default_regras)

    # Regras em texto livre
    _create_default_txt(
        get_path("regras_txt"),
        "Insulto leve: aviso verbal\nInsulto grave: mute de 24 horas\nSpam: mute de 1 hora\nRacismo: ban permanente\n"
    )

    # Config do app
    default_config = {
        "start_with_windows": False,
        "start_as_admin": False,
        "theme": "dark",
    }
    _create_default_json(get_path("config"), default_config)



def load_json(chave: str):
    try:
        with open(get_path(chave), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return [] if chave in ("respostas", "historico") else {}


def save_json(chave: str, data):
    with open(get_path(chave), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_txt(chave: str) -> str:
    try:
        with open(get_path(chave), "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def save_txt(chave: str, text: str):
    with open(get_path(chave), "w", encoding="utf-8") as f:
        f.write(text)
