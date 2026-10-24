import os
import zipfile
from src.audio.audio_manager import AudioManager


def test_create_zip_package(tmp_path):
    output_dir = tmp_path / "output"
    book_dir = output_dir / "audiobooks" / "Livro_Teste"
    book_dir.mkdir(parents=True)

    file1 = book_dir / "01 - Capitulo 1.mp3"
    file1.write_text("conteudo falso 1")
    file2 = book_dir / "02 - Capitulo 2.mp3"
    file2.write_text("conteudo falso 2")

    manager = AudioManager(base_output_dir=str(output_dir))
    zip_path = manager.create_zip_package(str(book_dir), "livro_teste.zip")

    assert os.path.exists(zip_path)
    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        assert "01 - Capitulo 1.mp3" in namelist
        assert "02 - Capitulo 2.mp3" in namelist
