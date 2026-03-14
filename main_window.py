
import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget,
    QSizePolicy, QMessageBox, QDialog, QTextEdit,
    QDialogButtonBox, QProgressBar, QApplication
)
from PySide6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QTimer,
    QThread, Signal, QParallelAnimationGroup, QSize
)
from PySide6.QtGui import QPixmap, QFont, QIcon

from ui.styles import MAIN_STYLE, COLORS
from modules.file_system import get_asset_path

# Importa todas as páginas
from ui.pages.home_page          import HomePage
from ui.pages.correction_page    import CorrectionPage
from ui.pages.moderation_page    import ModerationPage
from ui.pages.course_page        import CoursePage
from ui.pages.history_page       import HistoryPage
from ui.pages.settings_page      import SettingsPage
from ui.pages.quick_responses_page import QuickResponsesWidget


# verificar att
class UpdateCheckThread(QThread):
    update_found    = Signal(dict)
    no_update       = Signal()
    check_error     = Signal(str)

    def run(self):
        try:
            from modules.auto_update import check_for_update
            result = check_for_update()
            if result:
                self.update_found.emit(result)
            else:
                self.no_update.emit()
        except Exception as e:
            self.check_error.emit(str(e))


# dialog att
class UpdateDialog(QDialog):
    def __init__(self, info: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nova Atualização Disponível!")
        self.setFixedSize(500, 400)
        self.setStyleSheet(f"background: {COLORS['bg']}; color: {COLORS['text']};")
        self._info = info

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(16)

        # Cabeçalho 
        header_row = QHBoxLayout()
        icon_lbl = QLabel("🎉")
        icon_lbl.setStyleSheet("font-size: 32px;")
        header_row.addWidget(icon_lbl)

        header_text = QVBoxLayout()
        title_lbl = QLabel("Nova versão disponível!")
        title_lbl.setStyleSheet(f"font-size: 17px; font-weight: 800; color: {COLORS['accent2']};")
        header_text.addWidget(title_lbl)

        ver_lbl = QLabel(f"Savege Helper PD  →  v{info['version']}")
        ver_lbl.setStyleSheet(f"font-size: 13px; color: {COLORS['text2']};")
        header_text.addWidget(ver_lbl)
        header_row.addLayout(header_text)
        header_row.addStretch()
        layout.addLayout(header_row)

        # Separador 
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {COLORS['border']};")
        layout.addWidget(sep)

        #  O que há de novo
        news_lbl = QLabel("📋  O que há de novo nesta versão:")
        news_lbl.setStyleSheet(f"color: {COLORS['text']}; font-size: 13px; font-weight: 600;")
        layout.addWidget(news_lbl)

        changelog = QTextEdit()
        changelog.setReadOnly(True)
        changelog.setPlainText(info.get("changelog", "Sem informações sobre as novidades."))
        changelog.setStyleSheet(f"""
            QTextEdit {{
                background: {COLORS['card2']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
                color: {COLORS['text']};
                padding: 12px;
                font-size: 13px;
            }}
        """)
        layout.addWidget(changelog, stretch=1)

        # Progress bar 
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setRange(0, 0)
        self.progress.setFixedHeight(8)
        self.progress.setStyleSheet(f"""
            QProgressBar {{ background: {COLORS['card2']}; border-radius: 4px; border: none; }}
            QProgressBar::chunk {{ background: {COLORS['accent']}; border-radius: 4px; }}
        """)
        layout.addWidget(self.progress)

        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet(f"color: {COLORS['text2']}; font-size: 11px;")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_lbl)

        # Botões 
        btns = QHBoxLayout()
        btns.setSpacing(12)

        btn_later = QPushButton("Atualizar Depois")
        btn_later.setProperty("class", "secondary")
        btn_later.setFixedHeight(38)
        btn_later.clicked.connect(self.reject)
        btns.addWidget(btn_later)

        btns.addStretch()

        self.btn_update = QPushButton("⬆️  Atualizar Agora")
        self.btn_update.setFixedHeight(38)
        self.btn_update.setFixedWidth(170)
        self.btn_update.clicked.connect(self._do_update)
        btns.addWidget(self.btn_update)

        layout.addLayout(btns)

    def _do_update(self):
        url = self._info.get("download_url", "")
        if not url:
            QMessageBox.information(
                self, "Atualização",
                "A atualização será aplicada automaticamente na próxima inicialização."
            )
            return

        self.btn_update.setEnabled(False)
        self.progress.setVisible(True)
        self.status_lbl.setText("⬇️  Baixando atualização...")

        from modules.auto_update import download_and_install
        download_and_install(url, self)


class NavButton(QPushButton):
    def __init__(self, icon: str, text: str, parent=None):
        super().__init__(f"  {icon}   {text}", parent)
        self.setObjectName("nav_btn")
        self.setMinimumHeight(44)
        self.setCheckable(False)
        self._active = False
        self.setProperty("active", "false")

    def set_active(self, active: bool):
        self._active = active
        self.setProperty("active", "true" if active else "false")
        self.style().unpolish(self)
        self.style().polish(self)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Savege Helper PD")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 780)

        # Ícone do aplicativo
        icon_path = get_asset_path("App.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Aplica estilo global
        self.setStyleSheet(MAIN_STYLE)

        self._current_index = 0
        self._nav_buttons: list[NavButton] = []
        self._update_thread = None

        self._build_ui()
        self._check_updates()


    def _build_ui(self):
        central = QWidget()
        central.setStyleSheet(f"background: {COLORS['bg']};")
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar 
        sidebar = self._build_sidebar()
        root.addWidget(sidebar)

        # Content 
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background: {COLORS['bg']};")

        self._pages = [
            HomePage(),
            CorrectionPage(),
            ModerationPage(),
            CoursePage(),
            HistoryPage(),
            QuickResponsesWidget(),
            SettingsPage(),
        ]
        for page in self._pages:
            self.stack.addWidget(page)

        root.addWidget(self.stack, stretch=1)

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(4)

        # Logo
        logo_frame = QFrame()
        logo_frame.setStyleSheet(
            f"background: {COLORS['card2']}; border-radius: 12px; padding: 8px;"
        )
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(8, 10, 8, 10)
        logo_layout.setSpacing(4)

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        logo_path = get_asset_path("Savege.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaledToWidth(120, Qt.SmoothTransformation)
            logo_label.setPixmap(pix)
        else:
            logo_label.setText("🛡️")
            logo_label.setStyleSheet("font-size: 40px;")
        logo_layout.addWidget(logo_label)

        app_name = QLabel("Savege Helper")
        app_name.setAlignment(Qt.AlignCenter)
        app_name.setStyleSheet(f"color: {COLORS['accent2']}; font-size: 12px; font-weight: 700;")
        logo_layout.addWidget(app_name)

        layout.addWidget(logo_frame)
        layout.addSpacing(16)

        # Nav items: (icon, label, page_index)
        nav_items = [
            ("🏠", "Início",           0),
            ("✍️", "Correção de Texto", 1),
            ("🛡️", "Moderação IA",     2),
            ("📚", "Curso de Staff",   3),
            ("📋", "Histórico",        4),
            ("⚡", "Respostas Rápidas",5),
            ("⚙️", "Configurações",    6),
        ]

        for icon, label, idx in nav_items:
            btn = NavButton(icon, label)
            btn.clicked.connect(lambda checked, i=idx: self._navigate(i))
            self._nav_buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        # Versão
        ver_label = QLabel("v1.1.0")
        ver_label.setAlignment(Qt.AlignCenter)
        ver_label.setStyleSheet(f"color: {COLORS['text2']}; font-size: 11px;")
        layout.addWidget(ver_label)

        # Seleciona o primeiro botão
        self._nav_buttons[0].set_active(True)

        return sidebar

    #  Navegaçao

    def _navigate(self, index: int):
        if index == self._current_index:
            return

        # Atualiza botões
        for i, btn in enumerate(self._nav_buttons):
            btn.set_active(i == index)

        
        self._current_index = index

        # Refresca histórico ao entrar na página
        if index == 4 and hasattr(self._pages[4], "refresh"):
            self._pages[4].refresh()

        self.stack.setCurrentIndex(index)

    # Update Check 

    def _check_updates(self):
        """Verifica atualizações em background."""
        self._update_thread = UpdateCheckThread()
        self._update_thread.update_found.connect(self._on_update_found)
        self._update_thread.start()

    def _on_update_found(self, info: dict):
        QTimer.singleShot(1500, lambda: self._show_update_dialog(info))

    def _show_update_dialog(self, info: dict):
        dlg = UpdateDialog(info, self)
        dlg.exec()
