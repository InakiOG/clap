from __future__ import annotations

import argparse
import math
import platform
import shutil
import subprocess
import threading
import time
import wave
import webbrowser
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import quote


class ClapSpotifyPlayer:
    def __init__(
        self,
        song_name: str,
        placeholder_audio_path: Path,
        clap_threshold: float = 0.35,
        clap_cooldown_seconds: float = 1.0,
        action_runner: Optional[Callable[[], None]] = None,
    ) -> None:
        self.song_name = song_name.strip()
        self.placeholder_audio_path = Path(placeholder_audio_path)
        self.clap_threshold = clap_threshold
        self.clap_cooldown_seconds = clap_cooldown_seconds
        self._last_clap_time = 0.0
        self._action_runner = action_runner or self.run_clap_actions

    def ensure_placeholder_audio(self) -> None:
        if self.placeholder_audio_path.exists():
            return

        self.placeholder_audio_path.parent.mkdir(parents=True, exist_ok=True)

        sample_rate = 44100
        duration_seconds = 1.0
        frequency = 880.0
        amplitude = 16000
        frame_count = int(sample_rate * duration_seconds)

        with wave.open(str(self.placeholder_audio_path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)

            for i in range(frame_count):
                value = int(amplitude * math.sin(2.0 * math.pi * frequency * i / sample_rate))
                wav_file.writeframesraw(value.to_bytes(2, byteorder="little", signed=True))

    def spotify_uri(self) -> str:
        return f"spotify:search:{quote(self.song_name)}"

    def open_spotify_and_play(self) -> None:
        webbrowser.open(self.spotify_uri())

    def play_local_audio(self) -> None:
        if not self.placeholder_audio_path.exists():
            return

        file_path = str(self.placeholder_audio_path)
        system = platform.system()

        if system == "Windows":
            escaped_file_path = file_path.replace("'", "''")
            subprocess.Popen(
                [
                    "powershell",
                    "-c",
                    f"(New-Object Media.SoundPlayer '{escaped_file_path}').PlaySync();",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return

        if system == "Darwin" and shutil.which("afplay"):
            subprocess.Popen(
                ["afplay", file_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return

        if system == "Linux":
            if shutil.which("aplay"):
                subprocess.Popen(
                    ["aplay", file_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return
            if shutil.which("paplay"):
                subprocess.Popen(
                    ["paplay", file_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return

    def run_clap_actions(self) -> None:
        spotify_thread = threading.Thread(target=self.open_spotify_and_play, daemon=True)
        audio_thread = threading.Thread(target=self.play_local_audio, daemon=True)
        spotify_thread.start()
        audio_thread.start()

    def handle_clap(self) -> None:
        now = time.time()
        if now - self._last_clap_time < self.clap_cooldown_seconds:
            return

        self._last_clap_time = now
        self._action_runner()

    def listen_and_wait_for_claps(self) -> None:
        try:
            import numpy as np
            import sounddevice as sd
        except ImportError as exc:
            raise RuntimeError(
                "Microphone listening requires 'numpy' and 'sounddevice'. "
                "Install dependencies first."
            ) from exc

        self.ensure_placeholder_audio()
        print("Listening for claps... Press Ctrl+C to stop.")

        def audio_callback(indata, _frames, _callback_time, status):
            if status:
                return
            if indata.size == 0:
                return
            volume_norm = float(np.linalg.norm(indata) / np.sqrt(max(indata.size, 1)))
            if volume_norm >= self.clap_threshold:
                self.handle_clap()

        with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100):
            while True:
                time.sleep(0.1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Listen for a hand clap using the microphone, then open Spotify for a "
            "user-selected song and play a local placeholder audio."
        )
    )
    parser.add_argument(
        "--song",
        help="Song to search and play on Spotify. If omitted, you will be prompted.",
    )
    parser.add_argument(
        "--audio-file",
        default="placeholder_audio.wav",
        help="Path to local audio played when a clap is detected.",
    )
    parser.add_argument(
        "--clap-threshold",
        default=0.35,
        type=float,
        help="Clap sensitivity threshold.",
    )
    parser.add_argument(
        "--simulate-clap",
        action="store_true",
        help="Run clap actions immediately without microphone input.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    song_name = args.song or input("Enter a song name to play on clap: ").strip()
    if not song_name:
        raise SystemExit("A song name is required.")

    app = ClapSpotifyPlayer(
        song_name=song_name,
        placeholder_audio_path=Path(args.audio_file),
        clap_threshold=args.clap_threshold,
    )

    if args.simulate_clap:
        app.ensure_placeholder_audio()
        app.run_clap_actions()
        return

    app.listen_and_wait_for_claps()


if __name__ == "__main__":
    main()
