# Project Riko (Windows Guide)

Project Riko is an anime-focused voice chat pipeline that combines:
- OpenAI LLM responses
- Faster-Whisper ASR (speech-to-text)
- GPT-SoVITS TTS (text-to-speech)

This README is **Windows-only**.

## 1) Configure
Edit `character_config.yaml`:
- Put your real OpenAI key in `OPENAI_API_KEY`
- Confirm `ref_audio_path` points to a valid `.wav` file on your Windows machine

## 2) Install (Windows PowerShell)
```powershell
pip install uv
pip install torch==2.6.0 torchaudio --index-url https://download.pytorch.org/whl/cu126
uv pip install -r extra-req.txt --no-deps
uv pip install -r requirements.txt
```

(Optional NLTK assets)
```powershell
python - <<'PYCODE'
import nltk
for pkg in ["averaged_perceptron_tagger", "cmudict"]:
    nltk.download(pkg)
PYCODE
```

## 3) Start GPT-SoVITS API first
Start your GPT-SoVITS TTS server so this endpoint is available:
- `http://127.0.0.1:9880/tts`

## 4) Preview TTS only (quick check)
```powershell
python server/process/tts_func/sovits_ping.py
```
If successful, it generates `output.wav`.

## 5) Run full voice chat
From repo root:
```powershell
python server/main_chat.py
```

Flow:
1. Press Enter to start recording
2. Press Enter again to stop
3. Audio is transcribed
4. LLM generates response
5. GPT-SoVITS speaks response

## Notes
- Current assistant behavior is configured for Indian Hinglish responses in Roman script via `character_config.yaml`.
- If mic/audio playback fails on Windows, verify your default input/output devices in system sound settings.
