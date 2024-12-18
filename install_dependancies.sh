#!/bin/bash

# Navigate to the script directory
cd "$(dirname "$0")"

# Display Python version for confirmation
echo "Using Python version:"
python3 --version || { echo "Python3 is not installed or not in PATH. Please install Python3."; exit 1; }

# Check if dependencies need to be installed
if [ ! -f "install_dependancies.sh" ]; then
    echo "Dependency installation script not found. Ensure dependencies are installed manually."
else
    echo "Running install_dependancies.sh to check and install necessary dependencies..."
    ./install_dependancies.sh
fi

# Run the main Python script (now main.py)
echo "Running TTS Audio Automation..."
python3 main.py

# Check if the Python script ran successfully
if [ $? -eq 0 ]; then
    echo "TTS Audio Automation completed successfully."
else
    echo "TTS Audio Automation encountered an error. Check the output for more details."
fi

# Wait for user input before closing (optional)
read -p "Press any key to continue..."