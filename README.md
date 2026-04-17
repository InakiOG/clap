# clap

Simple Python app that listens for a clap on the microphone and, when detected:

1. Opens Spotify for a previously chosen song.
2. Plays a local placeholder audio file at the same time.

## Install

```bash
python -m pip install -r requirements.txt
```

## Usage

```bash
python clap_player.py --song "Never Gonna Give You Up"
```

Optional arguments:

- `--audio-file /path/to/file.wav` to use a custom local audio.
- `--clap-threshold 0.35` to adjust clap sensitivity.
- `--simulate-clap` to trigger the clap action immediately (useful for quick manual checks).

If the audio file does not exist, the app creates a `placeholder_audio.wav` tone automatically.
