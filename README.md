# clap

Simple Python app that listens for a clap on the microphone and, when detected:

1. Opens Spotify for a default track, unless you pass a custom song.
2. Plays a locally synthesized voice clip at the same time.

## Install

```bash
python -m pip install -r requirements.txt
```

## Usage

```bash
python clap_player.py
```

Optional arguments:

- `--song "Never Gonna Give You Up"` to override the default track with a search term, Spotify URI, or Spotify URL.
- `--audio-file /path/to/file.wav` to use a custom output file for the speech clip.
- `--speech-text "Playing Never Gonna Give You Up"` to customize the spoken phrase.
- `--temperature auto` to fetch the real current temperature automatically (default).
- `--temperature "72 F"` to provide a manual temperature value for the spoken prompt.
- `--weather-location "London"` to fetch real temperature for a specific location.
- `--speech-rate 150` to make the voice sound a little more robotic.
- `--clap-threshold 0.08` to adjust clap sensitivity.
- `--double-clap-window 0.5` to control how quickly the second clap must arrive.
- `--simulate-clap` to trigger the clap action immediately (useful for quick manual checks).

If the output file does not exist, the app creates a spoken voice clip automatically.
