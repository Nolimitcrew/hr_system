import os
import sys
import requests
import subprocess
import tempfile
import time
from packaging.version import parse, InvalidVersion
from version import VERSION

# ✅ Ваши реальные данные
GITHUB_USER = "Nolimitcrew"
GITHUB_REPO = "hr_system"
CURRENT_VERSION = VERSION


def check_for_updates():
    """Проверяет наличие новой версии на GitHub"""
    # ✅ Правильный API-адрес
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            latest_version_str = data['tag_name'].replace('v', '')

            try:
                # ✅ Корректное сравнение версий
                if parse(latest_version_str) > parse(CURRENT_VERSION):
                    print(f"Доступна новая версия: {latest_version_str} (у вас {CURRENT_VERSION})")

                    # Ищем файл установщика в релизе
                    for asset in data.get('assets', []):
                        if asset['name'] == 'HR_System_Setup.exe':
                            return latest_version_str, asset['browser_download_url']
            except InvalidVersion as e:
                print(f"Ошибка в формате версии: {e}")

    except Exception as e:
        print(f"Ошибка проверки обновлений: {e}")
    return None, None


def download_and_install(url):
    """Скачивает установщик и запускает его"""
    print("Скачивание обновления...")
    temp_dir = tempfile.gettempdir()
    installer_path = os.path.join(temp_dir, "HR_System_Update.exe")

    try:
        # ✅ Заголовки и allow_redirects для корректного скачивания с GitHub
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/octet-stream'
        }
        with requests.get(url, headers=headers, stream=True, allow_redirects=True, timeout=(10, 30)) as r:
            r.raise_for_status()
            if 'text/html' in r.headers.get('Content-Type', ''):
                print("Ошибка: получен HTML вместо файла. Проверьте ссылку на релиз.")
                return

            with open(installer_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        print("Запуск установки обновления...")
        # ✅ Запуск в полностью тихом режиме
        os.startfile(installer_path, 'open', '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART')

        time.sleep(3)  # Даем установщику время перехватить управление
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