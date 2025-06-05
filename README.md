# My Python App

A simple Python application in two parts, the main.exe will watch the Input folder, any document dropped in there will be picked up and forwarded to Azure Open AI endpoint configured in config.py with the prompt and extraction fields required. A second application validation.exe is used to validate and update if required any fields and the data is pushed to a single csv file.

## 📦 Requirements

- Python 3.x
- use the requirments.txt file

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/SunnySydney123/AIBasedExtraction.git
   cd AIBasedExtraction
# Optionally create virtual enviornment
   python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
# Install dependencies
pip install -r requirements.txt
# Run
python main.py
python validation.py

🙌 Author : Sunil Sharma