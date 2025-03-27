pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.10'
        VENV_NAME = 'venv'
        PYTHON_EXECUTABLE = 'python3'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'pwd'
                sh 'ls -la'
                echo "Checked out source code"
            }
        }
        
        stage('Setup Virtual Environment') {
            steps {
                script {
                    try {
                        sh '''
                            ${PYTHON_EXECUTABLE} -m venv ${VENV_NAME}
                            . ${VENV_NAME}/bin/activate
                            pip install --upgrade pip setuptools wheel
                        '''
                        echo "Virtual environment created successfully"
                    } catch (Exception e) {
                        echo "Failed to create virtual environment: ${e.getMessage()}"
                        error "Virtual environment setup failed"
                    }
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    try {
                        sh '''
                            . ${VENV_NAME}/bin/activate
                            pip install -r requirements.txt
                        '''
                        echo "Dependencies installed successfully"
                    } catch (Exception e) {
                        echo "Dependency installation failed: ${e.getMessage()}"
                        error "Dependency installation failed"
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    try {
                        sh '''
                            . ${VENV_NAME}/bin/activate
                            python -m pytest
                        '''
                        echo "Tests completed successfully"
                    } catch (Exception e) {
                        echo "Tests failed: ${e.getMessage()}"
                        error "Test execution failed"
                    }
                }
            }
        }
        
        stage('Static Code Analysis') {
            steps {
                script {
                    try {
                        sh '''
                            . ${VENV_NAME}/bin/activate
                            flake8 .
                        '''
                        echo "Static code analysis completed successfully"
                    } catch (Exception e) {
                        echo "Static code analysis failed: ${e.getMessage()}"
                        // Uncomment the next line if you want static code analysis to fail the build
                        // error "Code quality checks failed"
                    }
                }
            }
        }
        
        stage('Database Migrations') {
            steps {
                script {
                    try {
                        sh '''
                            . ${VENV_NAME}/bin/activate
                            python manage.py check
                            python manage.py migrate --noinput
                        '''
                        echo "Database migrations completed successfully"
                    } catch (Exception e) {
                        echo "Database migration failed: ${e.getMessage()}"
                        error "Database migration failed"
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Cleanup virtual environment
                sh '''
                    rm -rf ${VENV_NAME}
                '''
            }
            // Clean workspace
            cleanWs()
        }
        
        success {
            echo 'Pipeline completed successfully! 🎉'
        }
        
        failure {
            echo 'Pipeline failed. Investigating... 🚨'
        }
    }
}