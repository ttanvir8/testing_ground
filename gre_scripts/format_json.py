import json
import sys

def convert_to_standard_format(data):
    # If data is a dictionary, convert it to list format
    if isinstance(data, dict):
        result = []
        for word, details in data.items():
            # Handle cases where word has multiple meanings (e.g., "word (1)")
            if isinstance(details, dict):
                entry = details.copy()
                entry['word'] = word
                result.append(entry)
        return result
    return data

def standardize_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Convert to standard format
        standardized_data = convert_to_standard_format(data)
        
        # Write back to file with consistent formatting
        with open(file_path, 'w') as f:
            json.dump(standardized_data, f, indent=2)
        print(f'Successfully standardized {file_path}')
    except Exception as e:
        print(f'Error processing {file_path}: {str(e)}')

def needs_standardization(data):
    # Check if data is already in list format with 'word' field
    if isinstance(data, list):
        return not all('word' in item for item in data)
    return True

def main():
    import os
    import glob
    
    # Find all JSON files with Group_ prefix in current directory
    json_files = glob.glob('Group_*.json')
    
    if not json_files:
        print('No Group_*.json files found in current directory')
        return
    
    for file_path in json_files:
        try:
            # First check if file needs standardization
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            if needs_standardization(data):
                standardize_json_file(file_path)
            else:
                print(f'Skipping {file_path}: already in standard format')
        except Exception as e:
            print(f'Error checking {file_path}: {str(e)}')

if __name__ == '__main__':
    main()