from bs4 import BeautifulSoup
import re

def extract_words_by_day(html_file):
    """Extract GRE words grouped by day from GregMat HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    words_by_day = {}
    
    # Find all day sections - looking for GregMat's day markers
    day_sections = soup.find_all(['h2', 'h3'], 
                               string=re.compile(r'(day|week)\s+\d+', re.IGNORECASE))
    
    for section in day_sections:
        day_title = section.get_text().strip()
        words = []
        
        # Find words - look for the next unordered list which contains words
        word_container = section.find_next('ul')
        if word_container:
            word_elements = word_container.find_all('li')
            
            for element in word_elements:
                word_text = element.get_text().strip()
                # Clean up the text - remove numbers and special characters
                word_text = re.sub(r'^\d+\.\s*', '', word_text)  # Remove numbering
                word_text = re.sub(r'[^a-zA-Z\s-]', '', word_text)  # Keep only letters and hyphens
                word_text = word_text.strip()
                if word_text:
                    words.append(word_text)
        
        if words:
            words_by_day[day_title] = words
    
    return words_by_day

def extract_words_by_day(html_file):
    """Extract GRE words grouped by category from GregMat HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    words_by_group = {}
    
    # Find all group sections - looking for category headers
    group_headers = soup.find_all(['h3', 'h4'], 
                                string=re.compile(r'(basic|advanced|intermediate|hard|difficult|common)', re.IGNORECASE))
    
    for header in group_headers:
        group_title = header.get_text().strip()
        words = []
        
        # Find words - look for the next unordered list which contains words
        word_container = header.find_next('ul')
        if word_container:
            word_elements = word_container.find_all('li')
            
            for element in word_elements:
                word_text = element.get_text().strip()
                # Clean up the text - remove numbers and special characters
                word_text = re.sub(r'^\d+\.\s*', '', word_text)
                word_text = re.sub(r'[^a-zA-Z\s-]', '', word_text)
                word_text = word_text.strip()
                if word_text:
                    words.append(word_text)
        
        if words:
            words_by_group[group_title] = words
    
    return words_by_group

if __name__ == "__main__":
    html_file = "/Users/tanvirkhan/fun/testing_ground/gre_scripts/words.html"
    words_by_group = extract_words_by_day(html_file)
    
    # Print results with count
    for group, words in words_by_group.items():
        print(f"\n{group} ({len(words)} words):")
        for i, word in enumerate(words, 1):
            print(f"{i}. {word}")