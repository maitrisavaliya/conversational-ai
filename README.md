**requirements.txt**
# Conversational AI (local voice assistant)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A compact, privacy-first Python demo that turns speech into natural conversations using a local LLM and local speech tools. Designed for local development and experimentation with voice interruption (speak while the assistant is talking).

## Highlights

- Voice-first interaction (speech-to-text → LLM → text-to-speech)
- Supports quick, local LLMs (e.g., Ollama models)
- Designed to run locally — no cloud required
- Windows-friendly instructions (cmd/Batch examples)

---

## Recommended repository name & short description

- Repository name: `conversational-ai`
- Short description: "Local Python voice assistant with speech-to-text, LLM integration, and text-to-speech — Windows-friendly demo."

You can use those when creating the repo on GitHub.

---

## Files in this project

This README describes the project files found in the workspace root. Brief summaries help you quickly find where things live.

```
conversational_ai/
├── __init__.py         # package marker / module init
├── audio_handler.py    # audio capture & VAD (voice activity detection)
├── config.py           # config loader (env / defaults)
├── llm_handler.py      # LLM integration (e.g., Ollama client wrapper)
├── main.py             # main application loop / orchestrator
├── speech_to_text.py   # speech recognition wrapper (Whisper or local alternative)
├── text_to_speech.py   # text-to-speech output
└── README.md           # this file
```

If you add `requirements.txt`, `.env.example`, or other assets, document them here as well.

---

## Quick start (Windows cmd)

These commands use Windows-style activation and paths (Batch / cmd). Run them in a Command Prompt or PowerShell (they work in both when using the same syntax for venv activation).

1) Clone the repo

```batch
git clone https://github.com/maitrisavaliya/conversational-ai.git
cd conversational-ai
```

2) Create a virtual environment

```batch
python -m venv venv
venv\Scripts\activate
```

3) Install dependencies

```batch
pip install -r requirements.txt
```

4) (Optional) Pull a local LLM model with Ollama

```batch
ollama pull llama3:latest
```

5) Run the app

```batch
python main.py
```

When the assistant starts you should see a ready message and can speak into your microphone. Say `exit`, `quit`, or `goodbye` to stop.

---

## Configuration

Use environment variables or an `.env` file to customize the app. Example keys (add to `.env` or export in your environment):

```env
# LLM
OLLAMA_MODEL_NAME=llama3:latest
OLLAMA_BASE_URL=http://localhost:11434

# ASR (speech-to-text)
WHISPER_MODEL_SIZE=base.en

# Audio
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1
AUDIO_DEVICE_INDEX=

# TTS
TTS_RATE=180
TTS_VOLUME=1.0
```

If your project uses a different config format, adapt these keys accordingly in `config.py`.

---

## Troubleshooting (Windows)

- If you see audio errors, verify microphone access and that your audio drivers are working.
- Whisper requires FFmpeg. On Windows, download FFmpeg and add the `bin` folder to your PATH.
- If `ollama` commands fail, ensure Ollama is installed and running (`ollama serve`).

Common checks:

```batch
where ffmpeg
python -c "import sounddevice; print(sounddevice.query_devices())"
ollama list
```

---

## How to publish to GitHub (cmd)

1) Create the repository on GitHub using the name and description suggested above.

2) Push your local project:

```batch
git init
git add .
git commit -m "Initial: Add conversational AI demo"
git branch -M main
git remote add origin https://github.com/<your-username>/conversational-ai.git
git push -u origin main
```

Replace `<your-username>` with your GitHub username.

---

## Contributing

Contributions are welcome. Suggested small improvements:

- Add a `requirements.txt` listing precise dependencies
- Provide a `.env.example` with default keys
- Add unit tests for critical modules

Please open an issue or a pull request.

---

## License

This project is provided under the MIT License. Add a `LICENSE` file to the repo root.

---

## Final notes

- This README is Windows-first and avoids bash-only snippets.
- If you'd like, I can also:
  - generate a `requirements.txt` from the environment
  - create a `.env.example` with recommended defaults
  - add a small `CONTRIBUTING.md` and `LICENSE` file

If you want any of those, tell me which and I'll add them next.

<!-- End of README -->
