pipeline {
  agent any

  environment {
    AWS_REGION = 'ap-south-1'          
    S3_BUCKET = 'my-lambda-deploy-bucket-ayush-test' 
    S3_KEY_PREFIX = 'emp-lambda'
    ZIP_NAME = 'emp_lambda.zip'
    LAMBDA_NAME = 'Emp_Master'                    
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Package') {
      steps {
        sh '''
          rm -rf build
          mkdir build
          cp lambda_handler.py build/
          cd build
          zip -r ../${ZIP_NAME} .
          cd ..
          ls -lh ${ZIP_NAME}
        '''
      }
    }

    stage('Upload to S3') {
      steps {
        withCredentials([[
          $class: 'AmazonWebServicesCredentialsBinding',
          credentialsId: 'aws-credentials'  
        ]]) {
          sh '''
            aws --version
            aws s3 cp ${ZIP_NAME} s3://${S3_BUCKET}/${S3_KEY_PREFIX}/${ZIP_NAME} --region ${AWS_REGION}
          '''
        }
      }
    }

  post {
    success {
      echo "Deployment succeeded."
    }
    failure {
      echo "Deployment failed."
    }
  }
}
