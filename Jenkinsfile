pipeline {
  agent any
  stages {
    stage('Setup Python Env') {
      steps {
        sh 'python -m venv venv'
        sh '. venv/bin/activate && pip install -r requirements.txt'
      }
    }
    stage('Run Bot Check') {
      steps {
        // You can add a script to test the bot here, or keep it simple for now
        sh '. venv/bin/activate && echo "Bot environment ready"'
      }
    }
  }
}