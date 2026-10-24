import pytest
from unittest.mock import MagicMock, patch
from src.extractors.pdf_extractor import PDFExtractor


def test_clean_text_removes_hyphenation_and_page_numbers():
    with patch("src.extractors.pdf_extractor.PdfReader") as mock_reader:
        mock_reader.return_value.pages = []
        extractor = PDFExtractor(None)

        sample_raw = "Esta é uma pa-\nlavra dividida.\n\n42\n\nOutro parágrafo limpo."
        cleaned = extractor.clean_text(sample_raw)

        assert "palavra dividida." in cleaned
        assert "42" not in cleaned
        assert "Outro parágrafo limpo." in cleaned


def test_extract_chapters_fallback_chunking():
    with patch("src.extractors.pdf_extractor.PdfReader") as mock_reader:
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Texto corrido de teste para verificar a divisão em partes quando não há capítulos explícitos."
        mock_reader.return_value.pages = [mock_page]

        extractor = PDFExtractor(None)
        chapters = extractor.extract_chapters(words_per_chunk=5)

        assert len(chapters) > 1
        assert chapters[0]["id"] == 1
        assert "Parte 01" in chapters[0]["title"]
