import io
from typing import List, Dict, Any
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re

class EPUBExtractor:
    """Extrai capítulos estruturados de livros em formato EPUB."""

    def __init__(self, file_path_or_bytes):
        if isinstance(file_path_or_bytes, (bytes, io.BytesIO)):
            if isinstance(file_path_or_bytes, bytes):
                file_path_or_bytes = io.BytesIO(file_path_or_bytes)
            self.book = epub.read_epub(file_path_or_bytes)
        else:
            self.book = epub.read_epub(file_path_or_bytes)

    def clean_html(self, html_content: str) -> tuple[str, str]:
        """Extrai o título e o texto limpo do HTML do capítulo."""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Procura pelo primeiro cabeçalho (h1, h2, h3) para usar como título
        title = ""
        for heading in soup.find_all(['h1', 'h2', 'h3']):
            t = heading.get_text().strip()
            if t and len(t) < 100:
                title = t
                break

        # Remove elementos irrelevantes (scripts, estilos, rodapés de notas)
        for tag in soup(['script', 'style', 'nav', 'aside', 'footer']):
            tag.decompose()

        # Extrai parágrafos mantendo a fluidez da narração
        paragraphs = []
        for p in soup.find_all(['p', 'div', 'blockquote']):
            txt = p.get_text().strip()
            txt = re.sub(r'\s+', ' ', txt)
            if txt and len(txt) > 2:
                paragraphs.append(txt)

        text = "\n\n".join(paragraphs)
        return title, text

    def extract_chapters(self) -> List[Dict[str, Any]]:
        """Extrai todos os capítulos navegáveis do EPUB."""
        chapters = []
        chapter_idx = 1

        for item in self.book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content = item.get_content().decode('utf-8', errors='ignore')
            title, text = self.clean_html(content)

            # Filtra itens muito curtos (capa, folha de rosto, dedicatória curta de 3 palavras)
            words = text.split()
            if len(words) < 50:
                continue

            if not title:
                title = f"Capítulo {chapter_idx:02d}"

            chapters.append({
                "id": chapter_idx,
                "title": title,
                "text": text,
                "word_count": len(words)
            })
            chapter_idx += 1

        return chapters
