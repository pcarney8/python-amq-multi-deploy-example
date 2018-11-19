pipeline {

    agent {
        label "master"
    }

    environment {
        // Global Vars
        CI_CD_NAMESPACE = "patrick-ci-cd"
        DEV_NAMESPACE = "patrick-dev"
        TEST_NAMESPACE = "patrick-test"

        APP_NAME = sh(script: "oc get bc checksum-validate --template={{.metadata.labels.app}}", returnStdout: true)
        APPLY_PLAYBOOK_NAME = "apply.yml"
        APPLIER_TARGET = "apps"
        APPLIER_SKIP_TAGS = "amq-queues,bitbucket-jenkins-webhook"
        SOURCE_CONTEXT_DIR = "" // probably not needed

        JENKINS_TAG = "${JOB_NAME}.${BUILD_NUMBER}".replace("/", "-")
        ACTIVEMQ_ADDRESS = "amq-broker-amq-amqp-patrick-dev.apps.patrick.rht-labs.com"

        NEXUS_SERVICE_HOST = 'nexus'
        NEXUS_SERVICE_PORT = '8081'
        NEXUS_SECRET_NAME = "${CI_CD_NAMESPACE}-nexus-user-pass"

        OCP_API_SERVER = "${OPENSHIFT_API_URL}"
        OCP_TOKEN = readFile('/var/run/secrets/kubernetes.io/serviceaccount/token').trim()


    }

    options {
        buildDiscarder(logRotator(numToKeepStr:'10'))
        timeout(time: 15, unit: 'MINUTES')
        ansiColor('xterm')
        timestamps()
    }

    stages {
        stage("Test and Build") {
            agent {
                node {
                    label "jenkins-slave-python"
                }
            }
            steps {
                slackSend "${APP_NAME} Job Started - ${JOB_NAME} ${BUILD_NUMBER} (<${BUILD_URL}console|Open>)"

                    sh """
                        set -e
                        pwd
                        ls -al
                        pip install --user pipenv
                        pipenv sync
                        pipenv install --dev
                        pipenv run behave
                    """
            }
        }

        stage("Bake Image") {
            steps {
                script{
                    patchBuildConfigOutputLabels(env)

                    openshift.withCluster () {
                        def buildSelector = openshift.startBuild( "${APP_NAME}" )
                        buildSelector.logs('-f')
                    }
                }
            }
        }

        stage('Deploy: Dev'){
            agent { label 'jenkins-slave-ansible'}
            steps {
                script{
                    applyAnsibleInventory( "${APPLIER_TARGET}", 'app-deploy-dev', "${APPLIER_SKIP_TAGS}" )
                    timeout(5) { // in minutes
                        openshift.loglevel(3)
                        promoteImageWithinCluster( "${APP_NAME}", "${CI_CD_NAMESPACE}", "${DEV_NAMESPACE}", "${JENKINS_TAG}" )
                        verifyDeployment("${APP_NAME}-metadata", "${DEV_NAMESPACE}")
                        verifyDeployment("${APP_NAME}-science", "${DEV_NAMESPACE}")
                    }
                }
            }
        }

        stage('Deploy: Test'){
            agent { label 'jenkins-slave-ansible'}
            options {
                timeout(time: 1, unit: 'HOURS')
            }
            steps {
                script {
                    slackSend "${env.APP_NAME} Input requested - ${JOB_NAME} ${BUILD_NUMBER} (<${BUILD_URL}input/|Open>)"
                    input message: 'Deploy to Test?'

                }
                script{
                    applyAnsibleInventory( "${APPLIER_TARGET}", 'app-deploy-test' , "${APPLIER_SKIP_TAGS}" )
                    timeout(10) { // in minutes
                        promoteImageWithinCluster( "${APP_NAME}", "${CI_CD_NAMESPACE}", "${TEST_NAMESPACE}", "${JENKINS_TAG}" )
                        // the new client is having random failures
                        verifyDeployment("${APP_NAME}-metadata", "${TEST_NAMESPACE}")
                        verifyDeployment("${APP_NAME}-science", "${TEST_NAMESPACE}")
                    }
                }

                slackSend color: "good", message: ":success: ${APP_NAME} Build Completed - ${JOB_NAME} ${BUILD_NUMBER} (<${BUILD_URL}|Open>)"

            }
        }
    }
}
