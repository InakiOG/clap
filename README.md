# ClapSpotifyPlayer

A Windows app that listens for hand claps on your microphone. When you clap twice, it:

1. Opens your default Spotify track
2. Speaks a personalized message with the current time and temperature

## Download & Run

**For end users:** See [USER_GUIDE.md](USER_GUIDE.md) for download links and usage instructions.

Available as:
- **Portable** (no installation): `ClapSpotifyPlayer-Portable.zip` - just unzip and double-click
- **Installer**: `ClapSpotifyPlayer-Setup.exe` - installs to Start Menu

## For Developers

### Requirements

- Python 3.12+
- numpy
- sounddevice
- pyttsx3

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Build Windows exe

```powershell
.\build_windows_exe.ps1
```

Creates: `dist\ClapSpotifyPlayer.exe`

### Build portable package + installer

```powershell
.\build_windows_package.ps1
```

Creates:
- `dist\ClapSpotifyPlayer-Portable.zip` (always)
- `dist\ClapSpotifyPlayer-Setup.exe` (if Inno Setup is installed)

### Run from source

```bash
python clap_player.py
```

### Command-line options

- `--song "Song Name"` - Change the default track
- `--temperature "72 F"` - Override auto temperature
- `--weather-location "London"` - Fetch real temperature for a location
- `--clap-threshold 0.08` - Adjust sensitivity (lower = more sensitive)
- `--double-clap-window 0.5` - Time between claps
- `--simulate-clap` - Test without microphone
- `--debug` - Show debug logs

See `python clap_player.py --help` for all options.
