import whisper

model = whisper.load_model("base")  # options: tiny, base, small, medium

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]