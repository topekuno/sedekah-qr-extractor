import fitz  # PyMuPDF
import io
from PIL import Image
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import json
import os
import hashlib

def extract_and_save_qr_images(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    results = []
    qr_id = 1
    image_hashes = set()

    pdf_document = fitz.open(pdf_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            
            image = Image.open(io.BytesIO(image_bytes))
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            decoded_objects = decode(cv_image)
            
            for qr_code in decoded_objects:
                qr_data = qr_code.data.decode('utf-8')
                
                # Get QR code location
                points = qr_code.polygon
                if len(points) > 4:
                    hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                    points = hull
                
                # Crop the QR code from the image
                x, y, w, h = cv2.boundingRect(np.array([point for point in points], dtype=np.float32))
                qr_image = cv_image[y:y+h, x:x+w]
                
                # Convert to PIL Image for saving
                qr_pil_image = Image.fromarray(cv2.cvtColor(qr_image, cv2.COLOR_BGR2RGB))
                
                # Generate hash of the image
                img_hash = hashlib.md5(qr_pil_image.tobytes()).hexdigest()
                
                if img_hash not in image_hashes:
                    image_hashes.add(img_hash)
                    
                    # Save the image
                    image_filename = f"QR_{qr_id}.png"
                    qr_pil_image.save(os.path.join(output_folder, image_filename))
                    
                    results.append({
                        "id": qr_id,
                        "qrContent": qr_data,
                        "image": image_filename
                    })
                    qr_id += 1

    pdf_document.close()
    return results

def main(pdf_path, output_folder, json_output_path):
    qr_codes = extract_and_save_qr_images(pdf_path, output_folder)
    
    with open(json_output_path, 'w') as json_file:
        json.dump(qr_codes, json_file, indent=2)

    print(f"Extracted {len(qr_codes)} unique QR code images.")
    print(f"Images saved to {output_folder}")
    print(f"Results saved to {json_output_path}")

if __name__ == "__main__":
    pdf_path = "Main_PDF.pdf"
    output_folder = "QR_images"
    json_output_path = "qr_codes_with_images.json"
    main(pdf_path, output_folder, json_output_path)