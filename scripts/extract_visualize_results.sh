#!bin/bash

###### handle arguments ######
PYTHON_SCRIPT_PATH=$1 # path to the python script
TREE_DIR=$2 # tree dir
OUT_DIR=$3 # output dir
CMAPLE_SPRTA_TREE_PREFIX=$4 # The prefix of trees with SPRTA computed by CMAPLE


### pre steps #####
#module load python3/3.9.2
module load python3
chmod +x ${PYTHON_SCRIPT_PATH}


############
mkdir -p ${OUT_DIR}

for tree_path in "${TREE_DIR}"/${CMAPLE_SPRTA_TREE_PREFIX}*.treefile.nexus; do
	tree=$(basename "$tree_path")
    echo "Extract results from ${tree} and visualize them to ${OUT_DIR}/${tree}.png"
    echo "cd ${OUT_DIR} && python3 ${PYTHON_SCRIPT_PATH} --input ${TREE_DIR}/${tree} --output ${OUT_DIR}/${tree}"
    cd ${OUT_DIR} && python3 ${PYTHON_SCRIPT_PATH} --input ${TREE_DIR}/${tree} --output ${OUT_DIR}/${tree}
done
                        