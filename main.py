# main.py

import os
import shutil
import requests
import base64
import json
import time
from datetime import datetime
from config import (
    API_ENDPOINT, API_KEY, EXTRACTION_PROMPT, EXTRACTION_FIELDS,
    FOLDER_INPUT, FOLDER_INPROGRESS, FOLDER_PROCESSED, FOLDER_ERRORS
)

# Ensure required folders exist
def ensure_folders():
    for folder in [FOLDER_INPUT, FOLDER_INPROGRESS, FOLDER_PROCESSED, FOLDER_ERRORS, "folders/log"]:
        os.makedirs(folder, exist_ok=True)

# Detect image files in input folder
def get_image_files():
    return [f for f in os.listdir(FOLDER_INPUT) if f.lower().endswith(('.png', '.jpg'))]

# Write log entry
def log_event(file_name, status, tokens_used="N/A"):
    log_folder = "folders/log"
    log_file = os.path.join(log_folder, "process_log.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} | {file_name} | {status} | Tokens: {tokens_used}\n"
    with open(log_file, "a") as f:
        f.write(log_line)

# Send image to Azure OpenAI Vision API and get extracted data
def extract_data_from_image(image_path):
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": EXTRACTION_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/tiff;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4000
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        extracted_content = result["choices"][0]["message"]["content"]
        usage_tokens = result.get("usage", {}).get("total_tokens", "N/A")
        return extracted_content, usage_tokens
    else:
        print(f"API request failed: {response.status_code}, {response.text}")
        return None, None

# Process files: extract data and move to InProgress
def process_files():
    image_files = get_image_files()

    for file_name in image_files:
        input_path = os.path.join(FOLDER_INPUT, file_name)
        print(f"Processing {file_name}")

        try:
            extracted_data, tokens_used = extract_data_from_image(input_path)

            if extracted_data:
                base_name = os.path.splitext(file_name)[0]
                json_path = os.path.join(FOLDER_INPROGRESS, f"{base_name}.json")
                image_dest_path = os.path.join(FOLDER_INPROGRESS, file_name)

                # Save extracted data JSON
                with open(json_path, "w") as json_file:
                    json.dump(json.loads(extracted_data), json_file, indent=4)

                # Move image to InProgress
                shutil.move(input_path, image_dest_path)

                log_event(file_name, "PASS", tokens_used)
                print(f"Moved {file_name} and JSON to InProgress. Tokens used: {tokens_used}")

            else:
                shutil.move(input_path, os.path.join(FOLDER_ERRORS, file_name))
                log_event(file_name, "ERROR")
                print(f"Extraction failed for {file_name}. Moved to Errors.")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            shutil.move(input_path, os.path.join(FOLDER_ERRORS, file_name))
            log_event(file_name, "ERROR")

if __name__ == "__main__":
    ensure_folders()

    print("Watching for new image files in input folder...")

    while True:
        process_files()
        time.sleep(5)  # Check every 5 seconds
