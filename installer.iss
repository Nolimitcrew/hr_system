[Setup]
AppName=HR-Система
AppVersion=1.2
AppPublisher=Ваша Организация
DefaultDirName={autopf}\HR_System
DefaultGroupName=HR-Система
OutputDir=installer_output
OutputBaseFilename=HR_System_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayIcon={app}\HR_System.exe

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Files]
; Копируем ТОЛЬКО программу и файл .env (установщика PostgreSQL здесь больше нет!)
Source: "dist\HR_System\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: ".env"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Ярлыки
Name: "{group}\HR-Система"; Filename: "{app}\HR_System.exe"
Name: "{commondesktop}\HR-Система"; Filename: "{app}\HR_System.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Run]
; Запускаем программу (она сама создаст базу, если PostgreSQL уже установлен)
Filename: "{app}\HR_System.exe"; Description: "Запустить HR-Систему"; Flags: nowait postinstall skipifsilent

[Code]
// Этот блок проверяет, установлен ли PostgreSQL, и выводит предупреждение, если его нет
function InitializeSetup(): Boolean;
begin
  if not DirExists('C:\Program Files\PostgreSQL') and not DirExists('C:\Program Files (x86)\PostgreSQL') then
  begin
    MsgBox('ВНИМАНИЕ!' + #13#10 +
           'На вашем компьютере не обнаружен PostgreSQL.' + #13#10 +
           'Для работы HR-Системы требуется установленная база данных.' + #13#10#13#10 +
           'Вы можете продолжить установку программы, но перед запуском' + #13#10 +
           'вам будет необходимо установить PostgreSQL (файл postgresql-installer.exe).', mbError, MB_OK);
  end;
  Result := True;
end;