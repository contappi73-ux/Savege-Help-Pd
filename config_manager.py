
import sys
import os
from modules.file_system import load_json, save_json


def get_config() -> dict:
    """Carrega configurações do app."""
    default = {
        "start_with_windows": False,
        "start_as_admin": False,
        "theme": "dark",
    }
    data = load_json("config")
    if isinstance(data, dict):
        
        data.pop("api_key", None)
        default.update(data)
    return default


def save_config(config: dict):
    """Salva configurações do app."""
    save_json("config", config)


def set_start_with_windows(enabled: bool):
    """Ativa ou desativa o início com o Windows via registro."""
    if sys.platform != "win32":
        return
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "SavegeHelperPD"
        exe_path = sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__)

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            if enabled:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{exe_path}"')
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                except FileNotFoundError:
                    pass
    except Exception as e:
        print(f"[Config] Erro ao modificar registro: {e}")


def request_admin_restart():
    """Reinicia o aplicativo como administrador no Windows."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()
    except Exception as e:
        print(f"[Config] Erro ao pedir privilégios: {e}")
