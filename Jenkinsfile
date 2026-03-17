pipeline {
    agent any

    environment {
        ALLURE_RESULTS = 'allure-results'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                echo 'Создаём виртуальное окружение...'
                sh '''
                    python3 -m venv venv
                    
                    # Ззависимости
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install allure-pytest
                    
                    # Проверяем установку
                    pip list
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Запуск тестов...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ \
                        --alluredir=${ALLURE_RESULTS} \
                        -v
                '''
            }
        }
    }

    post {
        always {
            allure results: [[path: "${ALLURE_RESULTS}"]]
            archiveArtifacts artifacts: "${ALLURE_RESULTS}/**", allowEmptyArchive: true
        }
        success {
            echo '+ Все тесты пройдены!'
        }
        failure {
            echo 'X Тесты провалились'
        }
    }
}