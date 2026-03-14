
import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QFont, QIcon

from modules.file_system import init_file_system, get_asset_path
from modules.config_manager import get_config, request_admin_restart
from ui.main_window import MainWindow


def main():
    # ── Inicializa sistema de arquivos ──
    init_file_system()

    # ── Verifica se precisa reiniciar como admin ──
    config = get_config()
    if config.get("start_as_admin") and sys.platform == "win32":
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                request_admin_restart()
                return
        except Exception:
            pass

    # Cria aplicação Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Savege Helper PD")
    app.setApplicationVersion("1.1.0")
    app.setOrganizationName("Savege Team")

    # Ativa suporte a DPI alto
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Fonte padrão
    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.PreferNoHinting)
    app.setFont(font)

    # Ícone da aplicação
    icon_path = get_asset_path("App.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Cria e exibe janela principal
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
