import json
from collections import defaultdict

def remove_duplicates(input_json_path, output_json_path):
    # Read the input JSON file
    with open(input_json_path, 'r') as file:
        qr_codes = json.load(file)

    # Create a dictionary to store unique QR codes
    unique_qr_codes = defaultdict(list)

    # Group QR codes by their content
    for qr_code in qr_codes:
        unique_qr_codes[qr_code['qrContent']].append(qr_code)

    # Create a new list with duplicates removed
    deduplicated_qr_codes = []
    for qr_content, instances in unique_qr_codes.items():
        # Keep the first instance of each unique QR content
        deduplicated_qr_codes.append(instances[0])

    # Sort the deduplicated list by ID
    deduplicated_qr_codes.sort(key=lambda x: x['id'])

    # Reassign IDs to ensure they are sequential
    for new_id, qr_code in enumerate(deduplicated_qr_codes, start=1):
        qr_code['id'] = new_id

    # Write the deduplicated data to the output JSON file
    with open(output_json_path, 'w') as file:
        json.dump(deduplicated_qr_codes, file, indent=2)

    print(f"Removed {len(qr_codes) - len(deduplicated_qr_codes)} duplicates.")
    print(f"Deduplicated results saved to {output_json_path}")

    return deduplicated_qr_codes

def main(input_json_path, output_json_path):
    remove_duplicates(input_json_path, output_json_path)

if __name__ == "__main__":
    input_json_path = "Main_PDF_output.json"  # The output from the previous script
    output_json_path = "Main_PDF_output_deduplicate.json"
    main(input_json_path, output_json_path)