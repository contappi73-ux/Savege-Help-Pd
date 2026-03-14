"""
Estilos QSS do Savege Helper — tema escuro moderno.
"""

# Cores principais
C_BG        = "#0f0f17"   
C_PANEL     = "#16161f"   
C_CARD      = "#1e1e2e"  
C_CARD2     = "#252535"   
C_BORDER    = "#2a2a3d"   
C_ACCENT    = "#7c3aed"   
C_ACCENT2   = "#9d5cf5"  
C_ACCENT3   = "#5b21b6"   
C_TEXT      = "#e2e2f0"  
C_TEXT2     = "#9090b0"   
C_SUCCESS   = "#22c55e"   
C_WARNING   = "#f59e0b"   
C_DANGER    = "#ef4444"   
C_INPUT_BG  = "#1a1a2e"   


MAIN_STYLE = f"""
/* ═══════════════════════════════════
   GERAL
═══════════════════════════════════ */

QMainWindow, QDialog {{
    background-color: {C_BG};
    color: {C_TEXT};
}}

QWidget {{
    background-color: transparent;
    color: {C_TEXT};
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}}

/* ═══════════════════════════════════
   SCROLLBARS
═══════════════════════════════════ */

QScrollBar:vertical {{
    background: {C_PANEL};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {C_BORDER};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{ background: {C_ACCENT}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

QScrollBar:horizontal {{
    background: {C_PANEL};
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: {C_BORDER};
    border-radius: 4px;
    min-width: 30px;
}}
QScrollBar::handle:horizontal:hover {{ background: {C_ACCENT}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}

/* ═══════════════════════════════════
   INPUTS
═══════════════════════════════════ */

QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {C_INPUT_BG};
    border: 1.5px solid {C_BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    color: {C_TEXT};
    selection-background-color: {C_ACCENT};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {C_ACCENT};
}}

/* ═══════════════════════════════════
   BOTÕES PADRÃO
═══════════════════════════════════ */

QPushButton {{
    background-color: {C_ACCENT};
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    font-size: 13px;
}}
QPushButton:hover {{
    background-color: {C_ACCENT2};
}}
QPushButton:pressed {{
    background-color: {C_ACCENT3};
    padding-top: 9px;
    padding-bottom: 7px;
}}
QPushButton:disabled {{
    background-color: {C_BORDER};
    color: {C_TEXT2};
}}

/* ═══════════════════════════════════
   BOTÃO SECUNDÁRIO
═══════════════════════════════════ */

QPushButton[class="secondary"] {{
    background-color: {C_CARD2};
    color: {C_TEXT};
    border: 1.5px solid {C_BORDER};
}}
QPushButton[class="secondary"]:hover {{
    border-color: {C_ACCENT};
    color: {C_ACCENT2};
}}
QPushButton[class="secondary"]:pressed {{
    background-color: {C_CARD};
}}

/* ═══════════════════════════════════
   BOTÃO DANGER
═══════════════════════════════════ */

QPushButton[class="danger"] {{
    background-color: {C_DANGER};
    color: #ffffff;
}}
QPushButton[class="danger"]:hover {{
    background-color: #f87171;
}}
QPushButton[class="danger"]:pressed {{
    background-color: #dc2626;
}}

/* ═══════════════════════════════════
   BOTÃO SUCCESS
═══════════════════════════════════ */

QPushButton[class="success"] {{
    background-color: {C_SUCCESS};
    color: #ffffff;
}}
QPushButton[class="success"]:hover {{
    background-color: #4ade80;
}}

/* ═══════════════════════════════════
   SIDEBAR
═══════════════════════════════════ */

#sidebar {{
    background-color: {C_PANEL};
    border-right: 1px solid {C_BORDER};
    min-width: 220px;
    max-width: 220px;
}}

#nav_btn {{
    background-color: transparent;
    color: {C_TEXT2};
    border: none;
    border-radius: 10px;
    padding: 12px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
}}
#nav_btn:hover {{
    background-color: {C_CARD};
    color: {C_TEXT};
}}
#nav_btn[active="true"] {{
    background-color: {C_ACCENT};
    color: #ffffff;
    font-weight: 700;
}}
#nav_btn[active="true"]:hover {{
    background-color: {C_ACCENT2};
}}

/* ═══════════════════════════════════
   CARDS
═══════════════════════════════════ */

#card {{
    background-color: {C_CARD};
    border: 1px solid {C_BORDER};
    border-radius: 12px;
    padding: 16px;
}}

#card_header {{
    background-color: {C_CARD2};
    border-radius: 8px;
    padding: 10px 14px;
}}

/* ═══════════════════════════════════
   LABELS
═══════════════════════════════════ */

#title {{
    font-size: 22px;
    font-weight: 700;
    color: {C_TEXT};
}}
#subtitle {{
    font-size: 15px;
    font-weight: 600;
    color: {C_ACCENT2};
}}
#label_muted {{
    color: {C_TEXT2};
    font-size: 12px;
}}

/* ═══════════════════════════════════
   CHAT BUBBLES
═══════════════════════════════════ */

#bubble_user {{
    background-color: {C_ACCENT};
    border-radius: 12px;
    padding: 10px 14px;
    color: #ffffff;
}}
#bubble_ai {{
    background-color: {C_CARD2};
    border-radius: 12px;
    padding: 10px 14px;
    color: {C_TEXT};
    border: 1px solid {C_BORDER};
}}

/* ═══════════════════════════════════
   TABELA / LISTA
═══════════════════════════════════ */

QListWidget {{
    background-color: {C_CARD};
    border: 1px solid {C_BORDER};
    border-radius: 10px;
    padding: 4px;
}}
QListWidget::item {{
    background-color: {C_CARD2};
    border-radius: 8px;
    padding: 10px;
    margin: 3px;
    color: {C_TEXT};
}}
QListWidget::item:selected {{
    background-color: {C_ACCENT};
    color: #ffffff;
}}
QListWidget::item:hover {{
    background-color: {C_BORDER};
}}

QTableWidget {{
    background-color: {C_CARD};
    border: 1px solid {C_BORDER};
    border-radius: 10px;
    gridline-color: {C_BORDER};
}}
QTableWidget::item {{
    padding: 8px;
    color: {C_TEXT};
}}
QTableWidget::item:selected {{
    background-color: {C_ACCENT};
}}
QHeaderView::section {{
    background-color: {C_CARD2};
    color: {C_TEXT2};
    padding: 8px;
    border: none;
    border-bottom: 1px solid {C_BORDER};
    font-weight: 600;
}}

/* ═══════════════════════════════════
   COMBO BOX
═══════════════════════════════════ */

QComboBox {{
    background-color: {C_INPUT_BG};
    border: 1.5px solid {C_BORDER};
    border-radius: 8px;
    padding: 6px 12px;
    color: {C_TEXT};
}}
QComboBox:focus {{
    border-color: {C_ACCENT};
}}
QComboBox QAbstractItemView {{
    background-color: {C_CARD2};
    border: 1px solid {C_BORDER};
    selection-background-color: {C_ACCENT};
    color: {C_TEXT};
}}

/* ═══════════════════════════════════
   CHECKBOX / TOGGLE
═══════════════════════════════════ */

QCheckBox {{
    color: {C_TEXT};
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {C_BORDER};
    border-radius: 4px;
    background-color: {C_INPUT_BG};
}}
QCheckBox::indicator:checked {{
    background-color: {C_ACCENT};
    border-color: {C_ACCENT};
}}

/* ═══════════════════════════════════
   SEPARADOR
═══════════════════════════════════ */

QFrame[frameShape="4"], QFrame[frameShape="5"] {{
    color: {C_BORDER};
}}

/* ═══════════════════════════════════
   TOOLTIP
═══════════════════════════════════ */

QToolTip {{
    background-color: {C_CARD2};
    color: {C_TEXT};
    border: 1px solid {C_BORDER};
    border-radius: 6px;
    padding: 6px 10px;
}}

/* ═══════════════════════════════════
   STACKED WIDGET / PAGES
═══════════════════════════════════ */

QStackedWidget {{
    background-color: {C_BG};
}}
"""


COLORS = {
    "bg": C_BG,
    "panel": C_PANEL,
    "card": C_CARD,
    "card2": C_CARD2,
    "border": C_BORDER,
    "accent": C_ACCENT,
    "accent2": C_ACCENT2,
    "accent3": C_ACCENT3,
    "text": C_TEXT,
    "text2": C_TEXT2,
    "success": C_SUCCESS,
    "warning": C_WARNING,
    "danger": C_DANGER,
    "input_bg": C_INPUT_BG,
}
