import json

def get_state_from_postal_code(postal_code):
    # Mapping of postal code ranges to states in Malaysia
    state_mapping = {
        ('01000', '02000'): 'Perlis',
        ('05000', '09810'): 'Kedah',
        ('10000', '14400'): 'Penang',
        ('15000', '18500'): 'Kelantan',
        ('20000', '24300'): 'Terengganu',
        ('25000', '28800'): 'Pahang',
        ('30000', '36810'): 'Perak',
        ('39000', '39200'): 'Perak',
        ('40000', '48300'): 'Selangor',
        ('50000', '60000'): 'W.P. Kuala Lumpur',
        ('62000', '62988'): 'W.P. Putrajaya',
        ('63000', '68100'): 'Selangor',
        ('70000', '73509'): 'Negeri Sembilan',
        ('75000', '78309'): 'Melaka',
        ('79000', '86900'): 'Johor',
        ('87000', '91309'): 'Sabah',
        ('93000', '98859'): 'Sarawak',
        ('99000', '99999'): 'W.P. Labuan'
    }
    
    for (start, end), state in state_mapping.items():
        if start <= postal_code <= end:
            return state
    return 'Unknown'

def determine_category(merchant_name):
    merchant_name = merchant_name.lower()
    if 'masjid' in merchant_name or 'mosque' in merchant_name:
        return 'mosque'
    elif 'surau' in merchant_name:
        return 'surau'
    else:
        return 'others'

def parse_duitnow_qr(qr_content: str) -> dict:
    data = {}
    i = 0
    while i < len(qr_content):
        tag = qr_content[i:i+2]
        length = int(qr_content[i+2:i+4])
        value = qr_content[i+4:i+4+length]
        i += 4 + length

        if tag == '59':
            data['merchant_name'] = value
        elif tag == '60':
            data['merchant_city'] = value
        elif tag == '61':
            data['postal_code'] = value

    return data

def extract_duitnow_data(input_json_path: str, output_json_path: str):
    with open(input_json_path, 'r') as file:
        qr_codes = json.load(file)

    duitnow_data_list = []

    for qr in qr_codes:
        parsed_data = parse_duitnow_qr(qr['qrContent'])
        
        merchant_name = parsed_data.get('merchant_name', '')
        postal_code = parsed_data.get('postal_code', '')
        
        duitnow_data = {
            "id": qr['id'],
            "name": merchant_name,
            "category": determine_category(merchant_name),
            "state": get_state_from_postal_code(postal_code),
            "city": parsed_data.get('merchant_city', ''),
            "qrImage": qr['image'],
            "qrContent": qr['qrContent'],
        }
        
        # Optional fields
        if 'supported_payment' in qr:
            duitnow_data['supportedPayment'] = qr['supported_payment']
        if 'coords' in qr:
            duitnow_data['coords'] = qr['coords']
        
        duitnow_data_list.append(duitnow_data)

    with open(output_json_path, 'w') as file:
        json.dump(duitnow_data_list, file, indent=2)

    print(f"Extracted and parsed {len(duitnow_data_list)} DuitNow QR codes.")
    print(f"Results saved to {output_json_path}")

if __name__ == "__main__":
    input_json_path = "Data Processing/Output JSON/qr_codes_with_images_deduplicated.json"  # Your input file
    output_json_path = "Data Processing/Output JSON/refined_qr_data.json"
    extract_duitnow_data(input_json_path, output_json_path)