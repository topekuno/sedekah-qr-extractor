import json

# File paths
input_file_path = 'Data Processing/Output JSON/refined_qr_data_processed_names.json'
output_file_path = 'Data Processing/Output JSON/refined_qr_data_processed.json'

def process_city(city):
    # Capitalize only the first letter of each word in the city name
    return ' '.join(word.capitalize() for word in city.lower().split())

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        item['city'] = process_city(item['city'])

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

# Main execution
process_file(input_file_path, output_file_path)
print(f"Updated data with processed city names has been written to {output_file_path}")