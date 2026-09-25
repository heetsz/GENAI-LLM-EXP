# HR Helpdesk AI Assistant

A Streamlit chatbot that answers HR policy questions using the Google Gemini API and a constrained HR domain prompt.

## Setup

PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your Gemini API key to `.env`, then start the app:

```powershell
streamlit run app.py
```

Never commit `.env` or expose the API key publicly.