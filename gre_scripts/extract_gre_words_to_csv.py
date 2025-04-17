from bs4 import BeautifulSoup
import re
import pandas as pd
import os

def extract_words_by_group(html_file):
    """Extract GRE words grouped by category from GregMat HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    words_by_group = {}
    
    # Try to find group sections by different patterns
    # First try to find by day/week pattern
    day_sections = soup.find_all(['h2', 'h3', 'h4'], 
                               string=re.compile(r'(day|week)\s+\d+', re.IGNORECASE))
    
    if day_sections:
        # Process day/week sections
        for section in day_sections:
            group_title = section.get_text().strip()
            words = extract_words_from_section(section)
            if words:
                words_by_group[group_title] = words
    else:
        # Try to find by difficulty level pattern
        group_headers = soup.find_all(['h2', 'h3', 'h4'], 
                                    string=re.compile(r'(basic|advanced|intermediate|hard|difficult|common)', re.IGNORECASE))
        
        if group_headers:
            # Process difficulty level sections
            for header in group_headers:
                group_title = header.get_text().strip()
                words = extract_words_from_section(header)
                if words:
                    words_by_group[group_title] = words
        else:
            # If no specific headers found, try to find all unordered lists
            uls = soup.find_all('ul')
            for i, ul in enumerate(uls):
                # Use a generic group name
                group_title = f"Group {i+1}"
                words = []
                word_elements = ul.find_all('li')
                
                for element in word_elements:
                    word_text = clean_word_text(element.get_text().strip())
                    if word_text:
                        words.append(word_text)
                
                if words:
                    words_by_group[group_title] = words
    
    return words_by_group

def extract_words_from_section(section):
    """Extract words from a section following a header"""
    words = []
    
    # Find words - look for the next unordered list which contains words
    word_container = section.find_next('ul')
    if word_container:
        word_elements = word_container.find_all('li')
        
        for element in word_elements:
            word_text = clean_word_text(element.get_text().strip())
            if word_text:
                words.append(word_text)
    
    return words

def clean_word_text(word_text):
    """Clean up the word text by removing numbers and special characters"""
    # Remove numbering
    word_text = re.sub(r'^\d+\.\s*', '', word_text)
    # Keep only letters, spaces, and hyphens
    word_text = re.sub(r'[^a-zA-Z\s-]', '', word_text)
    return word_text.strip()

def save_to_csv(words_by_group, output_file):
    """Save the extracted words to a CSV file"""
    # Find the maximum number of words in any group
    max_words = max(len(words) for words in words_by_group.values())
    
    # Create a DataFrame with columns for each group
    data = {}
    for group, words in words_by_group.items():
        # Pad the list with empty strings if needed
        padded_words = words + [''] * (max_words - len(words))
        data[group] = padded_words
    
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Words saved to {output_file}")

def main():
    html_file = "/Users/tanvirkhan/fun/testing_ground/gre_scripts/words.html"
    output_file = "/Users/tanvirkhan/fun/testing_ground/gre_scripts/gre_words.csv"
    
    # Extract words by group
    words_by_group = extract_words_by_group(html_file)
    
    # Print summary
    print("\nWords extracted by group:")
    for group, words in words_by_group.items():
        print(f"\n{group} ({len(words)} words)")
    
    # Save to CSV
    save_to_csv(words_by_group, output_file)

if __name__ == "__main__":
    main()