#!/bin/bash

# Input markdown file
md_file="everything_json.md"

# Counter for JSON files
counter=16

# Read the file line by line
while IFS= read -r line || [ -n "$line" ]; do
    # Check if line contains ```json
    if [[ $line == *'```json'* ]]; then
        # Create a new file for JSON content
        json_file="Group_${counter}.json"
        counter=$((counter + 1))
        
        # Read until closing ``` is found
        while IFS= read -r content || [ -n "$content" ]; do
            if [[ $content == '```' ]]; then
                break
            fi
            echo "$content" >> "$json_file"
        done
    fi
done < "$md_file"