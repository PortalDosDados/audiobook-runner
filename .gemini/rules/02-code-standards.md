# 02 - Padrões de Código e Implementação

## Nomenclatura e Tipagem
- **Classes**: `PascalCase` (ex.: `PDFExtractor`, `EdgeTTSEngine`, `AudioManager`) [src/].
- **Métodos e Funções**: `snake_case` (ex.: `clean_text`, `extract_chapters`, `tag_mp3`) [src/].
- **Constantes**: `SCREAMING_SNAKE_CASE` (ex.: `AVAILABLE_VOICES`) [src/tts/edge_tts_engine.py].
- **Tipagem**: SEMPRE utilizar anotações de tipo do módulo `typing` para parâmetros e retornos de métodos públicos [src/extractors/pdf_extractor.py].

## Organização de Imports
- Seguir estritamente a ordem [OBSERVADO em app.py]:
  1. Biblioteca padrão (`os`, `io`, `re`, `asyncio`, `zipfile`, `typing`).
  2. Bibliotecas externas de terceiros (`streamlit`, `pypdf`, `ebooklib`, `bs4`, `mutagen`, `edge_tts`).
  3. Módulos internos do projeto (`from src.extractors...`).

## Tratamento de Erros e Exceções
- SEMPRE criar e utilizar exceções de domínio específicas em vez de capturar `Exception` genérica [DIRETRIZ aprovada pelo usuário]:
  - `ExtractionError`: para falhas na leitura ou decodificação de PDF/EPUB.
  - `TTSGenerationError`: para erros de conexão ou síntese com o edge-tts.
  - `AudioProcessingError`: para falhas ao gravar tags ID3 ou criar arquivo ZIP.
- NUNCA silenciar erros com blocos `except: pass` vazios [DIRETRIZ].
- SEMPRE informar ao usuário na UI via `st.error()` ou `st.warning()` quando uma exceção ocorrer [app.py].

## Anti-padrões Proibidos
- NUNCA executar chamadas bloqueantes de rede ou I/O pesado diretamente na thread principal do Streamlit sem controle de feedback (`st.spinner` ou barra de progresso) [app.py].
- NUNCA deixar caminhos absolutos hardcoded no código; usar `os.path.join` e caminhos relativos à raiz do projeto [src/audio/audio_manager.py].
- PREFIRA processamento assíncrono/concorrente para chamadas de rede no edge-tts [DIRETRIZ].
