# SummarAI

SummarAI is an AI-powered conversation analysis tool that converts text, uploaded files, or recorded audio into structured summaries and answers user questions based on the generated summary.

The system uses Google Gemini for summarization and question answering, and Whisper for speech-to-text transcription.

---

## Features

- Text summarization
- Audio recording and transcription
- Upload `.txt` files
- Structured summary generation
- Key points extraction
- Action items detection
- Copy individual sections
- Download summary
- Ask questions based on generated summary
- Editable transcribed text before summarization
- Handles large conversations using chunking and overlap

---

## Input Supported

- Manual text input
- Audio recording
- `.txt` file upload

---

## Output Generated

- Title
- Summary
- Key Points
- Action Items
- Answers to user questions

---

## Project Structure

```text
SummarAI/
│── app.py
│── requirements.txt
│── .env.example
│
├── services/
│   └── gemini_service.py
│
├── audio_processing/
│   ├── recorder.py
│   └── transcriber.py
│
├── utils/
│   └── text_loader.py
│
├── styles/
│   └── style.css
│
├── tests/
│   ├── test_gemini_service.py
│   ├── test_recorder.py
│   ├── test_transcriber.py
│   └── test_text_loader.py
│
└── mutants/
```

---

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- OpenAI Whisper
- Sounddevice
- NumPy
- SciPy
- PyTest

---

## Installation

Clone the repository:

```bash
git clone https://github.com/VaShIkEvAl/SummarAI
cd SummarAI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

---

## Run Project

```bash
streamlit run app.py
```

---

## Running Tests

Run unit tests & coverage:

```bash
pytest --cov=audio_processing --cov=services --cov=utils --cov-report=term-missing --cov-report=html
```

---

## Mutation Testing

Run mutation testing:

```bash
python mutation_runner.py
```

---

## Testing Summary

### Unit Testing
- White-box testing performed
- Coverage achieved: 97%

### Mutation Testing
- Mutation score achieved: 89.47%

### System Testing
- Black-box testing completed
- Acceptance testing completed

### GUI Testing
- UI interactions tested

### Non-Functional Testing
- Performance
- Reliability
- Maintainability

---

## System Workflow

```text
Input (Audio/Text/File)
        ↓
Transcription (if audio)
        ↓
Preprocessing
        ↓
Summarization
        ↓
Structured Output
        ↓
Question Answering
        ↓
Display / Copy / Download
```

---

## Modules

### app.py
Main UI controller

### recorder.py
Audio recording logic

### transcriber.py
Speech-to-text conversion

### text_loader.py
File reading utility

### gemini_service.py
Summarization and question answering

---

<!-- ## Future Improvements

- PDF file support
- DOCX support
- Speaker diarization
- Multiple language support
- Cloud deployment
- Real-time transcription -->

---

## Known Limitations

- Depends on Gemini API availability
- Requires internet connection
- Whisper may require FFmpeg on some systems

---

## Authors

Project Team: SummarAI

---

## License

This project is for academic purposes only.