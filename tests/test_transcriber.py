import pytest
from audio_processing import transcriber

def test_transcribe_audio(monkeypatch):
    def fake_transcribe(file_path):
        return {"text": "This is test transcription"}

    monkeypatch.setattr(transcriber.model, "transcribe", fake_transcribe)

    result = transcriber.transcribe_audio("fake.wav")

    assert result == "This is test transcription"