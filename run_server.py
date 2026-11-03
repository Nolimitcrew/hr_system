import os
import sys
import threading
import ctypes
from waitress import serve

# Настраиваем Django перед запуском
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from django.core.management import call_command, execute_from_command_line
from config.wsgi import application
from updater import run_update_check
from apps.directories.models import OrganizationSettings


def hide_console():
    """Скрывает черное окно консоли в Windows"""
    try:
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hWnd = kernel32.GetConsoleWindow()
        if hWnd:
            user32.ShowWindow(hWnd, 0)  # 0 = SW_HIDE (скрыть)
    except Exception:
        pass


if __name__ == '__main__':
    # =========================================================================
    # ПРОВЕРКА КОМАНД КОМАНДНОЙ СТРОКИ (createsuperuser, migrate и т.д.)
    # =========================================================================
    if len(sys.argv) > 1:
        # Если передана команда, выполняем её через стандартный Django
        # и завершаем работу (сервер не запускаем)
        execute_from_command_line(sys.argv)
        sys.exit(0)
    # =========================================================================

    # --- ОБЫЧНЫЙ ЗАПУСК ПРОГРАММЫ ---

    # 1. Проверяем обновления на GitHub
    run_update_check()

    print("==================================================")
    print("   Подготовка базы данных...")

    # 2. АВТОМАТИЧЕСКОЕ СОЗДАНИЕ БАЗЫ И ПОЛЬЗОВАТЕЛЯ
    try:
        import psycopg
        from dotenv import load_dotenv

        load_dotenv()
        db_host = os.getenv("DB_HOST", "127.0.0.1")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "hr_system_db")
        db_user = os.getenv("DB_USER", "hr_user")
        db_pass = os.getenv("DB_PASSWORD", "hr_password_2024")

        print("   Проверка наличия базы данных...")
        with psycopg.connect(host=db_host, port=db_port, dbname="postgres", user="postgres", password="postgres",
                             autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (db_user,))
                if not cur.fetchone():
                    cur.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_pass}';")
                cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (db_name,))
                if not cur.fetchone():
                    cur.execute(f"CREATE DATABASE {db_name};")
                    cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};")
        with psycopg.connect(host=db_host, port=db_port, dbname=db_name, user="postgres", password="postgres",
                             autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(f"GRANT ALL ON SCHEMA public TO {db_user};")
                cur.execute(f"ALTER SCHEMA public OWNER TO {db_user};")
        print("   База данных готова.")
    except Exception as e:
        print(f"   ВНИМАНИЕ: База уже существует или ошибка: {e}")

    # 3. МИГРАЦИИ И АДМИНИСТРАТОР
    try:
        def run_migrations():
            call_command('migrate', interactive=False)


        migration_thread = threading.Thread(target=run_migrations)
        migration_thread.daemon = True
        migration_thread.start()
        migration_thread.join(timeout=15.0)

        if migration_thread.is_alive():
            print("   ВНИМАНИЕ: Миграции заняли слишком много времени.")
        else:
            print("   База данных обновлена.")

        from django.contrib.auth import get_user_model

        User = get_user_model()
        if not User.objects.exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            print("   Создан администратор (admin / admin).")
    except Exception as e:
        print(f"   ОШИБКА МИГРАЦИЙ: {e}")

    # 4. СБОРКА СТАТИКИ
    try:
        call_command('collectstatic', interactive=False, clear=True)
    except Exception:
        pass

    # 5. ОПРЕДЕЛЯЕМ ПОРТ ИЗ НАСТРОЕК
    port = 8000
    try:
        org_settings = OrganizationSettings.objects.first()
        if org_settings and org_settings.port:
            port = org_settings.port
    except Exception:
        pass

    print("==================================================")
    print(f"   HR-Система запущена на порту {port}.")
    print(f"   Для входа откройте браузер и перейдите по адресу:")
    print(f"   http://127.0.0.1:{port}/")
    print("   Окно консоли будет скрыто. Для выхода закройте")
    print("   процесс HR_System.exe в диспетчере задач.")
    print("==================================================")

    # 6. СКРЫВАЕМ КОНСОЛЬ И ЗАПУСКАЕМ СЕРВЕР
    hide_console()
    serve(application, host='127.0.0.1', port=port)