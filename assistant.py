import json
import subprocess
import tempfile
import urllib.request
import wave
import mlx_whisper
import sounddevice as sd

MODEL = "llama3.2"

messages = [
    {
        "role": "system",
        "content": (
            "You are Rin, a helpful personal AI assistant for Varun. "
            "Be friendly and clear. Keep normal replies short because "
            "you are speaking them aloud. Remember the current conversation."
        )
    }
]


def speak(text):
    subprocess.run(["say", text])


def listen():
    SAMPLE_RATE = 16000
    RECORD_SECONDS = 8

    print("\n🎤 Rin is listening...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        filename = temp_audio.name

    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio.tobytes())

    print("🧠 Rin is understanding...")

    result = mlx_whisper.transcribe(
        filename,
        path_or_hf_repo="mlx-community/whisper-small-mlx"
    )

    spoken_text = result["text"].strip()

    return spoken_text


print("\nRin is ready. Say 'bye' to close.")
speak("Hello Varun. Rin is ready.")

while True:
    user_message = listen()
    print(f"You: {user_message}")

    if user_message.lower() in [
        "bye",
        "by",
        "goodbye",
        "exit",
        "quit",
        "stop rin",
        "rin stop"
    ]:
        print("Rin: Goodbye!")
        speak("Goodbye!")
        break

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    data = json.dumps(
        {
            "model": MODEL,
            "messages": messages,
            "stream": False
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))

        reply = result["message"]["content"].strip()

        print(f"Rin: {reply}")
        speak(reply)

        messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

    except Exception as error:
        print("Rin: I could not reach my AI brain.")
        print(f"Details: {error}")
        speak("I could not reach my AI brain.")