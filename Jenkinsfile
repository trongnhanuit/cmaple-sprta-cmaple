//  a JenkinsFile to build iqtree
// paramters
//  1. git branch
// 2. git url


properties([
    parameters([
        booleanParam(defaultValue: false, description: 'Build CMAPLE baseline?', name: 'BUILD_CMAPLE_BASELINE'),
        string(name: 'CMAPLE_BASELINE_BRANCH', defaultValue: 'sprta', description: 'Branch to build CMAPLE baseline'),
        string(name: 'CMAPLE_BASELINE_COMMIT', defaultValue: '29250bd', description: 'Commit ID of the CMAPLE baseline'),
        booleanParam(defaultValue: false, description: 'Re-build the latest CMAPLE?', name: 'BUILD_CMAPLE'),
        string(name: 'CMAPLE_BRANCH', defaultValue: 'sprta', description: 'Branch to build the latest CMAPLE'),
        booleanParam(defaultValue: false, description: 'Download testing data?', name: 'DOWNLOAD_DATA'),
        booleanParam(defaultValue: false, description: 'Infer ML trees?', name: 'INFER_TREE'),
        booleanParam(defaultValue: false, description: 'Compute SPRTA by CMAPLE baseline?', name: 'COMPUTE_SPRTA_CMAPLE_BASELINE'),
        string(name: 'MODEL', defaultValue: 'UNREST', description: 'Substitution model'),
        booleanParam(defaultValue: true, description: 'Blengths fixed?', name: 'BLENGTHS_FIXED'),
        booleanParam(defaultValue: false, description: 'Do not reroot?', name: 'NOT_REROOT'),
        booleanParam(defaultValue: true, description: 'Compute supports for branches with a length of zero?', name: 'ZERO_LENGTH_BRANCHES'),
        booleanParam(defaultValue: true, description: 'Output alternative SPRs?', name: 'OUT_ALT_SPR'),
        booleanParam(defaultValue: true, description: 'Compute SPRTA by the latest CMAPLE?', name: 'COMPUTE_SPRTA_CMAPLE'),
        booleanParam(defaultValue: true, description: 'Remove all exiting output files?', name: 'REMOVE_OUTPUT'),
        booleanParam(defaultValue: true, description: 'Use CIBIV cluster?', name: 'USE_CIBIV'),
    ])
])
pipeline {
    agent any
    environment {
        GITHUB_REPO_URL = "https://github.com/iqtree/cmaple.git"
        CMAPLE_BASELINE_NAME = "cmaple_baseline"
        NCI_ALIAS = "gadi"
        SSH_COMP_NODE = " "
        WORKING_DIR = "/scratch/dx61/tl8625/cmaple/ci-cd"
        SCRIPTS_DIR = "${WORKING_DIR}/scripts"
        CMAPLE_BASELINE_DIR = "${WORKING_DIR}/${CMAPLE_BASELINE_NAME}"
        BUILD_OUTPUT_DIR = "${WORKING_DIR}/builds"
        BUILD_CMAPLE_DIR = "${BUILD_OUTPUT_DIR}/build-default"
        BUILD_BASELINE = "${BUILD_OUTPUT_DIR}/build-baseline"
        DATA_DIR = "${WORKING_DIR}/data"
        ALN_DIR = "${DATA_DIR}/aln"
        TREE_DIR = "${DATA_DIR}/tree"
        OUT_DIR = "${DATA_DIR}/output"
        CMAPLE_BASELINE_PATH = "${BUILD_BASELINE}/cmaple"
        CMAPLE_PATH = "${BUILD_CMAPLE_DIR}/cmaple"
        ML_TREE_PREFIX = "ML_tree_"
        PYTHON_SCRIPT_PATH = "${SCRIPTS_DIR}/extract_visualize_results.py"
        CMAPLE_BASELINE_TREE_PREFIX = "SPRTA_CMAPLE_BASELINE_tree_"
        CMAPLE_SPRTA_TREE_PREFIX = "SPRTA_CMAPLE_tree_"
        LOCAL_OUT_DIR = "/Users/nhan/DATA/tmp/visualize-sprta-pipeline/output"
        PYPY_PATH="/scratch/dx61/tl8625/tmp/pypy3.10-v7.3.17-linux64/bin/pypy3.10"
    }
    stages {
        stage('Init variables') {
            steps {
                script {
                    if (params.USE_CIBIV) {
                        NCI_ALIAS = "eingang"
                        SSH_COMP_NODE = " ssh -tt cox "
                        WORKING_DIR = "/project/AliSim/cmaple"
                        SCRIPTS_DIR = "${WORKING_DIR}/scripts"
                        CMAPLE_BASELINE_DIR = "${WORKING_DIR}/${CMAPLE_BASELINE_NAME}"
                        BUILD_OUTPUT_DIR = "${WORKING_DIR}/builds"
                        BUILD_BASELINE = "${BUILD_OUTPUT_DIR}/build-baseline"
                        BUILD_CMAPLE_DIR = "${BUILD_OUTPUT_DIR}/build-default"
                        CMAPLE_BASELINE_PATH = "${BUILD_BASELINE}/cmaple"
                        CMAPLE_PATH = "${BUILD_CMAPLE_DIR}/cmaple"
                        PYTHON_SCRIPT_PATH = "${SCRIPTS_DIR}/extract_visualize_results.py"
                        
                        DATA_DIR = "${WORKING_DIR}/data"
                        ALN_DIR = "${DATA_DIR}/aln"
                        TREE_DIR = "${DATA_DIR}/tree"
                        OUT_DIR = "${DATA_DIR}/output"
                        PYPY_PATH="/project/AliSim/tools/pypy3.10-v7.3.17-linux64/bin/pypy3.10"
                        
                    }
                }
            }
        }
        stage('Copy scripts') {
            steps {
                script {
                        sh """
                            ssh -tt ${NCI_ALIAS} << EOF
                        
                            mkdir -p ${WORKING_DIR}
                            mkdir -p ${SCRIPTS_DIR}
                            exit
                            EOF
                        """
                        sh "scp -r scripts/* ${NCI_ALIAS}:${SCRIPTS_DIR}"
                }
            }
        }
        stage('Build the CMAPLE baseline') {
            steps {
                script {
                    if (params.BUILD_CMAPLE_BASELINE) {
                        sh """
                            ssh -tt ${NCI_ALIAS} << EOF
                        
                            mkdir -p ${WORKING_DIR}
                            cd  ${WORKING_DIR}
                            git clone --recursive ${GITHUB_REPO_URL} ${CMAPLE_BASELINE_DIR}
                            cd ${CMAPLE_BASELINE_NAME}
                            git checkout ${params.CMAPLE_BASELINE_BRANCH}
                            git reset --hard ${params.CMAPLE_BASELINE_COMMIT}
                            mkdir -p ${BUILD_OUTPUT_DIR}
                            cd ${BUILD_OUTPUT_DIR}
                            rm -rf *
                            exit
                            EOF
                        """
                        
                        sh """
                            ssh -tt ${NCI_ALIAS} ${SSH_COMP_NODE}<< EOF
                        
                            chmod +x ${SCRIPTS_DIR}/build_cmaple_baseline.sh 
                            sh ${SCRIPTS_DIR}/build_cmaple_baseline.sh ${CMAPLE_BASELINE_NAME} ${CMAPLE_BASELINE_DIR} 
                           
                            exit
                            EOF
                        """

                    }
                    else {
                        echo 'Skip building the CMAPLE baseline'
                    }
                }
            }
        }
        stage("Build the latest CMAPLE") {
            steps {
                script {
                    if (params.BUILD_CMAPLE) {
                        echo 'Building CMAPLE'
                        // trigger jenkins cmaple-build
                        build job: 'cmaple-build', parameters: [string(name: 'BRANCH', value: CMAPLE_BRANCH),
                        booleanParam(name: 'USE_CIBIV', value: USE_CIBIV),]

                    }
                    else {
                        echo 'Skip building the latest CMAPLE'
                    }
                }
            }
        }
        stage("Download testing data & Infer ML trees") {
            steps {
                script {
                    if (params.DOWNLOAD_DATA || params.INFER_TREE) {
                        // trigger jenkins cmaple-tree-inference
                        build job: 'cmaple-tree-inference', parameters: [booleanParam(name: 'DOWNLOAD_DATA', value: DOWNLOAD_DATA),
                        booleanParam(name: 'INFER_TREE', value: INFER_TREE),
                        string(name: 'MODEL', value: MODEL),
                        booleanParam(name: 'USE_CIBIV', value: USE_CIBIV),
                        ]
                    }
                    else {
                        echo 'Skip inferring ML trees'
                    }
                }
            }
        }
        stage('Compute SPRTA by CMAPLE baseline') {
            steps {
                script {
                    if (params.COMPUTE_SPRTA_CMAPLE_BASELINE) {
                        sh """
                            ssh -tt ${NCI_ALIAS} ${SSH_COMP_NODE}<< EOF
                            sh ${SCRIPTS_DIR}/cmaple_baseline_compute_sprta.sh ${ALN_DIR} ${TREE_DIR} ${CMAPLE_BASELINE_PATH} ${ML_TREE_PREFIX} ${CMAPLE_BASELINE_TREE_PREFIX} ${params.MODEL} ${params.BLENGTHS_FIXED} ${params.NOT_REROOT} ${params.ZERO_LENGTH_BRANCHES} ${params.OUT_ALT_SPR}
                            exit
                            EOF
                        """
                    }
                    else {
                        echo 'Skip computing SPRTA by CMAPLE baseline'
                    }
                }
            }
        }
        stage('Compute SPRTA by the latest CMAPLE') {
            steps {
                script {
                    if (params.COMPUTE_SPRTA_CMAPLE) {
                        sh """
                            ssh -tt ${NCI_ALIAS} ${SSH_COMP_NODE}<< EOF
                            sh ${SCRIPTS_DIR}/cmaple_compute_sprta.sh ${ALN_DIR} ${TREE_DIR} ${CMAPLE_PATH} ${CMAPLE_BASELINE_TREE_PREFIX} ${CMAPLE_SPRTA_TREE_PREFIX} ${params.MODEL} ${params.BLENGTHS_FIXED} ${params.NOT_REROOT} ${params.ZERO_LENGTH_BRANCHES} ${params.OUT_ALT_SPR}
                            exit
                            EOF
                        """

                    }
                    else {
                        echo 'Skip computing SPRTA by the latest CMAPLE'
                    }
                }
            }
        }
        stage('Visualize SPRTA scores computed by the two versions of CMAPLE') {
            steps {
                script {
                    if (params.REMOVE_OUTPUT) {
                        sh """
                            ssh -tt ${NCI_ALIAS} << EOF
                            rm -f ${OUT_DIR}/*
                            exit
                            EOF
                        """
                        sh "rm -f {LOCAL_OUT_DIR}/*"
                    }
                    sh """
                        ssh -tt ${NCI_ALIAS} ${SSH_COMP_NODE}<< EOF
                                              
                        sh ${SCRIPTS_DIR}/extract_visualize_results.sh ${PYTHON_SCRIPT_PATH} ${TREE_DIR} ${OUT_DIR} ${CMAPLE_SPRTA_TREE_PREFIX} 
                        
                        exit
                        EOF
                        """
                    sh "mkdir -p {LOCAL_OUT_DIR} && rsync -avz --include=\"*/*\" ${NCI_ALIAS}:${OUT_DIR}/ ${LOCAL_OUT_DIR}"
                    sh "mkdir -p {LOCAL_OUT_DIR} && rsync -avz --include=\"*/*\" ${NCI_ALIAS}:${TREE_DIR} ${LOCAL_OUT_DIR}"
                    if (params.OUT_ALT_SPR)
                    {
                        sh "mkdir -p mkdir -p ${LOCAL_OUT_DIR}/tsv && rsync -avz --include=\"*tsv\" --exclude=\"*\" ${NCI_ALIAS}:${DATA_DIR}/aln/ ${LOCAL_OUT_DIR}/tsv/"
                    }
                }
            }
        }
        stage ('Verify') {
            steps {
                script {
                    sh """
                        ssh -tt ${NCI_ALIAS} << EOF
                        cd  ${WORKING_DIR}
                        echo "Files in ${WORKING_DIR}"
                        ls -ila ${WORKING_DIR}
                        echo "Files in ${ALN_DIR}"
                        ls -ila ${ALN_DIR}
                        echo "Files in ${TREE_DIR}"
                        ls -ila ${TREE_DIR}
                        exit
                        EOF
                        """
                }
            }
        }


    }
    post {
        always {
            echo 'Cleaning up workspace'
            cleanWs()
        }
    }
}

def void cleanWs() {
    // ssh to NCI_ALIAS and remove the working directory
    // sh "ssh -tt ${NCI_ALIAS} 'rm -rf ${REPO_DIR} ${BUILD_SCRIPTS}'"
}