pipeline{
    agent any
    stages{
        stage("Docker Image"){
            steps{
                sh "docker build -t veneethkumar/pyappeks:${env.BUILD_NUMBER} ."
            }
        }
        stage("Pust To Docker Hub"){
            steps{
                withCredentials([usernamePassword(credentialsId: 'docker-pwd', passwordVariable: 'pwd', usernameVariable: 'usr')]) {
                    sh "docker login -u ${usr} -p ${pwd}"
                    sh "docker push veneethkumar/pyappeks:${env.BUILD_NUMBER}"
                }
            }
        }
        stage("Update Tag in Deployment YAML and push"){
            steps{
                withCredentials([gitUsernamePassword(credentialsId: 'git-pwd', gitToolName: 'Default')]) {
                    sh '''
    git config user.name "Jenkins Server"
    git config user.email "jenkins@automation.com"
    yq e '.spec.template.spec.containers[0].image = "veneethkumar/pyappeks:${BUILD_NUMBER}"' -i ./k8s/pyapp-deployment.yml

    # Add the updated YAML file to git
    git add ./k8s/pyapp-deployment.yml

    git commit -m "Updated image tag to ${BUILD_NUMBER}"
    git push origin main
'''

                }
            }
        }
    }
}
