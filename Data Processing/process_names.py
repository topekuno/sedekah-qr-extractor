import json
import re

# File paths
input_file_path = 'Data Processing/Output JSON/refined_qr_data.json'
output_file_path = 'Data Processing/Output JSON/refined_qr_data_processed_names.json'

def expand_abbreviation(word):
    abbreviations = {
        "MJD": "Masjid",
        "MSJD": "Masjid",
        "SR": "Surau",
        "SUR": "Surau",
        "TB": "Tabung",
        "TBG": "Tabung",
        "PBGN": "Pembangunan",
        "PBN": "Pembangunan",
        "KG": "Kampung",
        "TMN": "Taman",
        "SEK": "Sekolah",
        "SK": "Sekolah Kebangsaan",
        "SMK": "Sekolah Menengah Kebangsaan",
        "KPLKS": "Kompleks",
        "MT": "Madrasah Tahfiz",
        "MD": "Madrasah",
        "BT": "Batu",
    }
    return abbreviations.get(word.upper(), word)

def process_name(name):
    words = re.split(r'(\s+|-)', name)
    processed_words = []
    
    for word in words:
        expanded_word = expand_abbreviation(word)
        if word.isspace() or word == '-':
            processed_words.append(word)
        else:
            processed_words.append(expanded_word.capitalize())
    
    return ''.join(processed_words)

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        item['name'] = process_name(item['name'])

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

# Main execution
process_file(input_file_path, output_file_path)
print(f"Updated data with processed names has been written to {output_file_path}")