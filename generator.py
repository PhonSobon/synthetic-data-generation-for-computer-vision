#!/usr/bin/env python3

import os
import math
import argparse
import subprocess

# === CONFIGURATION ===
# The name for our tmux session.
SESSION_NAME = "data_generator"
# The path to your virtual environment's activate script.
# os.path.expanduser handles the '~' correctly.
VENV_PATH = os.path.expanduser("~/py_env/normal/bin/activate")
# The number of images each Python process will generate.
CHUNK_SIZE = 10
# Your Python script's name.
PYTHON_SCRIPT = "main.py"


def main():
    """
    Main function to set up and run parallel processes in a tmux session.
    """
    # 1. Setup argument parser to get user input
    parser = argparse.ArgumentParser(
        description="Run multiple Python data generation scripts in parallel using tmux.",
        epilog="Example: python3 generate.py 50000"
    )
    parser.add_argument(
        "total_images",
        type=int,
        help="The total number of images to generate."
    )
    args = parser.parse_args()
    total_images = args.total_images

    # 2. Kill any old tmux session with the same name to start fresh
    # The 'capture_output=True' prevents the command's stdout/stderr from being printed.
    check_session_cmd = ["tmux", "has-session", "-t", SESSION_NAME]
    session_exists = subprocess.run(check_session_cmd, capture_output=True).returncode == 0

    if session_exists:
        print(f"An old session named '{SESSION_NAME}' was found. Killing it.")
        subprocess.run(["tmux", "kill-session", "-t", SESSION_NAME], check=True)

    # 3. Calculate the number of chunks needed
    # Using math.ceil ensures we have enough chunks for all images.
    num_chunks = math.ceil(total_images / CHUNK_SIZE)
    
    print(f"Total images to generate: {total_images}")
    print(f"Chunk size: {CHUNK_SIZE}")
    print(f"This will require {num_chunks} parallel processes.")
    print("--------------------------------------------------")

    # 4. Loop to create the tmux windows and start the processes
    for i in range(num_chunks):
        start_index = i * CHUNK_SIZE
        # Use min() to cap the end index for the very last chunk
        end_index = min((i + 1) * CHUNK_SIZE, total_images)

        window_name = f"chunk_{i + 1}"
        
        # This command will be run inside the shell started by tmux
        command_to_run = (
            f". {VENV_PATH}; "
            f"python3 {PYTHON_SCRIPT} {start_index} {end_index} 1"
        )
        
        print(f"Starting process {i + 1}: {command_to_run}")

        if i == 0:
            # Create the first window and the session itself
            tmux_cmd = [
                "tmux", "new-session", "-d",
                "-s", SESSION_NAME,
                "-n", window_name,
                command_to_run
            ]
        else:
            # Create subsequent windows in the existing session
            tmux_cmd = [
                "tmux", "new-window",
                "-t", SESSION_NAME,
                "-n", window_name,
                command_to_run
            ]
        
        # Run the appropriate tmux command
        subprocess.run(tmux_cmd, check=True)

    print("--------------------------------------------------")
    print(f"All generation processes have been started in the tmux session '{SESSION_NAME}'.")
    print("You can attach to it with: tmux attach-session -t data_generator")
    print("You can now safely disconnect from the server.")


if __name__ == "__main__":
    main()