import os
import zipfile
from typing import List, Optional
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


class AudioProcessingError(Exception):
    """Exceção levantada para erros no processamento, empacotamento ou metadados de áudio."""

    pass


class AudioManager:
    """Organiza, etiqueta metadados e empacota capítulos de áudio para dispositivos de corrida."""

    def __init__(self, base_output_dir: str = "output"):
        self.base_output_dir = base_output_dir
        os.makedirs(self.base_output_dir, exist_ok=True)

    def tag_mp3(
        self,
        file_path: str,
        title: str,
        book_title: str,
        track_num: int,
        total_tracks: int,
        author: str = "Audiobook Runner",
    ) -> None:
        """Adiciona metadados ID3 para que players de celular e relógios (Garmin/Apple) exibam o capítulo certinho."""
        try:
            try:
                audio = EasyID3(file_path)
            except Exception:
                audio = MP3(file_path)
                audio.add_tags()
                audio.save()
                audio = EasyID3(file_path)

            audio["title"] = title
            audio["album"] = book_title
            audio["artist"] = author
            audio["tracknumber"] = f"{track_num}/{total_tracks}"
            audio.save()
        except Exception as e:
            raise AudioProcessingError(
                f"Erro ao adicionar tags ID3 em {file_path}: {e}"
            ) from e

    def combine_audio_files(
        self,
        file_paths: List[str],
        output_filename: str,
        title: Optional[str] = None,
        book_title: str = "Audiobook",
        author: str = "Audiobook Runner",
    ) -> str:
        """Compila uma lista de arquivos de áudio em um único arquivo de áudio final com metadados unificados.

        Remove cabeçalhos e rodapés de metadados ID3v2/ID3v1 intermediários de cada capítulo para compor um stream
        contínuo e íntegro de frames de áudio MP3, aplicando em seguida os metadados consolidados da obra.
        """
        if not file_paths:
            raise AudioProcessingError(
                "Nenhum arquivo de áudio fornecido para compilação."
            )

        if os.path.isabs(output_filename) or os.path.dirname(output_filename):
            final_path = output_filename
        else:
            final_path = os.path.join(self.base_output_dir, output_filename)

        os.makedirs(os.path.dirname(os.path.abspath(final_path)), exist_ok=True)

        try:
            with open(final_path, "wb") as out_f:
                for path in file_paths:
                    if not os.path.exists(path):
                        raise AudioProcessingError(
                            f"Arquivo de áudio não encontrado para compilação: {path}"
                        )

                    with open(path, "rb") as in_f:
                        data = in_f.read()

                    # Remove cabeçalho ID3v2 intermediário se presente
                    if data.startswith(b"ID3") and len(data) >= 10:
                        size_bytes = data[6:10]
                        tag_size = (
                            (size_bytes[0] << 21)
                            | (size_bytes[1] << 14)
                            | (size_bytes[2] << 7)
                            | size_bytes[3]
                        )
                        has_footer = bool(data[5] & 0x10)
                        header_size = 10 + tag_size + (10 if has_footer else 0)
                        data = data[header_size:]

                    # Remove rodapé ID3v1 intermediário se presente
                    if len(data) >= 128 and data[-128:-125] == b"TAG":
                        data = data[:-128]

                    out_f.write(data)

            # Aplica metadados ID3 consolidados ao arquivo completo
            track_title = title or f"{book_title} (Completo)"
            self.tag_mp3(
                file_path=final_path,
                title=track_title,
                book_title=book_title,
                track_num=1,
                total_tracks=1,
                author=author,
            )

            return final_path
        except AudioProcessingError:
            raise
        except Exception as e:
            raise AudioProcessingError(
                f"Erro ao compilar capítulos em arquivo único: {e}"
            ) from e

    def create_zip_package(self, book_dir: str, zip_filename: str) -> str:
        """Cria um pacote ZIP contendo todos os arquivos de áudio do livro para download rápido."""
        zip_path = os.path.join(self.base_output_dir, zip_filename)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(book_dir):
                for file in files:
                    if file.endswith((".mp3", ".m4b")):
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, book_dir)
                        zipf.write(full_path, arcname)
        return zip_path
