pipeline {
    agent any

    environment {
        IMAGE_NAME = "veneethkumar/pyappeks:${BUILD_NUMBER}"
    }

    stages {
        stage("Docker Image") {
            steps {
                echo "🔨 Building Docker image: ${IMAGE_NAME}"
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage("Push to Docker Hub") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-pwd', passwordVariable: 'pwd', usernameVariable: 'usr')]) {
                    echo "🚀 Logging in to Docker Hub"
                    sh "echo ${pwd} | docker login -u ${usr} --password-stdin"
                    echo "📦 Pushing Docker image: ${IMAGE_NAME}"
                    sh "docker push ${IMAGE_NAME}"
                }
            }
        }

        stage("Update Tag in Deployment YAML and Push to Git") {
            steps {
                withCredentials([gitUsernamePassword(credentialsId: 'git-pwd', gitToolName: 'Default')]) {
                    sh '''
                        echo "🔁 Checking out main branch"
                        git checkout main

                        echo "📝 Configuring Git user"
                        git config user.name "Jenkins Server"
                        git config user.email "jenkins@automation.com"

                        echo "🛠️ Updating Kubernetes YAML with new image tag"
                        yq e '.spec.template.spec.containers[0].image = "veneethkumar/pyappeks:'"$BUILD_NUMBER"'"' -i ./k8s/pyapp-deployment.yml

                        echo "📂 Adding updated YAML to Git"
                        git add ./k8s/pyapp-deployment.yml

                        echo "✅ Committing change"
                        git commit -m "Updated image tag to $BUILD_NUMBER" || echo "Nothing to commit"

                        echo "📤 Pushing to main branch"
                        git push origin main
                    '''
                }
            }
        }
    }
}
