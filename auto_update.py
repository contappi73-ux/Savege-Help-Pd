
import os
import sys
import subprocess
import requests
import json

CURRENT_VERSION = "1.1.0"
VERSION_URL   = "https://raw.githubusercontent.com/contappi73-ux/meu-app-updates/refs/heads/main/version.json"
CHANGELOG_URL = "https://raw.githubusercontent.com/contappi73-ux/meu-app-updates/refs/heads/main/changelog.txt"


def _parse_version(v: str):
    """Converte string de versão em tupla comparável."""
    try:
        return tuple(int(x) for x in v.strip().split("."))
    except Exception:
        return (0,)


def check_for_update() -> dict | None:
   
    try:
        resp = requests.get(VERSION_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        online_version = data.get("version", "0.0.0")
        download_url   = data.get("download_url", "")  # usado internamente, não exibido

        if _parse_version(online_version) > _parse_version(CURRENT_VERSION):
            # Busca changelog
            try:
                cr = requests.get(CHANGELOG_URL, timeout=10)
                changelog = cr.text if cr.ok else "Sem informações sobre as novidades."
            except Exception:
                changelog = "Sem informações sobre as novidades."

            return {
                "version":      online_version,
                "download_url": download_url,   # interno  não exibir
                "changelog":    changelog,
            }
    except Exception:
        pass
    return None


def download_and_install(download_url: str, parent_widget=None):
    
    if not getattr(sys, "frozen", False):
        print("[Update] Não está em modo executável. Atualização ignorada.")
        return

    try:
        exe_path = sys.executable
        tmp_path = exe_path + ".tmp"

        resp = requests.get(download_url, stream=True, timeout=60)
        resp.raise_for_status()

        with open(tmp_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        # Script batch para substituir o executável e reiniciar
        bat_path = os.path.join(os.path.dirname(exe_path), "_update.bat")
        bat_content = f"""@echo off
timeout /t 2 /nobreak > nul
move /y "{tmp_path}" "{exe_path}"
start "" "{exe_path}"
del "%~f0"
"""
        with open(bat_path, "w") as f:
            f.write(bat_content)

        subprocess.Popen(bat_path, shell=True)
        sys.exit(0)

    except Exception as e:
        print(f"[Update] Erro ao atualizar: {e}")
        if parent_widget:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(parent_widget, "Erro", f"Falha ao baixar atualização:\n{e}")
