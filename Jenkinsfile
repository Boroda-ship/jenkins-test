pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        disableConcurrentBuilds()
    }
    
    triggers {
        cron('H/15 * * * *')
    }
    
    environment {
        PYTHONUNBUFFERED = '1'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📦 Клонирование репозитория...'
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                echo '🐍 Настройка Python окружения...'
                bat """
                    cd %WORKSPACE%
                    echo Текущая директория: %CD%
                    echo Создание виртуального окружения...
                    if not exist venv\\Scripts\\activate.bat (
                        python -m venv venv
                        echo ✅ Виртуальное окружение создано
                    ) else (
                        echo ✅ Виртуальное окружение уже существует
                    )
                    echo Активация и установка зависимостей...
                    call venv\\Scripts\\activate.bat
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    deactivate
                """
            }
        }
        
        stage('Run Script') {
            steps {
                echo '🚀 Запуск Python скрипта...'
                bat """
                    cd %WORKSPACE%
                    call venv\\Scripts\\activate.bat
                    python scheduled_backup.py
                    set EXIT_CODE=%errorlevel%
                    deactivate
                    exit /b %EXIT_CODE%
                """
            }
            post {
                success {
                    echo '✅ Скрипт выполнен успешно!'
                }
                failure {
                    echo '❌ Скрипт завершился с ошибкой!'
                }
            }
        }
        
        stage('Archive Results') {
            steps {
                echo '📦 Архивируем результаты...'
                bat """
                    cd %WORKSPACE%
                    echo Сборка #%BUILD_NUMBER% > build_info.txt
                    echo Время: %BUILD_TIMESTAMP% >> build_info.txt
                    echo Статус: %BUILD_STATUS% >> build_info.txt
                """
                archiveArtifacts artifacts: 'backup_*.txt, *.log, build_info.txt', 
                                   allowEmptyArchive: true,
                                   fingerprint: true
            }
        }
        
        stage('Cleanup') {
            steps {
                echo '🧹 Очистка старых бэкапов (оставляем последние 20)...'
                bat """
                    cd %WORKSPACE%
                    for /f "skip=20 delims=" %%i in ('dir /b /o-d backup_*.txt 2^>nul') do (
                        echo Удаляю: %%i
                        del "%%i"
                    )
                    echo Очистка завершена
                """
            }
        }
    }
    
    post {
        always {
            echo "🏁 Сборка #${env.BUILD_NUMBER} завершена"
            cleanWs()  // Очистка рабочей области (опционально)
        }
        success {
            echo "🎉 Успех! Артефакты сохранены"
        }
        failure {
            echo "💥 Ошибка! Проверьте логи выше"
        }
    }
}
