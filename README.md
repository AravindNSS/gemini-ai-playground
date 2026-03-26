# GemmaScripts

A simple Python script that uses the Google Gemini API to generate content using the Gemma model.

## Prerequisites

- Python 3.8 or higher installed on your machine
- A valid Google Gemini API key

## Setup

### 1. Clone or download this repository

### 2. Create the virtual environment

Open a terminal in the project folder and run:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

Once activated, you should see `(.venv)` at the beginning of your terminal prompt.

### 4. Install dependencies

```powershell
pip install google-genai
```

### 5. Set your API key

Open `gemma.py` and replace the placeholder in the following line with your actual API key:

```python
client = genai.Client(api_key="YOUR_API_KEY_HERE")
```

### 6. Run the script

```powershell
python gemma.py
```

## Deactivating the virtual environment

When you're done, deactivate the virtual environment by running:

```powershell
deactivate
```
