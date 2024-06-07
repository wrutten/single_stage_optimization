#!/bin/bash

# Define the parent directory and Python script
PARENT_DIR="results/QH_BenchmarkScan_3"
PYTHON_SCRIPT="plot.py"

# Loop through all subdirectories of the parent directory
for SUBDIR in "$PARENT_DIR"/*/; do
    if [ -d "$SUBDIR" ]; then
        # Get the name of the subdirectory
        SUBDIR_NAME=$(basename "$SUBDIR")

        # Define the log file name
        LOG_FILE="$PARENT_DIR/$SUBDIR_NAME/log_${PYTHON_SCRIPT}.txt"

        # Run the Python script on the subdirectory and log the output along with timing
        {
            echo "Running $PYTHON_SCRIPT on $SUBDIR_NAME"
            start_time=$(date +%s)
            python "$PYTHON_SCRIPT" "$SUBDIR"
            end_time=$(date +%s)
            runtime=$((end_time - start_time))
            echo "Execution time: $runtime seconds"
        } > "$LOG_FILE" 2>&1
    fi
done

