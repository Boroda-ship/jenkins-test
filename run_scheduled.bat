@echo off
echo =========================================
echo Запуск: %date% %time%
echo =========================================

cd /d C:\Users\user\Desktop\jenkins-test
call venv\Scripts\activate.bat
python scheduled_backup.py
deactivate

echo =========================================
echo Завершено: %date% %time%
echo =========================================
