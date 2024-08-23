# Sedekah QR Code Extractor

## Overview

This project provides a Python script for extracting QR code data and images from PDF files. This can be particularly useful for processing documents containing charitable donation information with QR codes. It was mainly used to extract this [pdf](https://www.muamalat.com.my/wp-content/uploads/2023/10/LIST-OF-QR-CODE-FOR-E-DERMA.pdf)


## Features

* Extracts QR code content (e.g., URLs, text) from PDF files.
* Saves extracted QR code images.
* Outputs extracted data in JSON format for easy integration with other systems. 
* Merge refined

## Requirements

* Python 3.7+
* Install the required Python packages:

  ```bash
  pip install -r requirements.txt

## Other Notes
* PDF to JSON to TS flow = qr_codes_with_images.py/qr_codes_only.py -> duitnow_qr_parser_state.py -> merge_ts_json_data.py
* You can customize the scripts with the input/output location if needed
* Made with help from Claude Sonnet 3.5 and ChatGPT 4o
