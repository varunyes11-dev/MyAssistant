from pathlib import Path
from rin.transcriber import transcribe
audio = Path("rin_test.wav")
text = transcribe(audio)
print("\n========================")
print("Whisper Output:")
print(text)
print("========================")