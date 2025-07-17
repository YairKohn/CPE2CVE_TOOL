from dataclasses import dataclass
from typing import List
import requests

API_URL = "https://services.nvd.nist.gov/rest/json/cpes/2.0"

@dataclass
class CPEEntry:
    """Data class representing a CPE entry with URI and title."""
    uri: str
    title: str

def search_cpe(keyword: str) -> List[CPEEntry]:
    """
    Search for CPEs matching the given keyword using the NVD API.
    Args:
        keyword (str): The keyword to search for.
    Returns:
        list[CPEEntry]: List of matching CPE entries.
    """
    try:
        params = {"keywordSearch": keyword}
        resp = requests.get(API_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        entries = [] 
        for item in data.get("products", []):
            cpe = item.get("cpe")
            if not cpe:
                continue
            uri = cpe.get("cpeName")
            titles = cpe.get("titles", [])
            title = next((t["title"] for t in titles if t.get("lang") == "en"), uri)
            entries.append(CPEEntry(uri=uri, title=title))
        return entries
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch CPEs: {e}")
        return []
    except Exception as e:
        print(f"[ERROR] Unexpected error during CPE search: {e}")
        return []

def choose_cpe(cpe_list: List[CPEEntry]) -> CPEEntry:
    """
    Prompt the user to select a CPE from a list.
    Args:
        cpe_list (list[CPEEntry]): List of CPE entries to choose from.
    Returns:
        CPEEntry: The selected CPE entry.
    """
    for idx, cpe in enumerate(cpe_list, start=1):
        print(f"{idx}. {cpe.title} ({cpe.uri})")
    while True:
        try:
            choice = int(input("Select a CPE by number: "))
            if 1 <= choice <= len(cpe_list):
                return cpe_list[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(cpe_list)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")