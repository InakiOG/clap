import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from clap_player import ClapSpotifyPlayer, DEFAULT_SPOTIFY_TRACK_URL


class ClapSpotifyPlayerTests(unittest.TestCase):
    def test_spotify_uri_encodes_song_name(self) -> None:
        app = ClapSpotifyPlayer(
            song_name="Never Gonna Give You Up",
            placeholder_audio_path=Path("placeholder_audio.wav"),
        )
        self.assertEqual(
            app.spotify_uri(),
            "spotify:search:Never%20Gonna%20Give%20You%20Up",
        )

    def test_spotify_uri_defaults_to_fixed_track(self) -> None:
        app = ClapSpotifyPlayer(
            song_name=None,
            placeholder_audio_path=Path("placeholder_audio.wav"),
        )
        self.assertEqual(app.spotify_uri(), DEFAULT_SPOTIFY_TRACK_URL)

    def test_build_speech_text_uses_current_time_and_temperature(self) -> None:
        app = ClapSpotifyPlayer(
            song_name="Song",
            placeholder_audio_path=Path("placeholder_audio.wav"),
            temperature_text="72 F",
        )

        with patch("clap_player.datetime") as datetime_mock:
            datetime_mock.now.return_value = datetime(2026, 4, 17, 9, 5)
            self.assertEqual(
                app.build_speech_text(),
                "Good morning sir, systems are operational, the current time is: 9:05 AM, and the current temperature is: 72 F.",
            )

    def test_build_speech_text_uses_real_temperature_when_auto(self) -> None:
        app = ClapSpotifyPlayer(
            song_name="Song",
            placeholder_audio_path=Path("placeholder_audio.wav"),
            temperature_text="auto",
        )

        with patch("clap_player.datetime") as datetime_mock:
            datetime_mock.now.return_value = datetime(2026, 4, 17, 9, 5)
            with patch.object(app, "fetch_real_temperature", return_value="21 C"):
                self.assertEqual(
                    app.build_speech_text(),
                    "Good morning sir, systems are operational, the current time is: 9:05 AM, and the current temperature is: 21 C.",
                )

    @patch("clap_player.pyttsx3.init")
    @patch("clap_player.datetime")
    def test_ensure_placeholder_audio_creates_file(self, datetime_mock, init_mock) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_path = Path(temp_dir) / "placeholder_audio.wav"
            datetime_mock.now.return_value = datetime(2026, 4, 17, 9, 5)
            engine_mock = init_mock.return_value
            engine_mock.getProperty.return_value = []
            app = ClapSpotifyPlayer(
                song_name="Song",
                placeholder_audio_path=audio_path,
                temperature_text="72 F",
            )
            app.ensure_placeholder_audio()

            init_mock.assert_called_once()
            engine_mock.setProperty.assert_any_call("rate", 150)
            engine_mock.save_to_file.assert_called_once_with(
                "Good morning sir, systems are operational, the current time is: 9:05 AM, and the current temperature is: 72 F.",
                str(audio_path),
            )
            engine_mock.runAndWait.assert_called_once()

    def test_custom_speech_text_is_used(self) -> None:
        app = ClapSpotifyPlayer(
            song_name="Song",
            placeholder_audio_path=Path("placeholder_audio.wav"),
            speech_text="Testing one two",
            temperature_text="72 F",
            speech_rate=120,
        )

        self.assertEqual(app.speech_text, "Testing one two")
        self.assertEqual(app.speech_rate, 120)
        self.assertEqual(app.build_speech_text(), "Testing one two")

    def test_resolve_temperature_text_falls_back_when_fetch_fails(self) -> None:
        app = ClapSpotifyPlayer(
            song_name="Song",
            placeholder_audio_path=Path("placeholder_audio.wav"),
            temperature_text="auto",
        )

        with patch.object(app, "fetch_real_temperature", return_value=None):
            self.assertEqual(app.resolve_temperature_text(), "unavailable")

    @patch("clap_player.subprocess.Popen")
    def test_play_local_audio_skips_when_file_missing(self, popen_mock) -> None:
        app = ClapSpotifyPlayer(
            song_name="Song",
            placeholder_audio_path=Path("/does/not/exist.wav"),
        )
        app.play_local_audio()
        popen_mock.assert_not_called()

    @patch("clap_player.subprocess.Popen")
    @patch("clap_player.shutil.which")
    @patch("clap_player.platform.system", return_value="Linux")
    def test_play_local_audio_linux_uses_aplay(
        self, _platform_mock, which_mock, popen_mock
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_path = Path(temp_dir) / "placeholder_audio.wav"
            audio_path.write_bytes(b"audio")
            which_mock.side_effect = lambda command: "/usr/bin/aplay" if command == "aplay" else None

            app = ClapSpotifyPlayer(song_name="Song", placeholder_audio_path=audio_path)
            app.play_local_audio()

            popen_mock.assert_called_once()
            called_args = popen_mock.call_args[0][0]
            self.assertEqual(called_args[0], "aplay")
            self.assertEqual(called_args[1], str(audio_path))

    def test_handle_clap_respects_cooldown(self) -> None:
        calls = []
        app = ClapSpotifyPlayer(
            song_name="Song",
            placeholder_audio_path=Path("placeholder_audio.wav"),
            clap_cooldown_seconds=5.0,
            action_runner=lambda: calls.append("called"),
        )

        app.handle_clap()
        app.handle_clap()
        self.assertEqual(calls, ["called"])

    @patch("clap_player.time.time")
    def test_handle_clap_triggers_on_double_clap(self, time_mock) -> None:
        calls = []
        time_mock.side_effect = [100.0, 100.2]

        app = ClapSpotifyPlayer(
            song_name="Song",
            placeholder_audio_path=Path("placeholder_audio.wav"),
            double_clap_window_seconds=0.5,
            action_runner=lambda: calls.append("called"),
        )

        app.handle_clap()
        app.handle_clap()

        self.assertEqual(calls, ["called"])

    @patch("clap_player.time.time")
    def test_handle_clap_waits_for_second_clap(self, time_mock) -> None:
        calls = []
        time_mock.return_value = 100.0

        app = ClapSpotifyPlayer(
            song_name="Song",
            placeholder_audio_path=Path("placeholder_audio.wav"),
            double_clap_window_seconds=0.5,
            action_runner=lambda: calls.append("called"),
        )

        app.handle_clap()

        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
