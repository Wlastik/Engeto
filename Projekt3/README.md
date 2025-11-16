✅ FINAL README.md (krátká verze podle zadání)
# Elections Scraper

This project downloads the results of the 2017 Czech parliamentary elections for a selected district from the website **volby.cz** and saves them into a CSV file. The script processes all municipalities in the selected district and extracts voter statistics and vote counts for all political parties.


## Installation

It is recommended to use a virtual environment.

### 1. Create and activate virtual environment

**Windows (PowerShell)**:


python -m venv venv
.\venv\Scripts\activate


**Linux/macOS**:


python3 -m venv venv
source venv/bin/activate


### 2. Install required libraries


pip install -r requirements.txt



## Running the Project

The script requires **two arguments**:

1. URL of the district page (must contain `ps32`)
2. Name of the output CSV file

Syntax:


python main.py <DISTRICT_URL_PS32> <OUTPUT_CSV>



## Example Usage (District: Vsetín)

District URL:


https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7203


Run the scraper:


python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7203
" "vysledky_vsetin.csv"



## Program Output (Progress)

During execution, the script prints progress for each processed municipality:



Stahuji data z URL: https://www.volby.cz/
...
(1/61) Processing municipality: Branky (541648)
(2/61) Processing municipality: Bystřička (544592)
(3/61) Processing municipality: Halenkov (544773)
...


After completion:


Done. Results saved to file: vysledky_vsetin.csv



## Partial CSV Output Example

The resulting CSV file contains one row per municipality:



code,location,registered,envelopes,valid,Občanská demokratická strana,Česká pirátská strana,...
541648,Branky,771,455,453,58,23,...
544592,Bystřička,812,496,488,67,29,...
544773,Halenkov,1055,673,664,92,44,...


The file includes:

- municipality code (`code`)
- municipality name (`location`)
- registered voters
- envelopes issued
- valid votes
- vote counts for each political party


## Summary

- The script fulfills the project requirements: scraping, argument validation, CSV output.
- It is separated into clear functions and under the 200-line limit.
- CSV is encoded in `utf-8-sig` for proper display of Czech characters in Excel.


Pokud chceš, můžu ti udělat ještě kratší verzi, nebo delší detailní verzi, nebo česky. Stačí říct.