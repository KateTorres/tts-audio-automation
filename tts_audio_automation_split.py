import edge_tts
import os

def split_text_after_sentence(text):
    # This function splits text into two halves after completing a whole sentence.
    sentences = text.split('.')
    half_point = len(text) // 2

    first_half = ''
    second_half = ''

    char_count = 0
    for sentence in sentences:
        sentence = sentence.strip()
        if char_count + len(sentence) + 1 <= half_point or not second_half:
            first_half += sentence + '. '
            char_count += len(sentence) + 1
        else:
            second_half += sentence + '. '

    # Fallback if sentence-based splitting fails
    if not first_half.strip() or not second_half.strip():
        print("Warning: Fallback splitting used.")
        first_half = text[:half_point].strip()
        second_half = text[half_point:].strip()

    if not first_half or not second_half:
        raise ValueError("Failed to split text into two halves.")

    return first_half.strip(), second_half.strip()

def split_text_in_chunks(text, chunk_size):
    # Split text into chunks approximately equal to chunk_size while maintaining sentence boundaries
    sentences = text.split('.')
    chunks = []
    current_chunk = ''

    for sentence in sentences:
        sentence = sentence.strip()
        if len(current_chunk) + len(sentence) + 1 <= chunk_size:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '

    if current_chunk:
        chunks.append(current_chunk.strip())

    if not chunks:
        raise ValueError("Failed to split text into chunks.")

    return chunks

async def process_txt_files_edge(input_folder, output_folder, language='en', log_error=None, log_task_details=None):
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
            base_audio_filename = os.path.splitext(filename)[0]

            # Check file size and split if necessary
            file_size = os.path.getsize(file_path)

            if file_size < 1000 * 1024:  # Less than 1000kB
                # Save the spoken text to an audio file
                audio_filename = base_audio_filename + '.mp3'
                audio_path = os.path.join(output_folder, audio_filename)
                communicate = edge_tts.Communicate(text_content, voice)
                await communicate.save(audio_path)
                print(f'Successfully generated audio for {filename} as {audio_filename}')
            elif 1000 * 1024 <= file_size < 2000 * 1024:  # Between 1000kB and 2000kB
                try:
                    first_half, second_half = split_text_after_sentence(text_content)

                    # Generate first half audio
                    audio_filename_1 = base_audio_filename + '_part1.mp3'
                    audio_path_1 = os.path.join(output_folder, audio_filename_1)
                    communicate = edge_tts.Communicate(first_half, voice)
                    await communicate.save(audio_path_1)
                    print(f'Successfully generated audio for {filename} as {audio_filename_1}')

                    # Generate second half audio
                    audio_filename_2 = base_audio_filename + '_part2.mp3'
                    audio_path_2 = os.path.join(output_folder, audio_filename_2)
                    communicate = edge_tts.Communicate(second_half, voice)
                    await communicate.save(audio_path_2)
                    print(f'Successfully generated audio for {filename} as {audio_filename_2}')
                except ValueError as ve:
                    error_message = f"Error splitting text for {filename}: {ve}"
                    print(error_message)
                    if log_error:
                        log_error(error_message)
                    continue
            elif file_size >= 2000 * 1024:  # Greater than or equal to 2000kB
                try:
                    chunks = split_text_in_chunks(text_content, 800 * 1024)  # Approximately 800kB chunks

                    for i, chunk in enumerate(chunks[:-1]):
                        audio_filename = f"{base_audio_filename}_part{i + 1}.mp3"
                        audio_path = os.path.join(output_folder, audio_filename)
                        communicate = edge_tts.Communicate(chunk, voice)
                        await communicate.save(audio_path)
                        print(f'Successfully generated audio for {filename} as {audio_filename}')

                    # Handle the last chunk (split approximately in half)
                    last_chunk = chunks[-1]
                    first_half, second_half = split_text_after_sentence(last_chunk)

                    audio_filename_1 = f"{base_audio_filename}_part{len(chunks)}a.mp3"
                    audio_path_1 = os.path.join(output_folder, audio_filename_1)
                    communicate = edge_tts.Communicate(first_half, voice)
                    await communicate.save(audio_path_1)
                    print(f'Successfully generated audio for {filename} as {audio_filename_1}')

                    audio_filename_2 = f"{base_audio_filename}_part{len(chunks)}b.mp3"
                    audio_path_2 = os.path.join(output_folder, audio_filename_2)
                    communicate = edge_tts.Communicate(second_half, voice)
                    await communicate.save(audio_path_2)
                    print(f'Successfully generated audio for {filename} as {audio_filename_2}')
                except ValueError as ve:
                    error_message = f"Error splitting text into chunks for {filename}: {ve}"
                    print(error_message)
                    if log_error:
                        log_error(error_message)
                    continue
        except Exception as e:
            error_message = f"Error processing {filename}: {e}"
            print(error_message)
            if log_error:
                log_error(error_message)
            continue