#from tts_audio_automation_split import process_txt_files
from tts_audio_automation_split import process_txt_files_edge
from tkinter import Tk, filedialog
import asyncio
import time
import os

# Create or append log file
def log_error(message):
    if not os.path.exists("log.txt"):
        open("log.txt", "w", encoding="utf-8").close()  # Create the log file if it does not exist
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")

def log_task_details(task_details):
    if not os.path.exists("log.txt"):
        open("log.txt", "w", encoding="utf-8").close()  # Create the log file if it does not exist
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(task_details + "\n")

async def main_async():
    # Use Tkinter to open a file dialog for user-selected directories
    Tk().withdraw()  # Hide the root window

    # Ask the user to select the input directory
    input_folder = filedialog.askdirectory(title="Select Directory Containing .txt Files")
    if not input_folder:
        print("No input directory selected. Exiting...")
        return

    # Ask the user to select the output directory
    output_folder = filedialog.askdirectory(title="Select Directory to Save .mp3 Files")
    if not output_folder:
        print("No output directory selected. Exiting...")
        return

    # Prompt the user to select the language
    language = input("Select the language (en for English, ru for Russian): ").strip().lower()
    if language not in ['en', 'ru']:
        print("Invalid language selection. Defaulting to English.")
        language = 'en'

    # Call the processing function with asyncio for Edge TTS
    try:
        task_start_time = time.time()
        log_task_details(f"Task started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        await process_txt_files_edge(
            input_folder=input_folder,
            output_folder=output_folder,
            language=language,
            log_error=log_error,
            log_task_details=log_task_details
        )
        task_duration = time.time() - task_start_time
        log_task_details(f"Task completed in {task_duration:.2f} seconds.")
        print("All files have been processed successfully.")
    except Exception as main_error:
        log_error(f"An unexpected error occurred: {main_error}")
        print(f"An unexpected error occurred: {main_error}")

if __name__ == "__main__":
    asyncio.run(main_async())