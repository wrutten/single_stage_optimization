#!/bin/bash

# Define the parent directory and Python script
ROOT="results"
PARENT_DIR="QH_QFM_test2"
PYTHON_SCRIPT="plot"

echo "Looping over all subdirectories"
# Loop through all subdirectories of the parent directory
for SUBDIR in "$ROOT/$PARENT_DIR"/*/; do
    if [ -d "$SUBDIR" ]; then
        # Get the name of the subdirectory
        SUBDIR_NAME=$(basename "$SUBDIR")

        # Define the log file name
        LOG_FILE="$ROOT/$PARENT_DIR/$SUBDIR_NAME/log_${PYTHON_SCRIPT}.txt"

        # Run the Python script on the subdirectory and log the output along with timing
        echo "Running $PYTHON_SCRIPT.py on $ROOT/$PARENT_DIR/$SUBDIR_NAME"
        start_time=$(date +%s)
        {
        echo "Running $PYTHON_SCRIPT.py on $ROOT/$PARENT_DIR/$SUBDIR_NAME"  
        python "$PYTHON_SCRIPT".py "--results_folder" "$PARENT_DIR/$SUBDIR_NAME"
        end_time=$(date +%s)
        runtime=$((end_time - start_time))
        echo "Execution time: $runtime seconds"
       } > "$LOG_FILE" 2>&1
        echo "Execution time: $runtime seconds"
    fi
done

