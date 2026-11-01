import os
import sys
import webbrowser
from threading import Timer
from waitress import serve
from updater import run_update_check

# Настраиваем Django перед запуском
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from django.core.management import call_command
from config.wsgi import application


def open_browser():
    webbrowser.open_new('http://127.0.0.1:8000/')


if __name__ == '__main__':
    # 1. Проверяем обновления перед запуском
    run_update_check()

    print("==================================================")
    print("   Подготовка базы данных (миграции)...")
    try:
        # Автоматически применяем миграции при запуске
        call_command('migrate', interactive=False)
        print("   База данных готова.")
    except Exception as e:
        print(f"   ОШИБКА БАЗЫ ДАННЫХ: {e}")
        print("   Проверьте, запущен ли PostgreSQL и верны ли данные в .env")
    call_command('collectstatic', interactive=False, clear=True)
    print("   HR-Система запускается...")
    print("   Не закрывайте это окно, пока работаете!")
    print("==================================================")

    Timer(1.5, open_browser).start()
    serve(application, host='127.0.0.1', port=8000)