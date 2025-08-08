import edge_tts
import os
import re
import time
from utils.progress import ProgressBar

MAX_EDGE_TTS_CHUNK = 4900  # Safe character limit to avoid truncation

def split_text_in_chunks(text, chunk_size=MAX_EDGE_TTS_CHUNK):
    """
    Splits text into chunks of approximately `chunk_size` characters, preserving sentence boundaries.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ''

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= chunk_size:
            current_chunk += sentence + ' '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ' '

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Optional: Merge final chunk if very small
    if len(chunks) >= 2 and len(chunks[-1]) < 1000 and len(chunks[-2]) + len(chunks[-1]) <= chunk_size:
        chunks[-2] += ' ' + chunks.pop()

    if not chunks:
        raise ValueError("Failed to split text into chunks.")

    return chunks

async def process_txt_files_edge(input_folder, output_folder, language='en', log_error=None, log_task_details=None):
    voice = "en-US-GuyNeural" if language == 'en' else "ru-RU-DmitryNeural"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    if not txt_files:
        print("No .txt files found in the specified folder.")
        return

    for filename in txt_files:
        file_path = os.path.join(input_folder, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()

            if not text_content.strip():
                print(f"Skipped {filename}: File is empty.")
                continue

            base_audio_filename = os.path.splitext(filename)[0]
            char_length = len(text_content)
            total_bytes = len(text_content.encode('utf-8'))

            if char_length <= MAX_EDGE_TTS_CHUNK:
                audio_filename = base_audio_filename + '.mp3'
                audio_path = os.path.join(output_folder, audio_filename)
                communicate = edge_tts.Communicate(text_content, voice)
                await communicate.save(audio_path)
                print(f"Generated single MP3: {audio_filename}")
            else:
                chunks = split_text_in_chunks(text_content, chunk_size=MAX_EDGE_TTS_CHUNK)
                progress = ProgressBar(total=total_bytes, prefix=f"Processing {filename}")
                processed_bytes = 0
                progress.update(0)  # ✅ Show progress bar at 0% immediately

                for i, chunk in enumerate(chunks):
                    audio_filename = f"{base_audio_filename}_part{i + 1}.mp3"
                    audio_path = os.path.join(output_folder, audio_filename)

                    communicate = edge_tts.Communicate(chunk, voice)
                    await communicate.save(audio_path)

                    processed_bytes += len(chunk.encode("utf-8"))
                    progress.update(processed_bytes)

                print(f"\nFinished generating audio for {filename} ({len(chunks)} chunks).")

        except Exception as e:
            error_message = f"Error processing {filename}: {e}"
            print(error_message)
            if log_error:
                log_error(error_message)
            continue
