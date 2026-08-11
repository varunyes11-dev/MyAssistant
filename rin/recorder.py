from pathlib import Path
import queue

import numpy as np
import sounddevice as sd
import soundfile as sf
import webrtcvad

from .config import SAMPLE_RATE, CHANNELS, RECORD_SECONDS, SILENCE_TIMEOUT


class Recorder:
    def __init__(
        self,
        sample_rate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        output_file="data/temp/input.wav",
        vad_mode=2,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.output_file = Path(output_file)
        self.vad = webrtcvad.Vad(vad_mode)

        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        # WebRTC VAD works with 10, 20, or 30 ms audio frames.
        self.frame_duration_ms = 30
        self.frame_size = int(
            self.sample_rate * self.frame_duration_ms / 1000
        )

    def record(self, duration=RECORD_SECONDS):
        """
        Wait for speech, record while the user speaks,
        and stop after SILENCE_TIMEOUT seconds of silence.
        """

        if self.sample_rate not in (8000, 16000, 32000, 48000):
            raise ValueError(
                "WebRTC VAD requires a sample rate of "
                "8000, 16000, 32000, or 48000 Hz."
            )

        if self.channels != 1:
            raise ValueError(
                "WebRTC VAD requires mono audio."
            )

        audio_queue = queue.Queue()
        frames = []

        speech_started = False
        silence_frames = 0

        max_frames = int(
            self.sample_rate * duration / self.frame_size
        )

        max_silence_frames = int(
            SILENCE_TIMEOUT * 1000 / self.frame_duration_ms
        )

        def callback(indata, frame_count, time_info, status):
            if status:
                print(f"Audio status: {status}")

            audio_queue.put(indata.copy())

        print("\n🎤 Listening...")
        print("Start speaking. Rin will stop automatically after silence.\n")

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
            blocksize=self.frame_size,
            callback=callback,
        ):
            for _ in range(max_frames):
                audio_data = audio_queue.get()

                # Convert the NumPy frame to raw 16-bit PCM bytes
                audio_bytes = audio_data.reshape(-1).tobytes()

                is_speech = self.vad.is_speech(
                    audio_bytes,
                    self.sample_rate,
                )

                # Don't save silence before the user starts speaking
                if not speech_started:
                    if is_speech:
                        speech_started = True
                        print("🗣️ Speech detected...")
                        frames.append(audio_data)
                    continue

                # Save audio after speech has started
                frames.append(audio_data)

                if is_speech:
                    silence_frames = 0
                else:
                    silence_frames += 1

                if silence_frames >= max_silence_frames:
                    print("⏹️ Silence detected. Stopping...")
                    break

        if not frames:
            print("⚠️ No speech detected.")
            return None

        audio = np.concatenate(frames, axis=0)

        sf.write(
            self.output_file,
            audio,
            self.sample_rate,
        )

        print(f"✅ Audio saved to: {self.output_file}")

        return str(self.output_file)