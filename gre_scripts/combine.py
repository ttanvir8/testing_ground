import os
import subprocess
import sys

def merge_video_audio(video_file, audio_file, output_file):
    """
    Merges video and audio files using ffmpeg and deletes original files upon success.

    Args:
        video_file (str): The path to the video file.
        audio_file (str): The path to the audio file.
        output_file (str): The desired path for the output merged file.
    """
    # Construct the ffmpeg command as a list of arguments
    command = [
        'ffmpeg',
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',  # Copy video stream without re-encoding
        '-c:a', 'copy',  # Copy audio stream without re-encoding
        output_file
    ]

    try:
        print(f"Merging video: '{video_file}' and audio: '{audio_file}' into '{output_file}'")
        # Execute the command
        # check=True will raise CalledProcessError if the command returns a non-zero exit code
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully merged '{output_file}'")

        # --- Deletion logic ---
        print(f"Attempting to delete original files: '{video_file}' and '{audio_file}'")
        try:
            os.remove(video_file)
            print(f"Deleted '{video_file}'")
        except OSError as e:
            print(f"Error deleting '{video_file}': {e}")

        try:
            os.remove(audio_file)
            print(f"Deleted '{audio_file}'")
        except OSError as e:
            print(f"Error deleting '{audio_file}': {e}")
        # --- End deletion logic ---


    except FileNotFoundError:
        print(f"Error: ffmpeg command not found.")
        print("Please ensure ffmpeg is installed and accessible in your system's PATH.")
        print("You can download ffmpeg from https://ffmpeg.org/download.html")
    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg execution for {output_file}:")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return code: {e.returncode}")
        print(f"Stderr:\n{e.stderr}")
        print(f"Stdout:\n{e.stdout}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_base_name(filename):
    """
    Extracts the base name from the video or audio filename.

    Args:
        filename (str): The name of the file.

    Returns:
        str: The base name of the file, or None if the format doesn't match.
    """
    if filename.endswith("-audio.mp4"):
        # Remove '-audio.mp4' from the end
        return filename[:-10]
    elif filename.endswith(" (1080p with 60fps).mp4"):
        # Remove ' (1080p with 60fps).mp4' from the end
        return filename[:-23]
    elif filename.endswith(" (1080p with 30fps).mp4"):
         # Remove ' (1080p with 30fps).mp4' from the end
         return filename[:-23]
    # Add other potential video suffixes here if needed
    else:
        return None

def main():
    """
    Finds video and audio pairs in the current directory, merges them,
    and deletes original files upon successful merging.
    """
    file_groups = {}
    current_directory = os.getcwd()

    print(f"Scanning directory: {current_directory}")

    # Group files by their base name
    for filename in os.listdir(current_directory):
        if os.path.isfile(filename) and filename.endswith('.mp4'):
            base_name = get_base_name(filename)
            if base_name:
                if base_name not in file_groups:
                    file_groups[base_name] = {'video': None, 'audio': None}

                if filename.endswith("-audio.mp4"):
                    file_groups[base_name]['audio'] = filename
                elif filename.endswith(" (1080p with 60fps).mp4") or filename.endswith(" (1080p with 30fps).mp4"):
                    file_groups[base_name]['video'] = filename

    # Process each group
    print("\nProcessing file groups...")
    for base_name, files in file_groups.items():
        video_file = files['video']
        audio_file = files['audio']
        output_file = f"{base_name}.mp4"

        if video_file and audio_file:
            # Check if the output file already exists
            if os.path.exists(output_file):
                print(f"Output file '{output_file}' already exists. Skipping merge for '{base_name}'.")
            else:
                # Call the merge function which now includes deletion on success
                merge_video_audio(video_file, audio_file, output_file)
        else:
            # Provide warnings for incomplete pairs
            if not video_file and not audio_file:
                 print(f"Warning: No video or audio file found for base name '{base_name}'. Skipping.")
            elif not video_file:
                print(f"Warning: No video file found for base name '{base_name}'. Found audio: '{audio_file}'. Skipping.")
            elif not audio_file:
                 print(f"Warning: No audio file found for base name '{base_name}'. Found video: '{video_file}'. Skipping.")

    print("\nScript finished.")

if __name__ == "__main__":
    main()