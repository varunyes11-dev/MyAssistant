from pathlib import Path

# ==========================
# Project Paths
# ==========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

TEMP_DIR = DATA_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)

# ==========================
# AI Models
# ==========================

OLLAMA_MODEL = "llama3.2"

WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"

# ==========================
# Audio
# ==========================

SAMPLE_RATE = 16000

CHANNELS = 1

RECORD_SECONDS = 30
# Maximum recording time.
# Voice Activity Detection will stop earlier.

SILENCE_TIMEOUT = 1.0

# ==========================
# Assistant
# ==========================

ASSISTANT_NAME = "Rin"

USER_NAME = "Varun"

SYSTEM_PROMPT = f"""
You are {ASSISTANT_NAME},
a highly intelligent personal AI assistant.

You are loyal to {USER_NAME}.

Always speak naturally.

Keep spoken answers concise unless
the user specifically asks for detail.

Remember the current conversation.

If you don't know something,
say so instead of inventing facts.
"""