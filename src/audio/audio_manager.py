import os
import zipfile
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

class AudioManager:
    """Organiza, etiqueta metadados e empacota capítulos de áudio para dispositivos de corrida."""

    def __init__(self, base_output_dir: str = "output"):
        self.base_output_dir = base_output_dir
        os.makedirs(self.base_output_dir, exist_ok=True)

    def tag_mp3(self, file_path: str, title: str, book_title: str, track_num: int, total_tracks: int, author: str = "Audiobook Runner"):
        """Adiciona metadados ID3 para que players de celular e relógios (Garmin/Apple) exibam o capítulo certinho."""
        try:
            try:
                audio = EasyID3(file_path)
            except Exception:
                audio = MP3(file_path)
                audio.add_tags()
                audio = EasyID3(file_path)

            audio['title'] = title
            audio['album'] = book_title
            audio['artist'] = author
            audio['tracknumber'] = f"{track_num}/{total_tracks}"
            audio.save()
        except Exception as e:
            print(f"Erro ao adicionar tags ID3 em {file_path}: {e}")

    def create_zip_package(self, book_dir: str, zip_filename: str) -> str:
        """Cria um pacote ZIP contendo todos os arquivos de áudio do livro para download rápido."""
        zip_path = os.path.join(self.base_output_dir, zip_filename)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(book_dir):
                for file in files:
                    if file.endswith(('.mp3', '.m4b')):
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, book_dir)
                        zipf.write(full_path, arcname)
        return zip_path
