# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-07-25

**Reason for modificatrion** : There was a change in edge-tts or my environment. Files started to cut off before reaching the end. Troubleshooting revealed that file splitting no longer worked based on size in bytes.
### Correction
- len(text_content) was intriduced instead of os.path.getsize(file_path) to guide splitting decisions.
- Text is now split by 4900 bites (i.e every 4900 bites a new ..._partX.mp3 is created).

### Added
- `utils/progress.py`: New ProgressBar class that tracks byte-accurate progress.
- `utils/merge_mp3.py`: New utility for merging multiple _partX.mp3 chunk files into one. This module can be run independantly. Otherwise it runs automatically from main.
    - GUI-based multi-file selection for mp3 chunks
    - Sorting by chunk number
    - Optional deletion of original files after the merge. 
      (This option will be later automated. So far I have been merging 50-80 individual text files chunks to create 100-150 kB mp3 file, which is the preferred mp3 size for the target audience of this program).


### Changed
- Updated `process_txt_files_edge()` in `tts_audio_automation_split.py`:
  - Uses character count instead of file size for splitting logic.
  - Increased chunk size limit to `MAX_EDGE_TTS_CHUNK = 4900` for fewer, larger audio files.
  - Progress bar now appears immediately at 0% before the first chunk is processed.

### Fixed
- Prevented merge prompt when only 1 or 0 `.mp3` files are created.
- Ensured all imports (e.g., `time`) are correctly declared in `progress.py` and `tts_audio_automation_split.py`.

### Removed
- Legacy sentence-based splitting logic that used `split_text_after_sentence()`.

## [Planned]
- Merge menu gets stuck in the back, need to bring it to the front by deault
- Create virtual environment

