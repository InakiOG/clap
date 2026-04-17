# Deployment Guide

## What You Have

Your Windows application is ready to distribute. Two options are available:

### 1. Single Executable (Easiest for Most Users)

**File:** `dist/ClapSpotifyPlayer.exe` (~250 MB)

**How to distribute:**
- Upload to GitHub Releases
- Share via file hosting (Dropbox, Google Drive, etc.)
- Users just download and double-click

**Pros:**
- Single file, easy to share
- No extraction needed

**Cons:**
- File is larger
- No built-in uninstall

### 2. Portable ZIP (Best for Tech-Savvy Users)

**File:** `dist/ClapSpotifyPlayer-Portable.zip` (~248 MB)

**Contents:**
- `ClapSpotifyPlayer.exe` - Main executable
- `Run-ClapSpotifyPlayer.cmd` - Launcher (double-click to run)
- `README-FIRST.txt` - Quick start instructions
- `README.md` - Full documentation

**How to distribute:**
- Upload to GitHub Releases
- Share via file hosting
- Users unzip and run `Run-ClapSpotifyPlayer.cmd`

**Pros:**
- Includes clear first-run instructions
- Self-contained folder
- Easy to move or delete

**Cons:**
- Requires unzipping
- Slightly more steps

## Distribution Checklist

- [ ] Test both the .exe and .zip on a clean Windows machine
- [ ] Add to GitHub Releases with release notes
- [ ] Update USER_GUIDE.md with download links
- [ ] Test that `--simulate-clap` works
- [ ] Confirm Spotify integration works
- [ ] Verify microphone access prompt appears
- [ ] Test with `--temperature` override

## Rebuilding

When you make code changes:

```powershell
.\build_windows_package.ps1
```

This regenerates both the `.exe` and `.zip` in `dist/`.

## Future Improvements

### Installer
To create a proper `.exe` installer, install Inno Setup on your build machine:
1. Download from https://jrsoftware.org/isdl.php
2. Run `.\build_windows_package.ps1`
3. It will auto-detect and build `ClapSpotifyPlayer-Setup.exe`

### Code Signing
For production distribution, consider:
- Signing the .exe with a certificate to avoid SmartScreen warnings
- Getting Authenticode certificate from a certificate authority

### Updates
Consider adding auto-update functionality using a tool like:
- Squirrel.Windows
- WinSparkle
- Custom update checker

## Quick Release Template

```markdown
# ClapSpotifyPlayer v1.0.0

Listen for hand claps and trigger Spotify playback with voice announcements!

## Download

- **Portable (no installation):** [ClapSpotifyPlayer-Portable.zip](link)
- **Single executable:** [ClapSpotifyPlayer.exe](link)

## Quick Start

1. Download and run
2. Clap twice when ready
3. Enjoy!

[See USER_GUIDE.md for full instructions](USER_GUIDE.md)
```
