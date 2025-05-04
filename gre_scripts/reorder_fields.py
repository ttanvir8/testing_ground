import json
import glob
import os

def reorder_fields(data):
    required_fields = ['word', 'definition', 'concise_meaning', 'sentences', 'opposite_words', 'gre_synonyms']
    reordered_data = []
    
    for entry in data:
        reordered_entry = {field: entry[field] for field in required_fields}
        reordered_data.append(reordered_entry)
    
    return reordered_data

def process_files():
    # Get all Group_*.json files
    json_files = glob.glob('Group_*.json')
    
    for file_path in json_files:
        try:
            # Read the JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Reorder fields
            reordered_data = reorder_fields(data)
            
            # Write back to file with proper formatting
            with open(file_path, 'w') as f:
                json.dump(reordered_data, f, indent=2)
            
            print(f'Successfully processed {file_path}')
            
        except Exception as e:
            print(f'Error processing {file_path}: {str(e)}')

if __name__ == '__main__':
    process_files()