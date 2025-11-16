import sys
import argparse
import csv
from typing import Dict, List, Tuple, Optional

import requests
from bs4 import BeautifulSoup


def parse_args() -> Tuple[str, str]:
    """Parse command-line arguments and validate them."""
    parser = argparse.ArgumentParser(
        description="Download election results for a selected district and save them to CSV."
    )
    parser.add_argument("url", help="URL of the district page listing municipalities (ps32...).")
    parser.add_argument("output", help="Name of the output CSV file.")
    args = parser.parse_args()

    if "ps32" not in args.url:
        print("Error: The first argument must be a URL of the municipality listing page (ps32).")
        sys.exit(1)

    return args.url, args.output


def get_soup(url: str) -> BeautifulSoup:
    """Download a webpage and return a BeautifulSoup object."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Error while downloading URL '{url}': {exc}")
        sys.exit(1)
    return BeautifulSoup(response.text, "html.parser")


def get_base_url(url: str) -> str:
    """Return the base URL for constructing absolute links to subpages."""
    return url.rsplit("/", 1)[0] + "/"


def get_municipalities(soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str, str]]:
    """Extract all municipalities and their detail URLs from the district page."""
    municipalities: List[Tuple[str, str, str]] = []
    for link in soup.find_all("a"):
        code = link.get_text(strip=True)
        href = link.get("href", "")
        if not code.isdigit() or "ps311" not in href:
            continue
        name_cell = link.find_next("td")
        if not name_cell:
            continue
        name = name_cell.get_text(strip=True)
        full_url = base_url + href
        municipalities.append((code, name, full_url))
    return municipalities


def parse_summary(soup: BeautifulSoup) -> Tuple[int, int, int]:
    """
    Return (registered voters, envelopes issued, valid votes) for the selected municipality.

    Values are located in the summary table in cells marked by:
    - headers="sa2" -> Registered voters
    - headers="sa3" -> Envelopes issued
    - headers="sa6" -> Valid votes
    """
    def get_int_by_header(header_value: str) -> int:
        cell = soup.find("td", headers=header_value)
        if cell is None:
            raise ValueError(f"Could not find table cell with headers='{header_value}'.")
        text = (
            cell.get_text(strip=True)
            .replace("\xa0", "")
            .replace(" ", "")
            .replace("\u00a0", "")
        )
        return int(text.replace(",", ""))

    registered = get_int_by_header("sa2")
    envelopes = get_int_by_header("sa3")
    valid = get_int_by_header("sa6")

    return registered, envelopes, valid


def parse_party_votes(soup: BeautifulSoup) -> Dict[str, int]:
    """Parse party names and their vote counts for the selected municipality."""
    votes: Dict[str, int] = {}
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue
        order = cells[0].get_text(strip=True)
        if not order.isdigit():
            continue
        party = cells[1].get_text(strip=True)
        raw_votes = cells[2].get_text(strip=True).replace("\xa0", "").replace(" ", "")
        if not raw_votes.isdigit():
            continue
        votes[party] = int(raw_votes)
    if not votes:
        raise ValueError("No party vote results were found.")
    return votes


def parse_municipality(
    code: str, name: str, url: str, parties_header: Optional[List[str]]
) -> Tuple[Dict[str, int], List[str]]:
    """Parse a single municipality page and return a data row + party header list."""
    soup = get_soup(url)
    registered, envelopes, valid = parse_summary(soup)
    party_votes = parse_party_votes(soup)

    # First municipality determines the order of political parties
    if parties_header is None:
        parties_header = list(party_votes.keys())

    row: Dict[str, int] = {
        "code": int(code),
        "location": name,
        "registered": registered,
        "envelopes": envelopes,
        "valid": valid,
    }

    for party in parties_header:
        row[party] = party_votes.get(party, 0)

    return row, parties_header


def write_csv(filename: str, header: List[str], rows: List[Dict[str, int]]) -> None:
    """Write collected data rows into a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
    except OSError as exc:
        print(f"Error while writing file '{filename}': {exc}")
        sys.exit(1)


def main() -> None:
    """Main program entry point."""
    url, output_file = parse_args()
    print(f"Downloading data from: {url}")
    district_soup = get_soup(url)
    base_url = get_base_url(url)
    municipalities = get_municipalities(district_soup, base_url)

    if not municipalities:
        print("No municipalities were found on this page. Check the URL.")
        sys.exit(1)

    rows: List[Dict[str, int]] = []
    parties_header: Optional[List[str]] = None

    for index, (code, name, muni_url) in enumerate(municipalities, start=1):
        print(f"({index}/{len(municipalities)}) Processing municipality: {name} ({code})")
        row, parties_header = parse_municipality(code, name, muni_url, parties_header)
        rows.append(row)

    header = ["code", "location", "registered", "envelopes", "valid"]
    if parties_header:
        header.extend(parties_header)

    write_csv(output_file, header, rows)
    print(f"Done. Results saved to file: {output_file}")


if __name__ == "__main__":
    main()
