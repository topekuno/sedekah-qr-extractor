import fitz  # PyMuPDF
import io
from PIL import Image
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import json

def extract_qr_codes(pdf_path):
    results = []
    qr_id = 1
    seen_qr_codes = set()  # Set to keep track of unique QR codes

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Get the list of images on the page
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Convert image bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert PIL Image to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Decode QR codes
            decoded_objects = decode(cv_image)
            
            for qr_code in decoded_objects:
                qr_data = qr_code.data.decode('utf-8')
                if qr_data not in seen_qr_codes:  # Check if this QR code is new
                    seen_qr_codes.add(qr_data)  # Add to set of seen QR codes
                    results.append({
                        "id": qr_id,
                        "qrContent": qr_data
                    })
                    qr_id += 1

    pdf_document.close()
    return results

def main(pdf_path, output_json_path):
    qr_codes = extract_qr_codes(pdf_path)
    
    with open(output_json_path, 'w') as json_file:
        json.dump(qr_codes, json_file, indent=2)

    print(f"Extracted {len(qr_codes)} unique QR codes. Results saved to {output_json_path}")

if __name__ == "__main__":
    pdf_path = "PDF Files/Main_PDF.pdf" # Input PDF file
    output_json_path = "Data Extraction/Output JSON/qr_codes_only.json" # Output JSON file
    main(pdf_path, output_json_path)