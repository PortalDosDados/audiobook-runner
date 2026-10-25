import os
import zipfile
import pytest
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from src.audio.audio_manager import AudioManager, AudioProcessingError


def create_mock_mp3_frame(num_frames: int = 5) -> bytes:
    """Gera frames MPEG1 Layer III válidos (128kbps, 44.1kHz, Joint Stereo = 417 bytes por frame)."""
    frame = b"\xff\xfb\x90\x64" + b"\x00" * 413
    return frame * num_frames


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


def test_tag_mp3(tmp_path):
    file_path = str(tmp_path / "test_tag.mp3")
    with open(file_path, "wb") as f:
        f.write(create_mock_mp3_frame(2))

    manager = AudioManager(base_output_dir=str(tmp_path))
    manager.tag_mp3(
        file_path=file_path,
        title="Capítulo Único",
        book_title="Meu Livro",
        track_num=1,
        total_tracks=1,
        author="Autor Teste",
    )

    audio = EasyID3(file_path)
    assert audio["title"] == ["Capítulo Único"]
    assert audio["album"] == ["Meu Livro"]
    assert audio["artist"] == ["Autor Teste"]
    assert audio["tracknumber"] == ["1/1"]


def test_combine_audio_files_success(tmp_path):
    output_dir = tmp_path / "output"
    book_dir = output_dir / "audiobooks" / "Livro_Teste"
    book_dir.mkdir(parents=True)

    ch1_path = str(book_dir / "01 - Intro.mp3")
    ch2_path = str(book_dir / "02 - Meio.mp3")

    with open(ch1_path, "wb") as f:
        f.write(create_mock_mp3_frame(3))
    with open(ch2_path, "wb") as f:
        f.write(create_mock_mp3_frame(4))

    manager = AudioManager(base_output_dir=str(output_dir))
    manager.tag_mp3(ch1_path, "Intro", "Livro Teste", 1, 2)
    manager.tag_mp3(ch2_path, "Meio", "Livro Teste", 2, 2)

    combined_path = manager.combine_audio_files(
        file_paths=[ch1_path, ch2_path],
        output_filename="Livro_Teste_completo.mp3",
        title="Livro Teste (Completo)",
        book_title="Livro Teste",
        author="Corredor",
    )

    assert os.path.exists(combined_path)
    audio = MP3(combined_path)
    assert audio.info.length > 0

    tags = EasyID3(combined_path)
    assert tags["title"] == ["Livro Teste (Completo)"]
    assert tags["album"] == ["Livro Teste"]
    assert tags["artist"] == ["Corredor"]
    assert tags["tracknumber"] == ["1/1"]


def test_combine_audio_files_empty_list_raises_error(tmp_path):
    manager = AudioManager(base_output_dir=str(tmp_path))
    with pytest.raises(AudioProcessingError) as exc_info:
        manager.combine_audio_files([], "output.mp3")
    assert "Nenhum arquivo de áudio fornecido" in str(exc_info.value)


def test_combine_audio_files_missing_file_raises_error(tmp_path):
    manager = AudioManager(base_output_dir=str(tmp_path))
    with pytest.raises(AudioProcessingError) as exc_info:
        manager.combine_audio_files(["arquivo_inexistente.mp3"], "output.mp3")
    assert "não encontrado" in str(exc_info.value)
