import re
from typing import List, Dict, Any
from pypdf import PdfReader

class PDFExtractor:
    """Extrai texto e capítulos de arquivos PDF com limpeza de artefatos de cabeçalho e rodapé."""

    def __init__(self, file_path_or_buffer):
        self.reader = PdfReader(file_path_or_buffer)
        self.num_pages = len(self.reader.pages)

    def clean_text(self, text: str) -> str:
        """Remove quebras de linha excessivas, números de página soltos e hifens de quebra de palavra."""
        if not text:
            return ""

        # Junta palavras separadas por hífen no fim da linha (ex: compu-\ntador -> computador)
        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)

        # Substitui quebras de linha únicas por espaços, mantendo quebras duplas (parágrafos)
        paragraphs = text.split("\n\n")
        cleaned_paragraphs = []
        for p in paragraphs:
            # Substitui quebras simples por espaço
            cleaned_p = re.sub(r'\s*\n\s*', ' ', p.strip())
            # Remove linhas que sejam apenas números (número de página)
            if re.fullmatch(r'\d+', cleaned_p):
                continue
            if cleaned_p:
                cleaned_paragraphs.append(cleaned_p)

        return "\n\n".join(cleaned_paragraphs)

    def extract_chapters(self, words_per_chunk: int = 2500) -> List[Dict[str, Any]]:
        """
        Extrai o conteúdo tentando identificar marcadores de capítulos,
        ou divide em partes confortáveis para ouvir durante treinos/corridas.
        """
        full_text_pages = []
        for idx, page in enumerate(self.reader.pages):
            raw = page.extract_text() or ""
            cleaned = self.clean_text(raw)
            if cleaned:
                full_text_pages.append((idx + 1, cleaned))

        if not full_text_pages:
            return []

        # Tentar detectar capítulos por padrões comuns (ex: Capítulo 1, Cap. 2, Chapter 3)
        chapter_regex = re.compile(
            r'^(?:Cap[íi]tulo|Chapter|Parte|Seção|PARTE|CAPÍTULO)\s+([0-9IVXLCDM]+|[A-Za-z]+)(?::| -|\.|\n|$)',
            re.IGNORECASE | re.MULTILINE
        )

        all_text = ""
        page_map = []
        for page_num, text in full_text_pages:
            start_pos = len(all_text)
            all_text += text + "\n\n"
            page_map.append((start_pos, page_num))

        matches = list(chapter_regex.finditer(all_text))

        chapters = []
        if len(matches) >= 2:
            # Detectou capítulos explícitos
            for i, match in enumerate(matches):
                start = match.start()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(all_text)
                chunk = all_text[start:end].strip()

                first_line = chunk.split("\n")[0].strip()
                title = first_line[:80]
                text = "\n".join(chunk.split("\n")[1:]).strip()

                if len(text) > 100:  # Ignora capítulos vazios ou sumários
                    chapters.append({
                        "id": len(chapters) + 1,
                        "title": title,
                        "text": text,
                        "word_count": len(text.split())
                    })

        # Se não encontrou capítulos estruturados ou se o PDF não tiver regex clara:
        if not chapters:
            current_words = []
            current_chapter = 1
            words = all_text.split()

            for i in range(0, len(words), words_per_chunk):
                chunk_words = words[i:i + words_per_chunk]
                text = " ".join(chunk_words)
                chapters.append({
                    "id": current_chapter,
                    "title": f"Parte {current_chapter:02d} (~{len(chunk_words)} palavras)",
                    "text": text,
                    "word_count": len(chunk_words)
                })
                current_chapter += 1

        return chapters
