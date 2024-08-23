# Sedekah QR Code Extractor

## Overview

This project provides a Python script for extracting QR code data and images from PDF files. This can be particularly useful for processing documents containing charitable donation information with QR codes. It was mainly used to extract this [pdf](https://www.muamalat.com.my/wp-content/uploads/2023/10/LIST-OF-QR-CODE-FOR-E-DERMA.pdf). It only extracts data from the QR Code itself and not from the text inside the PDF.

Scripts used to process the PDF:
qr_codes_with_images.py/qr_codes_only.py -> duitnow_qr_parser_state.py -> merge_ts_json_data.py


## Features

* Extracts QR code content (e.g., URLs, text) from PDF files.
* Saves extracted QR code images.
* Outputs extracted data in JSON format for easy integration with other systems.
* Merges easily with institutions.ts in sedekah-je repo

## Requirements

* Python 3.7+
* Install the required Python packages:

  ```bash
  pip install -r requirements.txt

## Other Notes
* It flows from PDF to JSON to TS
* You can customize the scripts with the input/output location if needed
* Made with help from Claude Sonnet 3.5 and ChatGPT 4o

[TODO] add documentation for the scripts
