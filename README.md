# 🛡️ Savege Helper PD

Aplicativo desktop moderno para auxiliar moderadores e staffs na tomada de decisões, aprendizado e atendimento profissional.

---

## 📋 Requisitos

- Python 3.10 ou superior
- Windows 10/11 (recomendado)
- Conexão com internet (para funções de IA)

---

## 🚀 Instalação e Execução

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:
```bash
pip install PySide6 requests
```

### 2. Adicione as imagens (opcional)

Coloque os arquivos na pasta raiz do projeto (ao lado de `main.py`):
- `Savege.png` — Logo do aplicativo
- `App.ico` — Ícone da janela

Se não encontrados, o app usará emoji como fallback.

### 3. Execute o aplicativo

```bash
python main.py
```

---

## ⚙️ Configuração Inicial

1. Abra o app e vá em **Configurações** (ícone ⚙️ no menu lateral)
2. Insira sua **Chave de API da Anthropic** (obtenha em [console.anthropic.com](https://console.anthropic.com))
3. Clique em **Testar Conexão** para verificar
4. Clique em **Salvar Configurações**

---

## 📁 Arquivos do Sistema

O app cria automaticamente a pasta:
```
Documentos/config/
```

Arquivos gerados:
| Arquivo | Descrição |
|---------|-----------|
| `app_config.json` | Configurações do app (API key, etc.) |
| `historico.json` | Histórico de interações com a IA |
| `respostas_rapidas.json` | Respostas rápidas salvas |
| `regras_estruturadas.json` | Regras do servidor (tabela) |
| `regras_texto_livre.txt` | Regras em formato texto |

---

## 🔧 Funcionalidades

### ✍️ Correção de Texto
- Cole qualquer texto no chat
- A IA corrige ortografia, gramática e pontuação
- Mantém o sentido original
- Deixa o texto mais profissional

### 🛡️ Moderação IA
- Descreva uma situação de moderação
- A IA analisa baseada nas regras configuradas
- Sugere a punição mais adequada
- Gerencie as regras diretamente na tela

### 📚 Curso de Staff
- 6 módulos completos sobre moderação
- Aprenda do zero sobre tickets e punições
- Conteúdo com exemplos práticos

### 📋 Histórico
- Veja todas as interações anteriores
- Filtre por tipo (correção / moderação)
- Copie respostas antigas

### ⚡ Respostas Rápidas
- Crie respostas para situações comuns
- Clique direito para editar/excluir
- Copie ou use em um clique

---

## 🏗️ Estrutura do Projeto

```
savege_helper/
├── main.py                    # Ponto de entrada
├── requirements.txt           # Dependências
├── modules/
│   ├── ai_handler.py          # Chamadas à API de IA
│   ├── auto_update.py         # Atualização automática
│   ├── config_manager.py      # Configurações do sistema
│   ├── file_system.py         # Gerenciamento de arquivos
│   ├── history_manager.py     # Histórico
│   └── quick_responses.py     # Respostas rápidas
└── ui/
    ├── main_window.py         # Janela principal + sidebar
    ├── styles.py              # Tema visual QSS
    └── pages/
        ├── home_page.py       # Tela inicial
        ├── correction_page.py # Chat de correção
        ├── moderation_page.py # Chat de moderação + regras
        ├── course_page.py     # Curso de staff
        ├── history_page.py    # Histórico
        ├── quick_responses_page.py # Respostas rápidas
        └── settings_page.py   # Configurações
```

---

## 📦 Gerar Executável (.exe)

Para gerar um executável standalone:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=App.ico --add-data "Savege.png;." --name "SavegeHelperPD" main.py
```

O executável será gerado em `dist/SavegeHelperPD.exe`.

---

## ℹ️ Informações

- **Versão:** 1.0.0
- **Tecnologia:** Python + PySide6 (Qt6)
- **IA:** Anthropic Claude (API)
- **Desenvolvido por:** Savege Team
