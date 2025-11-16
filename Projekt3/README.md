# Elections Scraper

This project downloads the results of the 2017 Czech parliamentary elections for a single district  
(from [volby.cz](https://www.volby.cz)) and saves them into a CSV file.

The script:

- takes a **district URL** (page listing municipalities, `ps32`) as the first argument,
- takes an **output CSV filename** as the second argument,
- downloads and parses the results for **all municipalities in that district**,
- outputs one row per municipality, including:
  - municipality code,
  - municipality name (as `location`),
  - number of registered voters,
  - number of envelopes issued,
  - number of valid votes,
  - one column per political party (vote counts).


## Project structure

The repository contains:

- `main.py` – main and only Python script (program entry point),
- `requirements.txt` – list of third-party dependencies and their versions,
- `vysledky_vsetin.csv` (example) – sample output file with scraped results,
- `README.md` – this documentation file.


## Virtual environment and installation

It is recommended to run the project inside a Python virtual environment.

### 1. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\activate
