# Jenkins Test Project

Проект для автоматического выполнения Python скриптов по расписанию на Windows.

## 📁 Структура проекта
jenkins-test/
├── venv/ # Виртуальное окружение (не в репозитории)
├── scheduled_backup.py # Основной скрипт
├── run_scheduled.bat # Запускатор для планировщика
├── requirements.txt # Зависимости Python
├── check_task.sh # Скрипт проверки статуса
├── monitor_task.sh # Скрипт мониторинга
├── .gitignore # Исключаемые файлы
└── README.md # Этот файл

text

## 🚀 Установка

### 1. Клонирование репозитория
```bash
git clone <your-repo-url>
cd jenkins-test
2. Создание виртуального окружения
bash
python -m venv venv
source venv/Scripts/activate  # Git Bash
# или
venv\Scripts\activate.bat     # CMD
3. Установка зависимостей
bash
pip install -r requirements.txt
📝 Использование
Ручной запуск
bash
python scheduled_backup.py
Запуск через .bat
bash
./run_scheduled.bat
Настройка планировщика Windows
bash
schtasks /create /tn "JenkinsBackupTask" /tr "C:\Users\%USERNAME%\Desktop\jenkins-test\run_scheduled.bat" /sc minute /mo 5 /f
Мониторинг
bash
./check_task.sh      # Проверка статуса
./monitor_task.sh    # Мониторинг выполнения
🔧 Настройка
Изменение расписания
Каждые 15 минут: /sc minute /mo 15

Каждый час: /sc hourly

Ежедневно в 9:00: /sc daily /st 09:00

Изменение скрипта
Отредактируйте scheduled_backup.py под свои нужды.

📊 Логирование
Логи сохраняются в scheduled_task.log

История выполнения в task_execution.log

🗑️ Очистка
Старые файлы бэкапов автоматически удаляются (остается последние 10).

📦 Зависимости
Python 3.14+


