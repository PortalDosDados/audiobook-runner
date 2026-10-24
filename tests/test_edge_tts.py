import pytest
from unittest.mock import AsyncMock, patch
from src.tts.edge_tts_engine import EdgeTTSEngine, AVAILABLE_VOICES


def test_available_voices():
    voices = EdgeTTSEngine.get_voices()
    assert len(voices) > 0
    ids = [v["id"] for v in voices]
    assert "pt-BR-FranciscaNeural" in ids


@pytest.mark.asyncio
async def test_generate_speech_uses_mock(tmp_path):
    engine = EdgeTTSEngine(voice="pt-BR-FranciscaNeural", rate="+10%")
    output_file = str(tmp_path / "test.mp3")

    with patch("edge_tts.Communicate") as mock_comm_cls:
        mock_instance = AsyncMock()
        mock_comm_cls.return_value = mock_instance

        result = await engine.generate_speech("Teste de narração", output_file)

        assert result == output_file
        mock_comm_cls.assert_called_once_with(
            text="Teste de narração",
            voice="pt-BR-FranciscaNeural",
            rate="+10%",
            pitch="+0Hz",
        )
        mock_instance.save.assert_awaited_once_with(output_file)
