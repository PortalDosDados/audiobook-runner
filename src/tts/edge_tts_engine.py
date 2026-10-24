import asyncio
import os
import edge_tts
from typing import List, Dict, Optional

AVAILABLE_VOICES = [
    {"id": "pt-BR-FranciscaNeural", "name": "Francisca (Português - Feminina, Natural)", "gender": "Feminina", "lang": "pt-BR"},
    {"id": "pt-BR-AntonioNeural", "name": "Antonio (Português - Masculina, Firme)", "gender": "Masculina", "lang": "pt-BR"},
    {"id": "pt-BR-ThalitaNeural", "name": "Thalita (Português - Feminina, Clara)", "gender": "Feminina", "lang": "pt-BR"},
    {"id": "pt-PT-RaquelNeural", "name": "Raquel (Português de Portugal)", "gender": "Feminina", "lang": "pt-PT"},
    {"id": "pt-PT-DuarteNeural", "name": "Duarte (Português de Portugal)", "gender": "Masculina", "lang": "pt-PT"},
    {"id": "en-US-GuyNeural", "name": "Guy (Inglês - Masculina)", "gender": "Masculina", "lang": "en-US"},
    {"id": "en-US-JennyNeural", "name": "Jenny (Inglês - Feminina)", "gender": "Feminina", "lang": "en-US"}
]

class EdgeTTSEngine:
    """Motor de síntese de voz usando vozes neurais de alta fidelidade do Edge-TTS."""

    def __init__(self, voice: str = "pt-BR-FranciscaNeural", rate: str = "+0%", pitch: str = "+0Hz"):
        self.voice = voice
        self.rate = rate
        self.pitch = pitch

    @staticmethod
    def get_voices() -> List[Dict[str, str]]:
        return AVAILABLE_VOICES

    async def generate_speech(self, text: str, output_path: str, progress_callback=None) -> str:
        """
        Gera o áudio a partir do texto e salva no caminho indicado.
        Suporta textos longos dividindo por parágrafos para maior estabilidade.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            pitch=self.pitch
        )
        await communicate.save(output_path)
        return output_path

    def generate_speech_sync(self, text: str, output_path: str) -> str:
        """Versão síncrona para chamadas diretas."""
        return asyncio.run(self.generate_speech(text, output_path))
