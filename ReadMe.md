# Web Summarizer Project

This project reads a given website, and returns a short summary of its contents. 

Files of interest:
- `main.py` — main script (prompts for URL, fetches page, extracts paragraphs, summarizes).
- `requirements.txt` — Python dependencies.
- `setup.ps1` — simple PowerShell setup script.

## Features
- Fetches page HTML with a safe `User-Agent` header.
- Parses paragraph text from the page (`parse_wiki_content`).
- Summarizes long pages by chunking text and using a transformer summarizer (`facebook/bart-large-cnn` by default).
- Lazy chunking (generator) so long pages don't use excessive memory.

## Prerequisites
- Python 3.8+ installed and on your PATH.
- Windows PowerShell (examples below assume PowerShell).

## Quick setup (PowerShell)
Open PowerShell in the project folder (where `main.py`, `requirements.txt`, and `setup.ps1` live) and run:

```powershell
# allow activation scripts for the current user (first time only)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# run the setup script:
.\setup.ps1

# activate the venv (in the same shell)
.\venv\Scripts\Activate


