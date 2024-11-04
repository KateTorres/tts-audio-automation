#from tts_audio_automation import process_txt_files
from tts_audio_automation import process_txt_files_edge
from tkinter import Tk, filedialog
import asyncio

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
    await process_txt_files_edge(input_folder, output_folder, language)

    #try:
    #    process_txt_files(input_folder, output_folder, language)
    #    print("All files have been processed successfully.")
    #except Exception as main_error:
    #    print(f"An unexpected error occurred: {main_error}")

if __name__ == "__main__":
    asyncio.run(main_async())