# TTS-Audio-Automation

## Overview
**TTS-Audio-Automation** is a Python-based tool that automates the process of converting `.txt` files into high-quality audio files using text-to-speech (TTS) technology. 

## Features
- **Batch processing of `.txt` files**: Reads all text files from a specified folder and converts them into audio files.
- **Audio output**: Saves the generated audio in `.mp3` format.
- **Extensible**: Can be enhanced to include automatic upload to Google Drive and email integration for sharing links.
- Option to choose between English and Russian languages.
- Configurable to set a male voice as default for Russian text.
- Cross-platform support (Windows and Linux).
- Integration with `tkinter` for user-friendly directory selection.

## Installation
1. Ensure `ffmpeg` is installed for audio processing with `pydub`.

## Dependencies
- **Python 3.7+**
- **edge-tts**: Primary TTS library for high-quality voice synthesis
- **pydub**: For audio processing
- **ffmpeg**: Required by `pydub` for audio export

## Usage
1. Place your `.txt` files in the `input` folder (or specify a custom input path).
2. Run the script:
   python tts_automation.py
   Generated `.mp3` files will be saved in the `output` folder.

## Customization
- **Speech properties**: Modify `engine.setProperty('rate', value)` and `engine.setProperty('volume', value)` in the script to change the rate and volume.
- **Output directory**: Change the `output_folder` path in the script to specify where audio files should be saved.

## Future Enhancements
- **Google Drive Integration**: Automate file uploads to Google Drive and generate shareable links using the Google Drive API.
- **Email Notifications**: Send audio file links via email using `smtplib` or a third-party service like `SendGrid`.
- **Docker Containerization**: Package the application in a Docker container for easy deployment.
- **AWS Integration**: Use AWS Lambda to trigger the script automatically and AWS S3 for cloud storage.

## Contributing
Contributions are welcome! If you have suggestions or improvements, please submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
