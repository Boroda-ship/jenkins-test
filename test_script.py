import datetime
import sys
import os

print("=" * 60)
print(f"Python версия: {sys.version}")
print(f"Виртуальное окружение: {sys.prefix}")
print(f"Время запуска: {datetime.datetime.now()}")
print(f"Рабочая директория: {os.getcwd()}")
print("=" * 60)

# Создаем файл
filename = f"task_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(filename, 'w') as f:
    f.write(f"Задача выполнена: {datetime.datetime.now()} Hello world\n")
    f.write(f"Python: {sys.version}\n")

print(f"✅ Создан файл: {filename}")
print("✅ Задача выполнена успешно!")
