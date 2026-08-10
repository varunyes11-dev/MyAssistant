from pathlib import Path
import sounddevice as sd
import soundfile as sf


class Recorder:
    def __init__(
        self,
        sample_rate=16000,
        channels=1,
        dtype="int16",
        output_file="data/temp/input.wav",
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.output_file = Path(output_file)

        # Create the folder if it doesn't exist
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

    def record(self, duration=5):
        print("\n🎤 Listening...")
        print(f"Speak for up to {duration} seconds.\n")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
        )

        sd.wait()

        sf.write(
            self.output_file,
            audio,
            self.sample_rate,
        )

        print(f"✅ Audio saved to: {self.output_file}")

        return str(self.output_file)