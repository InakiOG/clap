param(
    [string]$PythonExe = "c:\Users\Green\miniconda3\envs\AprAut\python.exe"
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

& .\build_windows_exe.ps1 -PythonExe $PythonExe

$distDir = Join-Path $projectRoot "dist"
$portableDir = Join-Path $projectRoot "release\ClapSpotifyPlayer-Portable"
$portableZip = Join-Path $distDir "ClapSpotifyPlayer-Portable.zip"

if (Test-Path $portableDir) {
    Remove-Item $portableDir -Recurse -Force
}

New-Item -ItemType Directory -Path $portableDir | Out-Null
Copy-Item (Join-Path $distDir "ClapSpotifyPlayer.exe") $portableDir
Copy-Item (Join-Path $projectRoot "README.md") $portableDir

@"
ClapSpotifyPlayer Portable

1. Double-click ClapSpotifyPlayer.exe or Run-ClapSpotifyPlayer.cmd.
2. Allow microphone access if Windows asks.
3. Clap twice to trigger the action.

Optional command-line overrides are listed in README.md.
"@ | Set-Content -Path (Join-Path $portableDir "README-FIRST.txt") -Encoding ASCII

$launcherPath = Join-Path $portableDir "Run-ClapSpotifyPlayer.cmd"
@"
@echo off
start "" "%~dp0ClapSpotifyPlayer.exe"
"@ | Set-Content -Path $launcherPath -Encoding ASCII

if (Test-Path $portableZip) {
    Remove-Item $portableZip -Force
}

Compress-Archive -Path (Join-Path $portableDir '*') -DestinationPath $portableZip -Force

$iscc = Get-Command iscc -ErrorAction SilentlyContinue
if ($iscc) {
    & $iscc.Source (Join-Path $projectRoot "installer\ClapSpotifyPlayer.iss")
    Write-Host "Built installer using Inno Setup."
} else {
    Write-Host "Inno Setup not found; created portable package: $portableZip"
}
