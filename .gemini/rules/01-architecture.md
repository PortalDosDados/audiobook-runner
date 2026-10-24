# 01 - Arquitetura e Fronteiras de Camadas

## Mapa de Diretórios
- `/app.py`: Camada de apresentação e orquestração de UI com Streamlit [app.py].
- `/src/extractors/`: Camada de extração e limpeza de textos (`pdf_extractor.py`, `epub_extractor.py`) [src/extractors/].
- `/src/tts/`: Camada de síntese de fala e abstração do provedor TTS (`edge_tts_engine.py`) [src/tts/].
- `/src/audio/`: Camada de gerenciamento de arquivos de áudio, tags ID3 e empacotamento ZIP (`audio_manager.py`) [src/audio/].
- `/output/`: Armazenamento de arquivos de áudio gerados e pacotes `.zip` [app.py], [.gitignore].

## Responsabilidades e Acoplamento
- **Camada de Apresentação (`app.py`)**:
  - SEMPRE usar `st.session_state` para persistência temporária de capítulos e caminhos de áudio [app.py].
  - NUNCA colocar regras de parsing de binários (PDF/EPUB) diretamente no `app.py` [DIRETRIZ].
- **Camada de Extração (`src/extractors/`)**:
  - SEMPRE retornar estruturas padronizadas `List[Dict[str, Any]]` com `id`, `title`, `text`, `word_count` [src/extractors/pdf_extractor.py].
  - NUNCA importar `streamlit` em arquivos dentro de `src/` [DIRETRIZ].
- **Camada de Síntese (`src/tts/`)**:
  - SEMPRE encapsular lógica assíncrona do `edge_tts` permitindo chamadas síncronas e concorrentes [src/tts/edge_tts_engine.py].
  - NUNCA acoplar a engine de TTS a caminhos fixos de UI [DIRETRIZ].
- **Camada de Áudio (`src/audio/`)**:
  - SEMPRE aplicar tags ID3 em MP3 para suportar players de smartwatch e mobile [src/audio/audio_manager.py].
  - SEMPRE validar se o diretório de destino existe antes de gravar [src/audio/audio_manager.py].

## Regras de Importação
- Fluxo unidirecional obrigatório: `app.py` -> `src/*` [OBSERVADO em app.py].
- NUNCA permitir dependências circulares entre submódulos de `src/` [DIRETRIZ].
- NUNCA importar `src/extractors` dentro de `src/tts` ou vice-versa [DIRETRIZ].
