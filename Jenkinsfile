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
          # if you need pip deps uncomment following line:
          # pip3 install -r requirements.txt -t build/
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

    stage('Deploy Lambda (create/update)') {
      steps {
        withCredentials([[
          $class: 'AmazonWebServicesCredentialsBinding',
          credentialsId: 'aws-credentials'
        ]]) {
          script {
            def s3Key = "${S3_KEY_PREFIX}/${ZIP_NAME}"
            sh '''
              set -e
              # check if function exists
              if aws lambda get-function --function-name ${LAMBDA_NAME} --region ${AWS_REGION} > /dev/null 2>&1; then
                echo "Updating function code..."
                aws lambda update-function-code --function-name ${LAMBDA_NAME} --s3-bucket ${S3_BUCKET} --s3-key ${s3Key} --region ${AWS_REGION}
              else
                echo "Function not found. Creating function..."
                if [ -z "${ROLE_ARN}" ]; then
                  echo "ROLE_ARN must be set to create the function. Please set pipeline environment variable ROLE_ARN"
                  exit 1
                fi
                aws lambda create-function \
                  --function-name ${LAMBDA_NAME} \
                  --runtime python3.9 \
                  --role ${ROLE_ARN} \
                  --handler lambda_handler.handler \
                  --code S3Bucket=${S3_BUCKET},S3Key=${s3Key} \
                  --timeout 30 \
                  --memory-size 128 \
                  --region ${AWS_REGION}
              fi
            '''
          }
        }
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
