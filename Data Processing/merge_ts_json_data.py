import json
import re

# File paths (you can modify these as needed)
existing_file_path = 'institutions.ts'
new_data_file_path = 'Data Processing/Output JSON/refined_qr_data_processed.json'
output_file_path = 'Final Output/updated_institutions.ts'

def read_ts_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Extract the array content
    match = re.search(r'export const institutions: Institution\[] = (\[[\s\S]*?\]);', content)
    if match:
        return match.group(1)
    return '[]'

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def merge_data(existing_data_string, new_data):
    # Extract existing qrContents and find the highest ID
    existing_qr_contents = re.findall(r'qrContent:\s*"([^"]*)"', existing_data_string)
    existing_qr_contents = set(existing_qr_contents)
    highest_id = max(map(int, re.findall(r'id:\s*(\d+)', existing_data_string)), default=0)

    # Prepare new entries
    new_entries = []
    for new_item in new_data:
        if new_item['qrContent'] not in existing_qr_contents:
            highest_id += 1
            new_entry = f"""  {{
    id: {highest_id},
    name: "{new_item['name']}",
    category: "{new_item['category']}",
    state: "{new_item['state']}",
    city: "{new_item['city']}",
    qrImage: "",
    qrContent: "{new_item['qrContent']}",
    supportedPayment: ["duitnow", "tng"],
  }},"""
            new_entries.append(new_entry)

    # Insert new entries at the end of the existing data
    if new_entries:
        insert_position = existing_data_string.rfind(']')
        updated_data = (
            existing_data_string[:insert_position] +
            ',\n' +
            '\n'.join(new_entries) +
            existing_data_string[insert_position:]
        )
        return updated_data
    return existing_data_string

def write_ts_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("import type { Institution } from \"../types/institutions\";\n\n")
        file.write(f"export const institutions: Institution[] = {data};")

# Main execution
existing_data = read_ts_file(existing_file_path)
new_data = read_json_file(new_data_file_path)
merged_data = merge_data(existing_data, new_data)
write_ts_file(merged_data, output_file_path)

print(f"Updated data has been written to {output_file_path}")
print(f"New entries added: {len(new_data) - len(set(re.findall(r'qrContent:\s*"([^"]*)"', existing_data)))}")