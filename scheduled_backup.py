#!/usr/bin/env python
import datetime
import os
import shutil
import logging
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduled_task.log'),
        logging.StreamHandler()
    ]
)

class TaskScheduler:
    def __init__(self):
        self.task_name = "Jenkins_Backup_Task"
        self.log_dir = Path("logs")
        self.backup_dir = Path("backups")
        
        # Создаем необходимые директории
        self.log_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self):
        """Создает бэкап важных файлов"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"backup_{timestamp}.txt"
        
        # Собираем информацию о текущем состоянии
        with open(backup_file, 'w') as f:
            f.write(f"Backup created: {datetime.datetime.now()}\n")
            f.write(f"Task: {self.task_name}\n")
            f.write("-" * 50 + "\n")
            
            # Список всех Python скриптов
            scripts = list(Path(".").glob("*.py"))
            f.write(f"Python scripts found: {len(scripts)}\n")
            for script in scripts:
                f.write(f"  - {script}\n")
            
            # Список всех текстовых файлов
            txt_files = list(Path(".").glob("*.txt"))
            f.write(f"\nText files found: {len(txt_files)}\n")
            for txt in txt_files:
                f.write(f"  - {txt}\n")
        
        logging.info(f"Backup created: {backup_file}")
        return backup_file
    
    def cleanup_old_files(self, keep=10):
        """Удаляет старые файлы бэкапов"""
        backups = sorted(self.backup_dir.glob("backup_*.txt"))
        removed = 0
        
        if len(backups) > keep:
            for old_backup in backups[:-keep]:
                old_backup.unlink()
                removed += 1
                logging.info(f"Removed old backup: {old_backup}")
        
        if removed:
            logging.info(f"Cleaned up {removed} old backups")
        return removed
    
    def run(self):
        """Основной метод выполнения задачи"""
        start_time = datetime.datetime.now()
        logging.info(f"=== Starting task: {self.task_name} ===")
        
        try:
            # Выполняем основную работу
            backup_file = self.create_backup()
            cleaned = self.cleanup_old_files()
            
            # Создаем отчет
            duration = (datetime.datetime.now() - start_time).total_seconds()
            
            report = {
                "status": "SUCCESS",
                "task": self.task_name,
                "start_time": start_time.isoformat(),
                "duration_seconds": duration,
                "backup_file": str(backup_file),
                "files_cleaned": cleaned
            }
            
            logging.info(f"Task completed successfully in {duration:.2f} seconds")
            logging.info(f"Backup: {backup_file}")
            
            # Сохраняем отчет
            report_file = self.log_dir / f"report_{start_time.strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_file, 'w') as f:
                for key, value in report.items():
                    f.write(f"{key}: {value}\n")
            
            return report
            
        except Exception as e:
            logging.error(f"Task failed: {e}")
            return {"status": "ERROR", "error": str(e)}

if __name__ == "__main__":
    task = TaskScheduler()
    result = task.run()
    print(f"\nResult: {result}")
