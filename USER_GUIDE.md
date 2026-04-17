# ClapSpotifyPlayer - User Guide

## Quick Start

### Option 1: Portable (No Installation Needed)

1. Download `ClapSpotifyPlayer-Portable.zip`
2. Unzip it to any folder
3. Double-click `Run-ClapSpotifyPlayer.cmd`
4. Allow microphone access if Windows asks
5. Clap twice to trigger the action!

### Option 2: Installer (Installs to Start Menu)

1. Download `ClapSpotifyPlayer-Setup.exe`
2. Run it and follow the prompts
3. Find ClapSpotifyPlayer in your Start Menu or desktop
4. Click to launch

## How to Use

### Basic Usage

1. **Launch the app** - Either run the portable launcher or click the Start Menu shortcut
2. **Wait for startup** - You'll see "Listening for claps..." in a console window
3. **Make two claps** - The app detects claps and triggers:
   - **Opens Spotify** for a default song
   - **Plays a voice announcement** with the current time and temperature

### What It Says

By default, the app says something like:
> "Good morning sir, systems are operational, the current time is 9:30 AM, and the current temperature is 18 C."

Then it opens Spotify and plays the announcement.

### Customization

If you want to change the default song or other settings, you can:

1. Right-click `ClapSpotifyPlayer.exe` or `Run-ClapSpotifyPlayer.cmd`
2. Select "Open Command Prompt here"
3. Type one of these commands:

```
REM Play a different song:
ClapSpotifyPlayer.exe --song "Your Favorite Song"

REM Use a manual temperature:
ClapSpotifyPlayer.exe --temperature "72 F"

REM Adjust clap sensitivity (lower = more sensitive):
ClapSpotifyPlayer.exe --clap-threshold 0.05

REM Test without listening to microphone:
ClapSpotifyPlayer.exe --simulate-clap
```

## Troubleshooting

### "Listening for claps..." but nothing happens

- **Check your microphone** - Make sure your mic is plugged in and enabled in Windows
- **Clap louder** - Try clapping directly at your microphone
- **Adjust sensitivity** - Add `--clap-threshold 0.05` to make it more sensitive

### Spotify doesn't open

- Make sure Spotify is installed on your computer
- If you want a different song, use: `--song "Song Name"`

### No voice announcement

- Check your speakers/headphones are on
- The app needs internet to fetch the current temperature; if offline, it will say "unavailable"

### "Could not import numpy" or similar error

- This is a packaging issue. Try:
  1. Delete the app folder
  2. Unzip the portable zip again
  3. Try the launcher again

## For Advanced Users

Run with `--help` to see all command-line options:

```
ClapSpotifyPlayer.exe --help
```

## Support

If you encounter issues:

1. Try the `--simulate-clap` flag to test without microphone
2. Check that your microphone works in Windows Settings
3. Ensure you have internet for weather/Spotify lookups
