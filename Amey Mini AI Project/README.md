# AI Citizen Services Assistant — BCA Mini Project

A beginner-friendly Streamlit web app that helps users discover Indian public-service portals, read basic guidance, and prepare document checklists.

## Features
- Search public-service portals by keyword
- Filter by category
- Rule-based question assistant
- Service-specific preparation checklist
- Direct links to official portals
- No paid API key required

## Requirements
- Python 3.9+
- Internet connection to install packages

## Run on Windows
1. Extract this ZIP file.
2. Open PowerShell in the extracted `ai_citizen_services_assistant` folder.
3. Check Python:
   ```powershell
   py --version
   ```
4. Install libraries:
   ```powershell
   py -m pip install -r requirements.txt
   ```
5. Start the app:
   ```powershell
   py -m streamlit run app.py
   ```
6. Open the local URL shown in the terminal, usually `http://localhost:8501`.

Important: Run commands from the folder containing `app.py` and `requirements.txt`. If PowerShell says a file cannot be found, use `dir` to check the current folder.

## How it works
The app searches a small curated service directory using keyword matching and shows relevant portal links. It is a rule-based educational demo, not a government AI system.

## Safety and limitations
- This app is not affiliated with any government department.
- It does not submit applications or access government databases.
- Do not enter personal identifiers, passwords, OTPs, or bank PINs.
- Verify eligibility, fees, deadlines, and document requirements on the official portal.
