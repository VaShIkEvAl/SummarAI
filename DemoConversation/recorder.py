import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

fs = 16000

class Recorder:
    def __init__(self):
        self.recording = []
        self.is_recording = False
        self.stream = None

    def callback(self, indata, frames, time, status):
        if self.is_recording:
            self.recording.append(indata.copy())

    def start(self):
        self.recording = []
        self.is_recording = True
        self.stream = sd.InputStream(
            samplerate=fs,
            channels=1,
            callback=self.callback
        )
        self.stream.start()

    def stop(self):
        self.is_recording = False
        self.stream.stop()
        self.stream.close()

        audio = np.concatenate(self.recording, axis=0)

        audio = np.clip(audio, -1, 1)
        # 🔥 FIX: Convert to 16-bit PCM
        audio = (audio * 32767).astype(np.int16)

        write("conversation.wav", fs, audio)

        return "conversation.wav"