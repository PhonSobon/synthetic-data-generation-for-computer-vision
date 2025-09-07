#!/bin/bash

# === CONFIGURATION ===
# The name for our tmux session.
SESSION_NAME="data_generator"
# The path to your virtual environment's activate script.
VENV_PATH="$HOME/venv/bin/activate" # Using $HOME is safer than ~ in scripts
# The number of images each Python process will generate.
CHUNK_SIZE=10000
# Your Python script's name.
PYTHON_SCRIPT="main.py"

# === SCRIPT LOGIC ===

# 1. Check for user input
if [ -z "$1" ]; then
    echo "Usage: ./generate.sh <total_images_to_generate>"
    echo "Example: ./generate.sh 50000"
    exit 1
fi

TOTAL_IMAGES=$1

# 2. Kill any old tmux session with the same name to start fresh
tmux has-session -t $SESSION_NAME 2>/dev/null
if [ $? == 0 ]; then
    echo "An old session named '$SESSION_NAME' was found. Killing it."
    tmux kill-session -t $SESSION_NAME
fi

# 3. Calculate the number of chunks needed
NUM_CHUNKS=$(( (TOTAL_IMAGES + CHUNK_SIZE - 1) / CHUNK_SIZE ))
echo "Total images to generate: $TOTAL_IMAGES"
echo "Chunk size: $CHUNK_SIZE"
echo "This will require $NUM_CHUNKS parallel processes."
echo "--------------------------------------------------"

# 4. Create the first tmux window and start the first process
START_INDEX=0
END_INDEX=$CHUNK_SIZE
if [ $END_INDEX -gt $TOTAL_IMAGES ]; then
    END_INDEX=$TOTAL_IMAGES
fi
# --- MODIFIED COMMAND ---
# Activate venv then run python
COMMAND_TO_RUN="source $VENV_PATH; python3 $PYTHON_SCRIPT $START_INDEX $END_INDEX 1"
echo "Starting process 1: $COMMAND_TO_RUN"
tmux new-session -d -s $SESSION_NAME -n "chunk_1" "$COMMAND_TO_RUN"

# 5. Loop to create the rest of the windows and processes
for (( i=1; i<NUM_CHUNKS; i++ ))
do
    START_INDEX=$(( i * CHUNK_SIZE ))
    END_INDEX=$(( (i + 1) * CHUNK_SIZE ))
    
    # Cap the end index for the very last chunk
    if [ $END_INDEX -gt $TOTAL_IMAGES ]; then
        END_INDEX=$TOTAL_IMAGES
    fi

    WINDOW_NAME="chunk_$((i+1))"
    # --- MODIFIED COMMAND ---
    # Activate venv then run python
    COMMAND_TO_RUN="source $VENV_PATH; python3 $PYTHON_SCRIPT $START_INDEX $END_INDEX 1"
    
    echo "Starting process $((i+1)): $COMMAND_TO_RUN"
    tmux new-window -t $SESSION_NAME -n "$WINDOW_NAME" "$COMMAND_TO_RUN"
done

echo "--------------------------------------------------"
echo "All generation processes have been started in the tmux session '$SESSION_NAME'."
echo "You can now safely disconnect from the server."