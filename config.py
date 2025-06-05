# config.py

# Azure OpenAI API configuration
API_ENDPOINT = "https://kfx-salesengineering.openai.azure.com/openai/deployments/SunilSharma/chat/completions?api-version=2025-01-01-preview"
API_KEY = "2681d84819354f08918bb1aab4c4d960"

# Prompt for extraction (hardcoded for one document type)
EXTRACTION_PROMPT = """
You will receive an image containing a scanned form with handwritten values.
Extract the following fields exactly as written, Work towards accuracy rather than speed. Keep in mind that the handwriting may vary in style and legibility and also keep in mind that this is an Australian form, so the handwriting may include Australian names and addresses.
The fields to extract are:
- Full Name
- Street Address
- Suburb
- Postcode
- Name of School
- Parent Name


Respond in JSON format:
{
  "Full Name": "",
  "Street Address": "",
  "Suburb": "",
  "Postcode": "",
  "Name of School": ""
  "Parent Name": ""
}
"""

# Labels for extraction fields in the form
EXTRACTION_FIELDS = [
    "Full Name",
    "Street Address",
    "Suburb",
    "Name of School",
    "Parent Name"
]

# Folder paths
FOLDER_INPUT = "folders/input"
FOLDER_INPROGRESS = "folders/inprogress"
FOLDER_PROCESSED = "folders/processed"
FOLDER_ERRORS = "folders/errors"

# Output CSV path
CSV_OUTPUT_PATH = "data/output.csv"
