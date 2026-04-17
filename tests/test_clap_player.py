import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from clap_player import ClapSpotifyPlayer


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

    def test_ensure_placeholder_audio_creates_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_path = Path(temp_dir) / "placeholder_audio.wav"
            app = ClapSpotifyPlayer(
                song_name="Song",
                placeholder_audio_path=audio_path,
            )
            app.ensure_placeholder_audio()

            self.assertTrue(audio_path.exists())
            self.assertGreater(audio_path.stat().st_size, 0)

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
            which_mock.side_effect = lambda command: "aplay" if command == "aplay" else None

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


if __name__ == "__main__":
    unittest.main()
