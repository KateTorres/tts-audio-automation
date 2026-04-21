import os
from tkinter import Tk, filedialog

def merge_mp3_files_selected(output_filename="merged_output.mp3", parent=None):
    """
    Prompts user to select multiple MP3 chunk files (named *_partX.mp3),
    sorts them by X, merges them, and optionally deletes originals.
    """
    from pydub import AudioSegment

    # Reuse existing Tk root or create one
    if parent is None:
        root = Tk()
        root.withdraw()
        own_root = True
    else:
        root = parent
        own_root = False
    root.lift()
    root.attributes("-topmost", True)
    root.update()

    selected_files = filedialog.askopenfilenames(
        parent=root,
        title="Select MP3 chunk files to merge (in *_partX.mp3 format)",
        filetypes=[("MP3 files", "*.mp3")]
    )

    if not selected_files:
        print("No files selected. Exiting.")
        if own_root:
            root.destroy()
        return

    def get_part_number(filename):
        basename = os.path.basename(filename)
        if "_part" in basename:
            try:
                part_str = basename.split("_part")[-1].split(".mp3")[0]
                return int(part_str)
            except ValueError:
                pass
        return float("inf")

    sorted_files = sorted(selected_files, key=get_part_number)

    output_path = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 files", "*.mp3")],
        title="Save merged MP3 as...",
        initialfile=output_filename
    )

    if not output_path:
        print("No output file selected. Exiting.")
        if own_root:
            root.destroy()
        return

    # Destroy Tk root before long-running merge and input() calls
    if own_root:
        root.destroy()

    combined = AudioSegment.empty()
    for file_path in sorted_files:
        print(f"Adding: {os.path.basename(file_path)}")
        combined += AudioSegment.from_mp3(file_path)

    combined.export(output_path, format="mp3")
    print(f"\n[V] Merged MP3 saved to: {output_path}")

    response = input("\nDo you want to delete the original chunk files? (Y/N): ").strip().lower()
    if response == 'y':
        for file_path in sorted_files:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
    else:
        print("Original chunk files were not deleted.")

if __name__ == "__main__":
    merge_mp3_files_selected()
    