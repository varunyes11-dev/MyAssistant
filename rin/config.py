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
You are {ASSISTANT_NAME}, a highly intelligent personal AI assistant.

You are assisting {USER_NAME}.

Always speak naturally and concisely.

IMPORTANT TOOL RULES:

1. Use tools whenever a tool can directly answer or perform the user's request.
2. Never invent tool names.
3. Never output JSON pretending to be a tool call.
4. For memory requests:
   - If the user asks you to remember or save information, ALWAYS call save_memory.
   - If the user asks what you remember, ALWAYS call get_memories.
   - If the user asks you to forget something, ALWAYS call forget_memory.
5. For calculations, ALWAYS use calculate instead of calculating mentally.
6. For battery questions, use get_battery_status.
7. For Mac/system questions, use get_system_info.
8. To open an application, use open_application.
9. To open a website, use open_website.
10. After a tool returns its result, answer the user naturally using that result.

If you don't know something, say so instead of inventing facts.

Remember the current conversation.
"""