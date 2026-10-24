# 00 - Visão Geral do Projeto

## Escopo
- Aplicação local para extração de texto de PDF/EPUB e conversão em audiobook com capítulos e tags ID3 para treinos/corrida [README.md].

## Stack Tecnológica
- **Runtime**: Python 3.11+ [OBSERVADO no ambiente local].
- **UI Framework**: Streamlit >= 1.35.0 [requirements.txt].
- **TTS Engine**: edge-tts >= 6.1.12 (vozes neurais gratuitas da Microsoft) [requirements.txt].
- **Extratores**: pypdf >= 4.2.0 [requirements.txt], ebooklib >= 0.18 [requirements.txt], beautifulsoup4 >= 4.12.0 [requirements.txt].
- **Áudio / Metadados**: mutagen >= 1.47.0 [requirements.txt].
- **Testes**: pytest [DIRETRIZ aprovada pelo usuário].

## Comandos Fundamentais
- **Instalação**:
  ```bash
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```
  *Fonte: [README.md]*
- **Execução Local**:
  ```bash
  streamlit run app.py
  ```
  *Fonte: [README.md]*
- **Testes Automatizados**:
  ```bash
  pytest
  ```
  *Fonte: [DIRETRIZ]*

## Regras Globais
- SEMPRE executar a aplicação via `streamlit run app.py` [README.md].
- NUNCA adicionar dependências em `requirements.txt` sem necessidade comprovada [DIRETRIZ].
- SEMPRE manter arquivos de áudio restritos a `output/` [app.py], [.gitignore].
