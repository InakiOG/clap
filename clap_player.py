from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime
import platform
import shutil
import subprocess
import threading
import time
import webbrowser
from pathlib import Path
from typing import Callable, Optional, cast
from urllib.parse import quote
from urllib.request import urlopen

import pyttsx3


logger = logging.getLogger(__name__)
DEFAULT_SPOTIFY_TRACK_URL = "https://open.spotify.com/track/39shmbIHICJ2Wxnk1fPSdz?si=c2238860c1314edc"


class ClapSpotifyPlayer:
    def __init__(
        self,
        song_name: Optional[str],
        placeholder_audio_path: Path,
        clap_threshold: float = 0.08,
        double_clap_window_seconds: float = 0.5,
        clap_cooldown_seconds: float = 1.0,
        speech_text: Optional[str] = None,
        temperature_text: Optional[str] = None,
        weather_location: Optional[str] = None,
        speech_rate: int = 150,
        action_runner: Optional[Callable[[], None]] = None,
    ) -> None:
        self.song_name = (song_name or "").strip()
        self.song_target = self.song_name or DEFAULT_SPOTIFY_TRACK_URL
        self.placeholder_audio_path = Path(placeholder_audio_path)
        self.clap_threshold = clap_threshold
        self.double_clap_window_seconds = double_clap_window_seconds
        self.clap_cooldown_seconds = clap_cooldown_seconds
        self.speech_text = speech_text.strip() if speech_text else None
        self.temperature_text = (temperature_text or "auto").strip() or "auto"
        self.weather_location = (weather_location or "").strip()
        self.speech_rate = speech_rate
        self._last_clap_time = 0.0
        self._pending_clap_time = 0.0
        self._resolved_temperature_text: Optional[str] = None
        self._action_runner = action_runner or self.run_clap_actions

    def fetch_real_temperature(self) -> Optional[str]:
        if self.weather_location:
            weather_url = f"https://wttr.in/{quote(self.weather_location)}?format=j1"
        else:
            weather_url = "https://wttr.in/?format=j1"

        try:
            with urlopen(weather_url, timeout=6) as response:
                weather_data = json.load(response)
            temp_c = weather_data["current_condition"][0]["temp_C"]
            return f"{temp_c} C"
        except Exception as exc:
            logger.debug("Could not fetch real temperature: %s", exc)
            return None

    def resolve_temperature_text(self) -> str:
        if self._resolved_temperature_text is not None:
            return self._resolved_temperature_text

        if self.temperature_text.lower() != "auto":
            self._resolved_temperature_text = self.temperature_text
            return self._resolved_temperature_text

        real_temperature = self.fetch_real_temperature()
        self._resolved_temperature_text = real_temperature or "unavailable"
        return self._resolved_temperature_text

    def build_speech_text(self) -> str:
        if self.speech_text is not None:
            return self.speech_text

        current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
        resolved_temperature = self.resolve_temperature_text()
        return (
            "Good morning sir, systems are operational, the current time is: "
            f"{current_time}, and the current temperature is: {resolved_temperature}."
        )

    def ensure_placeholder_audio(self) -> None:
        self.placeholder_audio_path.parent.mkdir(parents=True, exist_ok=True)

        engine = pyttsx3.init()
        engine.setProperty("rate", self.speech_rate)
        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)
        speech_text = self.build_speech_text()
        engine.save_to_file(speech_text, str(self.placeholder_audio_path))
        engine.runAndWait()
        logger.debug("Generated speech audio: %s", speech_text)

    def spotify_uri(self) -> str:
        if (
            self.song_target.startswith("https://")
            or self.song_target.startswith("http://")
            or self.song_target.startswith("spotify:")
        ):
            return self.song_target
        return f"spotify:search:{quote(self.song_target)}"

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

        if self._pending_clap_time and now - self._pending_clap_time <= self.double_clap_window_seconds:
            logger.debug(
                "Double clap detected: interval=%.4f window=%.4f",
                now - self._pending_clap_time,
                self.double_clap_window_seconds,
            )
            self._pending_clap_time = 0.0
            self._last_clap_time = now
            self._action_runner()
            return

        self._pending_clap_time = now
        logger.debug("First clap detected; waiting for second clap")

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

        default_input_device = sd.default.device[0]
        if default_input_device is not None:
            device_info = sd.query_devices(default_input_device, kind="input")
            device_info_dict = cast(dict[str, object], device_info)
            logger.debug(
                "Using input device %s: %s",
                default_input_device,
                device_info_dict.get("name", "<unknown>"),
            )
        else:
            logger.debug("Using system default input device")

        def audio_callback(indata, _frames, _callback_time, status):
            if status:
                logger.debug("Audio stream status: %s", status)
                return
            if indata.size == 0:
                return
            volume_norm = float(np.linalg.norm(indata) / np.sqrt(indata.size))
            logger.debug(
                "Audio level: volume_norm=%.4f threshold=%.4f",
                volume_norm,
                self.clap_threshold,
            )
            if volume_norm >= self.clap_threshold:
                logger.debug(
                    "Clap detected: volume_norm=%.4f threshold=%.4f",
                    volume_norm,
                    self.clap_threshold,
                )
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
        help=(
            "Optional song override. Accepts a song name/search term, Spotify URI, "
            "or Spotify URL. If omitted, a default track is used."
        ),
    )
    parser.add_argument(
        "--audio-file",
        default="placeholder_audio.wav",
        help="Path to local synthesized speech played when a clap is detected.",
    )
    parser.add_argument(
        "--clap-threshold",
        default=0.08,
        type=float,
        help="Clap sensitivity threshold. Lower values make detection more sensitive.",
    )
    parser.add_argument(
        "--double-clap-window",
        default=0.5,
        type=float,
        help="Maximum time in seconds between two claps to count as a double clap.",
    )
    parser.add_argument(
        "--speech-text",
        default=None,
        help="Override the generated speech text.",
    )
    parser.add_argument(
        "--temperature",
        default="auto",
        help="Temperature text for speech. Use 'auto' to fetch real current temperature.",
    )
    parser.add_argument(
        "--weather-location",
        default="",
        help="Optional location for real temperature lookup (example: London).",
    )
    parser.add_argument(
        "--speech-rate",
        default=150,
        type=int,
        help="Speech rate for the generated voice clip. Lower values sound more robotic.",
    )
    parser.add_argument(
        "--simulate-clap",
        action="store_true",
        help="Run clap actions immediately without microphone input.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging, including clap detection messages.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    for noisy_logger_name in ("comtypes", "comtypes.client", "pyttsx3"):
        logging.getLogger(noisy_logger_name).setLevel(logging.WARNING)

    app = ClapSpotifyPlayer(
        song_name=args.song,
        placeholder_audio_path=Path(args.audio_file),
        clap_threshold=args.clap_threshold,
        double_clap_window_seconds=args.double_clap_window,
        speech_text=args.speech_text,
        temperature_text=args.temperature,
        weather_location=args.weather_location,
        speech_rate=args.speech_rate,
    )

    if args.simulate_clap:
        app.ensure_placeholder_audio()
        app.run_clap_actions()
        return

    app.listen_and_wait_for_claps()


if __name__ == "__main__":
    main()
