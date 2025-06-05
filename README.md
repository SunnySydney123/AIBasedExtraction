# AI-Based Extraction

A simple Python application in two parts:

- **main.exe** watches the `Input` folder. Any document dropped in there is picked up and forwarded to an Azure OpenAI endpoint (configured in `config.py`) with the prompt and required extraction fields.
- **validation.exe** is used to validate and update any extracted fields if necessary. The finalized data is then appended to a single CSV file.

---

## 📦 Requirements

- Python 3.x
- Use the provided `requirements.txt` file to install dependencies.

---

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SunnySydney123/AIBasedExtraction.git
   cd AIBasedExtraction
2. (Optional) Create a virtual environment:
python -m venv venv
3. Activate the virtual environment:
 .ON WIndows
 venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Run the application
python main.py
6. Run Validation
python validation.py
Project Structure
AIBasedExtraction/
│
├── main.py
├── validation.py
├── config.py
├── requirements.txt
├── .gitignore
├── README.md
├── Input/
├── Output/
└── venv/ (ignored)
🙌 Author
Sunil Sharma