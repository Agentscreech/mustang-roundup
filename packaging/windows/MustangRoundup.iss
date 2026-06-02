#define MyAppName "Mustang Roundup"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Mustang Roundup"
#define MyAppExeName "MustangRoundup.exe"

[Setup]
AppId={{7C5D853A-7BA8-42F2-A8C8-6185410E94AF}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\Mustang Roundup
DefaultGroupName=Mustang Roundup
DisableProgramGroupPage=yes
OutputDir=..\..\dist\installer
OutputBaseFilename=MustangRoundup-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "..\..\dist\MustangRoundup\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Mustang Roundup"; Filename: "{app}\{#MyAppExeName}"
Name: "{userdesktop}\Mustang Roundup"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: checkedonce

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Start Mustang Roundup"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
