# Testing & Release Guide

## Testing Before Release

### Test the Portable ZIP

1. **On a clean Windows machine or virtual machine:**
   - Download `ClapSpotifyPlayer-Portable.zip` to your Downloads folder
   - Right-click → Extract All
   - Open the extracted folder
   - Double-click `Run-ClapSpotifyPlayer.cmd`

2. **Verify these behaviors:**
   - [ ] Command prompt appears with "Listening for claps..."
   - [ ] After a few seconds, you see: "Listening for claps. Please double-clap to trigger action..."
   - [ ] Windows asks "Allow ClapSpotifyPlayer to access your microphone?" → Click "Allow" or "Yes"
   - [ ] The console shows your default microphone device name
   - [ ] Try: `--simulate-clap` flag to trigger without clapping
     - Open Command Prompt in the folder
     - Type: `ClapSpotifyPlayer.exe --simulate-clap`
     - Spotify should open or show a browser tab
     - You should hear/see a voice message

3. **Verify customization works:**
   - Open Command Prompt in the extracted folder
   - Try: `ClapSpotifyPlayer.exe --temperature "72 F" --simulate-clap`
   - Verify the spoken message includes "72 F"

4. **Verify first-run instructions:**
   - [ ] Open `README-FIRST.txt` - it's clear and helpful
   - [ ] It explains the 4 basic steps

### Test the Single EXE

1. **On a clean Windows machine:**
   - Download `ClapSpotifyPlayer.exe` to your Downloads folder
   - Double-click it directly (no extraction needed)

2. **Verify same behaviors as above:**
   - Console appears
   - Microphone permission prompt
   - `--simulate-clap` works

3. **File integrity:**
   - [ ] File size matches what you built (~250 MB)
   - [ ] Runs without any "corrupted" or "missing dependencies" errors
   - [ ] No pop-up about running unsigned code (Windows may warn, but should run)

### Optional: Real Clap Test

If you have a microphone on your test machine:

1. Run `ClapSpotifyPlayer.exe` or launch from the zip
2. Clap twice at normal volume
3. Verify it triggers within ~2 seconds
4. Adjust if needed: `--clap-threshold 0.05` (more sensitive) or `0.15` (less sensitive)

## Uploading to GitHub Releases

### Prerequisites

- Git installed and configured
- GitHub repo created: `github.com/yourusername/clap` (or your repo name)
- Local repo ready

### Step 1: Commit Your Documentation Changes

```powershell
cd F:\Github\clap

# Stage all changes
git add .

# Commit
git commit -m "Add user guides and deployment documentation"

# Push to GitHub
git push origin main
```

### Step 2: Create a GitHub Release

**Option A: Via GitHub Web UI (Easiest)**

1. Go to your repo: `https://github.com/yourusername/clap`
2. Click "Releases" on the right sidebar
3. Click "Create a new release" or "Draft a new release"
4. Fill in:
   - **Tag version:** `v1.0.0`
   - **Release title:** `ClapSpotifyPlayer v1.0.0`
   - **Description:** Paste the template below
5. Scroll to "Attach binaries by dropping them here or selecting them"
6. Drag and drop these files:
   - `dist/ClapSpotifyPlayer.exe`
   - `dist/ClapSpotifyPlayer-Portable.zip`
7. Click "Publish release"

**Option B: Via PowerShell (If you have GitHub CLI installed)**

```powershell
# Create the release
gh release create v1.0.0 `
  --title "ClapSpotifyPlayer v1.0.0" `
  --notes "Listen for hand claps and trigger Spotify playback with voice announcements!`
`n`n**Download:**`n- [ClapSpotifyPlayer-Portable.zip](https://github.com/yourusername/clap/releases/download/v1.0.0/ClapSpotifyPlayer-Portable.zip) - Recommended (no installation needed)`n- [ClapSpotifyPlayer.exe](https://github.com/yourusername/clap/releases/download/v1.0.0/ClapSpotifyPlayer.exe)`n`n**Quick Start:**`n1. Download one of the files above`n2. Run it (no installation needed)`n3. Clap twice when ready`n`nSee [USER_GUIDE.md](https://github.com/yourusername/clap/blob/main/USER_GUIDE.md) for full instructions." `
  dist/ClapSpotifyPlayer.exe dist/ClapSpotifyPlayer-Portable.zip
```

### Release Description Template

Copy this into your release notes:

```markdown
# ClapSpotifyPlayer v1.0.0

Listen for hand claps and trigger Spotify playback with dynamic voice announcements!

## What It Does

- Listens to your microphone for hand claps
- Detects double-claps (two quick claps)
- Opens your default Spotify track
- Speaks a personalized message with the current time and temperature

## Download

**Pick one:**

- **[ClapSpotifyPlayer-Portable.zip](...)** ← Recommended (no installation needed)
  - Just unzip and double-click to run
  - Includes first-run instructions
  
- **[ClapSpotifyPlayer.exe](...)** ← Single file
  - Download and double-click to run

## Quick Start

1. Download and run
2. Allow microphone access when prompted
3. Clap twice when you see "Listening for claps..."
4. Spotify opens and speaks a message!

## Full Instructions

See [USER_GUIDE.md](link-to-your-repo/blob/main/USER_GUIDE.md) for:
- Detailed usage guide
- Customization options
- Troubleshooting

## System Requirements

- Windows 7 or later
- Microphone
- Spotify installed (optional for testing with `--simulate-clap`)
- Internet (for weather/Spotify lookups)

## Known Issues

- First run may take a few seconds as it downloads speech synthesis
- Windows SmartScreen may warn about unsigned executable (click "Run anyway")

## Changelog

- Initial release
```

## Verification Checklist Before Publishing

- [ ] Tested exe on clean Windows machine
- [ ] Tested zip on clean Windows machine
- [ ] `--simulate-clap` works in both
- [ ] Microphone permission prompt appears
- [ ] Files committed to GitHub
- [ ] Release tag is semantic versioning (v1.0.0, v1.0.1, etc.)
- [ ] Release notes use the template above
- [ ] Both files attached to release
- [ ] Release is marked "Latest" (GitHub does this automatically)

## Post-Release

1. **Announce it** (optional):
   - Share GitHub Release link on social media, Reddit, Hacker News, etc.
   - Format: "I built a Clap-Activated Spotify Player for Windows - no installation needed"

2. **Collect feedback**:
   - GitHub Issues for bug reports
   - GitHub Discussions for feature requests

3. **For next version**:
   - Fix bugs or add features
   - Run `.\build_windows_package.ps1` again
   - Commit changes
   - Create new release with v1.0.1, v1.1.0, etc.

## Troubleshooting Upload Issues

**Files too large?**
- GitHub allows up to 2 GB per release
- Your files are ~250 MB each, so no issue

**Upload keeps timing out?**
- Try uploading one file at a time
- Use GitHub CLI instead of web UI: `gh release upload v1.0.0 dist/ClapSpotifyPlayer.exe`

**Need to delete and re-upload?**
```powershell
# Delete the release (you must have access)
# GitHub UI: Click the release → Click "Edit" → Click "Delete"
# Or use CLI:
gh release delete v1.0.0
```

## Alternative Distribution Options

**If you don't want to use GitHub:**

1. **Dropbox**: Upload to shared folder, get public link
2. **Google Drive**: Share folder with public link
3. **Your own website**: Upload to hosting
4. **SourceForge**: Old but still used for binary hosting

For now, **GitHub Releases is recommended** because:
- Free
- Reliable download speeds
- Built-in version control
- Users can star/watch your repo for updates
