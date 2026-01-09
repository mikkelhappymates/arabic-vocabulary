[Setup]
AppName=Arabic Vocabulary
AppVersion=0.4.1 Beta
AppPublisher=Arabic Vocabulary
DefaultDirName={autopf}\Arabic Vocabulary
DefaultGroupName=Arabic Vocabulary
OutputBaseFilename=ArabicVocabulary-0.4.1-beta-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=assets\icon.ico
UninstallDisplayIcon={app}\Arabic Vocabulary.exe

[Files]
Source: "dist\Arabic Vocabulary\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Arabic Vocabulary"; Filename: "{app}\Arabic Vocabulary.exe"
Name: "{commondesktop}\Arabic Vocabulary"; Filename: "{app}\Arabic Vocabulary.exe"

[Run]
Filename: "{app}\Arabic Vocabulary.exe"; Description: "Launch Arabic Vocabulary"; Flags: postinstall nowait skipifsilent
