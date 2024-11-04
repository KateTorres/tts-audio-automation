#import pyttsx3
import edge_tts
import os
import asyncio

#def set_language_voice(engine, language='en'):
#    voices = engine.getProperty('voices')
#    for voice in voices:
#        if language == 'ru' and ('russian' in voice.name.lower() or 'ru' in voice.id.lower()):
#            engine.setProperty('voice', voice.id)
#            print(f"Russian voice set: {voice.name}")
#            return True
#        elif language == 'en' and ('english' in voice.name.lower() or 'en' in voice.id.lower()):
#            engine.setProperty('voice', voice.id)
#            print(f"English voice set: {voice.name}")
#            return True
#    print(f"No {language} voice found. Using default voice.")
#    return False

#def process_txt_files(input_folder, output_folder, language='en'):
#    try:
#        # Initialize the TTS engine
#        engine = pyttsx3.init()
#        set_language_voice(engine, language)  # Set the selected language voice
#
#        engine.setProperty('rate', 150)  # Set speech rate
#        engine.setProperty('volume', 1.0)  # Set volume level

async def process_txt_files_edge(input_folder, output_folder, language='en'):
    # Map language to the desired voice
    voice = "en-US-GuyNeural" if language == 'en' else "ru-RU-DmitryNeural"

        # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each .txt file in the folder
    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    if not txt_files:
        print("No .txt files found in the specified folder.")
        return

    for filename in txt_files:
        file_path = os.path.join(input_folder, filename)
        try:
            # Read the content of the .txt file
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()

            # Handle empty files
            if not text_content.strip():
                print(f"Skipped {filename}: File is empty.")
                continue

            # Set the name for the output audio file
            audio_filename = os.path.splitext(filename)[0] + '.mp3'
            audio_path = os.path.join(output_folder, audio_filename)

            # Save the spoken text to an audio file
            #engine.save_to_file(text_content, audio_path)
            #engine.runAndWait()

            # Initialize the TTS engine and save the output
            communicate = edge_tts.Communicate(text_content, voice)
            await communicate.save(audio_path)            

            print(f'Successfully generated audio for {filename} as {audio_filename}')
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

        except Exception as e:
            print(f"An error occurred during the process: {e}")