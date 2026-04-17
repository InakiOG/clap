[Setup]
AppName=ClapSpotifyPlayer
AppVersion=1.0.0
AppPublisher=ClapSpotifyPlayer
DefaultDirName={autopf}\ClapSpotifyPlayer
DefaultGroupName=ClapSpotifyPlayer
OutputDir=..\dist
OutputBaseFilename=ClapSpotifyPlayer-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\dist\ClapSpotifyPlayer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ClapSpotifyPlayer"; Filename: "{app}\ClapSpotifyPlayer.exe"
Name: "{commondesktop}\ClapSpotifyPlayer"; Filename: "{app}\ClapSpotifyPlayer.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\ClapSpotifyPlayer.exe"; Description: "Launch ClapSpotifyPlayer"; Flags: nowait postinstall skipifsilent
