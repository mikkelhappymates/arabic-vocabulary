[Setup]
AppName=Arabic Vocabulary
AppVersion=0.5.1
AppPublisher=Arabic Vocabulary
DefaultDirName={autopf}\Arabic Vocabulary
DefaultGroupName=Arabic Vocabulary
OutputBaseFilename=ArabicVocabulary-0.5.1-Setup
OutputDir=Output
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=assets\icon.ico
UninstallDisplayIcon={app}\ArabicVocabulary.exe

[Files]
Source: "dist\ArabicVocabulary\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Arabic Vocabulary"; Filename: "{app}\ArabicVocabulary.exe"
Name: "{commondesktop}\Arabic Vocabulary"; Filename: "{app}\ArabicVocabulary.exe"

[Run]
Filename: "{app}\ArabicVocabulary.exe"; Description: "Launch Arabic Vocabulary"; Flags: postinstall nowait skipifsilent
