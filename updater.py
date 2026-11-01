import os
import sys
import requests
import subprocess
import tempfile
import time
from version import VERSION

# ВАЖНО: Замените эти данные на ваш репозиторий на GitHub!
GITHUB_USER = "ваш_логин_github"
GITHUB_REPO = "hr_system"
CURRENT_VERSION = VERSION


def check_for_updates():
    """Проверяет наличие новой версии на GitHub"""
    url = f"https://github.com/Nolimitcrew/hr_system/releases/latest"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            latest_version = data['tag_name'].replace('v', '')  # Убираем 'v' из 'v1.0.1'

            # Если версия на GitHub новее
            if latest_version != CURRENT_VERSION:
                print(f"Доступна новая версия: {latest_version} (у вас {CURRENT_VERSION})")

                # Ищем файл установщика в релизе
                for asset in data.get('assets', []):
                    if asset['name'] == 'HR_System_Setup.exe':
                        return latest_version, asset['browser_download_url']
    except Exception as e:
        print(f"Ошибка проверки обновлений: {e}")
    return None, None


def download_and_install(url):
    """Скачивает установщик и запускает его"""
    print("Скачивание обновления...")
    temp_dir = tempfile.gettempdir()
    installer_path = os.path.join(temp_dir, "HR_System_Update.exe")

    try:
        # Скачиваем файл кусками (чтобы не загружать 300 МБ в память)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(installer_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("Запуск установки обновления...")

        # Запускаем установщик в тихом режиме (/SILENT)
        # Установщик сам закроет текущую программу, обновит файлы и запустит заново
        subprocess.Popen([installer_path, '/SILENT', '/SUPPRESSMSGBOXES', '/NORESTART'])

        # Даем установщику пару секунд, чтобы он перехватил управление, и закрываем текущую программу
        time.sleep(2)
        sys.exit(0)

    except Exception as e:
        print(f"Ошибка при скачивании обновления: {e}")
        input("Нажмите Enter для продолжения работы...")


def run_update_check():
    """Основная функция, вызываемая при старте"""
    new_version, download_url = check_for_updates()
    if new_version and download_url:
        print(f"\n!!! Доступно обновление до версии {new_version} !!!")
        answer = input("Обновить программу прямо сейчас? (y/n): ")
        if answer.lower() == 'y':
            download_and_install(download_url)