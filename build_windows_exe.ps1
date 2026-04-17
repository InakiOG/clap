param(
    [string]$PythonExe = "c:\Users\Green\miniconda3\envs\AprAut\python.exe"
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

& $PythonExe -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --console `
    --name ClapSpotifyPlayer `
    --collect-all pyttsx3 `
    --collect-all comtypes `
    --collect-all sounddevice `
    clap_player.py

Write-Host "Built dist\ClapSpotifyPlayer.exe"