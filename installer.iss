[Setup]
AppName=HR-Система
AppVersion=1.0
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
; 1. Копируем нашу собранную программу
Source: "dist\HR_System\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 2. Копируем файл .env
Source: ".env"; DestDir: "{app}"; Flags: ignoreversion
; 3. Копируем установщик PostgreSQL во временную папку
Source: "postgresql-18.6-5-windows-x64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Run]
; 1. ТИХАЯ УСТАНОВКА POSTGRESQL (Версия 18)
Filename: "{tmp}\postgresql-18.6-5-windows-x64.exe"; \
Parameters: "--mode unattended --unattendedmodeui minimal --superpassword postgres --servicename postgresql-x64-18 --serverport 5432  --prefix ""{commonpf}\PostgreSQL\18"""; \
StatusMsg: "Установка базы данных PostgreSQL (это может занять несколько минут)..."; \
Flags: waituntilterminated

; 2. СОЗДАНИЕ БАЗЫ ДАННЫХ И ПОЛЬЗОВАТЕЛЯ
; Идем в папку bin установленного Postgres 18 и запускаем psql.exe
Filename: "{commonpf}\PostgreSQL\18\bin\psql.exe"; \
Parameters: "-U postgres -c ""CREATE DATABASE hr_system_db;"" -c ""CREATE USER hr_user WITH PASSWORD 'hr_password_2024';"" -c ""GRANT ALL PRIVILEGES ON DATABASE hr_system_db TO hr_user;"""; \
StatusMsg: "Настройка базы данных..."; \
Flags: waituntilterminated runhidden

; 3. ЗАПУСК ПРОГРАММЫ ПОСЛЕ УСТАНОВКИ
Filename: "{app}\HR_System.exe"; Description: "Запустить HR-Систему"; Flags: nowait postinstall skipifsilent

[Icons]
Name: "{group}\HR-Система"; Filename: "{app}\HR_System.exe"
Name: "{autodesktop}\HR-Система"; Filename: "{app}\HR_System.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked