import numpy as np
from audio_processing.recorder import Recorder

def test_callback():
    rec = Recorder()
    rec.is_recording = True

    fake_data = np.array([[0.5]])
    rec.callback(fake_data, None, None, None)

    assert len(rec.recording) == 1


def test_start(monkeypatch):
    rec = Recorder()

    class FakeStream:
        def start(self): pass

    def fake_stream(*args, **kwargs):
        return FakeStream()

    monkeypatch.setattr("audio_processing.recorder.sd.InputStream", fake_stream)

    rec.start()

    assert rec.is_recording is True


def test_stop(monkeypatch):
    rec = Recorder()

    rec.recording = [np.array([[0.1], [0.2]])]

    class FakeStream:
        def stop(self): pass
        def close(self): pass

    rec.stream = FakeStream()

    def fake_write(filename, fs, audio):
        assert filename == "conversation.wav"

    monkeypatch.setattr("audio_processing.recorder.write", fake_write)

    result = rec.stop()

    assert result == "conversation.wav"

def test_recorder_audio_not_empty(monkeypatch):
    import numpy as np
    from audio_processing.recorder import Recorder

    rec = Recorder()
    rec.recording = [np.array([[0.5], [0.2]])]

    class FakeStream:
        def stop(self): pass
        def close(self): pass

    rec.stream = FakeStream()

    def fake_write(filename, fs, audio):
        assert audio.shape[0] > 0

    monkeypatch.setattr("audio_processing.recorder.write", fake_write)

    rec.stop()