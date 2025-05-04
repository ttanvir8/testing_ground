import json
import glob
import os

def validate_word_entry(entry):
    required_fields = {
        'word',
        'definition',
        'concise_meaning',
        'sentences',
        'opposite_words',
        'gre_synonyms'
    }
    
    # Check if all required fields exist
    if not all(field in entry for field in required_fields):
        missing_fields = required_fields - set(entry.keys())
        return False, f'Missing fields: {missing_fields}'
    
    # Validate data types
    if not isinstance(entry['word'], str):
        return False, 'Word must be a string'
    if not isinstance(entry['definition'], str):
        return False, 'Definition must be a string'
    if not isinstance(entry['concise_meaning'], str):
        return False, 'Concise meaning must be a string'
    if not isinstance(entry['sentences'], list):
        return False, 'Sentences must be a list'
    if not isinstance(entry['opposite_words'], list):
        return False, 'Opposite words must be a list'
    if not isinstance(entry['gre_synonyms'], list):
        return False, 'GRE synonyms must be a list'
    
    return True, 'Valid'

def validate_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            return False, 'File must contain a list of word entries'
        
        # Check and convert 'synonyms' to 'gre_synonyms' if needed
        modified = False
        for entry in data:
            if 'synonyms' in entry and 'gre_synonyms' not in entry:
                entry['gre_synonyms'] = entry.pop('synonyms')
                modified = True
        
        # Save the modified data if changes were made
        if modified:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        
        for i, entry in enumerate(data):
            is_valid, message = validate_word_entry(entry)
            if not is_valid:
                return False, f'Entry {i} ({entry.get("word", "unknown")}) is invalid: {message}'
        
        return True, 'Valid'
    except json.JSONDecodeError as e:
        return False, f'Invalid JSON format: {str(e)}'
    except Exception as e:
        return False, f'Error processing file: {str(e)}'

def main():
    # Get all Group_*.json files
    files = glob.glob('Group_*.json')
    
    print('Validating JSON files...')
    print('-' * 50)
    
    all_valid = True
    for file in sorted(files):
        is_valid, message = validate_json_file(file)
        status = '✓' if is_valid else '✗'
        print(f'{status} {file}: {message}')
        if not is_valid:
            all_valid = False
    
    print('-' * 50)
    if all_valid:
        print('All files are valid and follow the same format!')
    else:
        print('Some files have format issues. Please check the details above.')

if __name__ == '__main__':
    main()