import os

# Define the list of topics with their numbers
# This dictionary maps the topic number to the topic name.
topics = {
    1: "Lines and Vocabulary",
    2: "Lines and Angles",
    3: "Perpendicular Angles (Right Angles)",
    4: "Acute and Obtuse Angles",
    5: "Angles and Parallel Lines",
    6: "Polygons and Vocabulary",
    7: "Degrees of a Triangle",
    8: "Sum of Interior Angles",
    9: "Interior Angle of Regular Polygon",
    10: "Sum of Exterior Angles",
    11: "Exterior Angle of Regular Polygon",
    12: "Types of Triangles",
    13: "Angle versus Side Length",
    14: "Possible Side Lengths of Triangle",
    15: "Area of a Triangle",
    16: "When are Triangles Congruent?",
    17: "The Pythagorean Theorem",
    18: "Euclid's Proof of a² + b² = c²",
    19: "Visual Proof of a² + b² = c²",
    20: "Pythagorean Triplets",
    21: "Are Pythagorean Triplets Infinite?",
    22: "30-60-90 Triangles"
}

# Create a mapping from keywords found in filenames to their corresponding topic numbers.
# This dictionary helps in matching video files to the numbered topics.
# The keys are substrings expected in the filenames, and the values are the topic numbers.
keyword_to_topic = {
    "30-60-90 Triangles": 22,
    "Pythagorean Triplets Infinite": 21,
    "Types of Triangles": 12,
    "Polygons and Vocabulary": 6,
    "Angle versus Side Length": 13,
    "Possible Side Lengths of a Triangle": 14,
    "Euclid's Proof of the Pythagorean Theorem": 18,
    "Exterior Angle of Regular Polygon": 11,
    "Sum of Exterior Angles": 10,
    "The Pythagorean Theorem": 17,
    "Pythagorean Triplets": 20,
    "Interior Angle of Regular Polygon": 9,
    "Area of a Triangle": 15,
    "Visual Proof of the Pythagorean Theorem": 19,
    "Sum of Interior Angles": 8,
    "When are Triangles Congruent": 16,
}

# --- Configuration ---
# Set the directory where your video files are located.
# IMPORTANT: Replace 'path/to/your/video/directory' with the actual path.
directory_path = '.'

# List of files to skip (e.g., quiz files, non-video files)
files_to_skip = [
    "PrepSwift Quant Tickbox Quiz 10 - Geometry Column 1 ( 1080p with 30fps ) .mp4",
    "PrepSwift Quant Tickbox Quiz 10 - Geometry Column 1.mp4",
    "combine.py"
]
# --- End Configuration ---


print(f"Processing files in directory: {directory_path}")

try:
    # Get a list of all files in the specified directory
    files_in_directory = os.listdir(directory_path)

    # Iterate through each file in the directory
    for filename in files_in_directory:
        # Construct the full path to the file
        old_filepath = os.path.join(directory_path, filename)

        # Skip directories and specified files
        if os.path.isdir(old_filepath) or filename in files_to_skip:
            print(f"Skipping: {filename}")
            continue

        matched = False
        # Convert filename to lowercase for case-insensitive matching
        filename_lower = filename.lower()

        # Iterate through the keywords to find a match in the filename
        for keyword, topic_number in keyword_to_topic.items():
            if keyword.lower() in filename_lower:
                # Construct the new filename with the number prefix
                # Uses zero-padding for single-digit numbers (e.g., 06 instead of 6)
                new_filename = f"{topic_number:02d} - {filename}"
                new_filepath = os.path.join(directory_path, new_filename)

                # Check if the new filename already exists to avoid overwriting
                if os.path.exists(new_filepath):
                    print(f"Skipping rename for '{filename}': Target file '{new_filename}' already exists.")
                else:
                    # Rename the file
                    try:
                        os.rename(old_filepath, new_filepath)
                        print(f"Renamed '{filename}' to '{new_filename}'")
                    except OSError as e:
                        print(f"Error renaming file '{filename}': {e}")

                matched = True
                break # Stop searching for keywords once a match is found

        # If no keyword match was found for the filename
        if not matched:
            print(f"No matching topic found for: {filename}")

except FileNotFoundError:
    print(f"Error: Directory not found at {directory_path}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("Script finished.")
