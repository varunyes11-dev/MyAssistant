from .brain import Brain
from .config import ASSISTANT_NAME, RECORD_SECONDS
from .recorder import Recorder
from .speaker import speak
from .transcriber import transcribe


class RinApp:
    def __init__(self):
        self.recorder = Recorder()
        self.brain = Brain()

    def run(self):
        speak(f"Hello Varun. {ASSISTANT_NAME} is ready.")

        while True:
            try:
                # 1. Record your voice
                audio_file = self.recorder.record(
                    duration=RECORD_SECONDS
                )

                # 2. Voice → Text
                user_message = transcribe(audio_file).strip()

                if not user_message:
                    print("Rin: I didn't hear anything.")
                    continue

                print(f"You: {user_message}")

                # 3. Stop command
                if user_message.lower() in {
                    "bye",
                    "goodbye",
                    "exit",
                    "quit",
                    "stop rin",
                    "rin stop",
                }:
                    speak("Goodbye Varun.")
                    break

                # 4. Think
                reply = self.brain.ask(user_message)

                # 5. Speak the answer
                speak(reply)

            except KeyboardInterrupt:
                print("\nStopping Rin...")
                speak("Goodbye Varun.")
                break

            except Exception as error:
                print(f"Rin error: {error}")
                speak("Sorry, something went wrong.")


if __name__ == "__main__":
    RinApp().run()