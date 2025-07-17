from dataclasses import dataclass, field
from typing import List, Dict
import requests

API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

@dataclass
class CVERecord:
    """Data class representing a CVE record with id, cvss score, description, and exploit info."""
    id: str
    cvss: float
    desc: str
    exploit_refs: List[str] = field(default_factory=list)
    exploit_info: Dict = field(default_factory=dict)

def fetch_cves_for_cpe(cpe_uri: str) -> List[CVERecord]:
    """
    Fetch CVEs for a given CPE URI from the NVD API.
    Args:
        cpe_uri (str): The CPE URI to fetch CVEs for.
    Returns:
        list[CVERecord]: List of CVE records.
    """
    try:
        params = {"cpeName": cpe_uri, "resultsPerPage": 100}
        resp = requests.get(API_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        cves = []
        for item in data.get("vulnerabilities", []):
            cve_id = item["cve"]["id"]
            desc_data = item["cve"]["descriptions"]
            desc = next((d["value"] for d in desc_data if d["lang"] == "en"), "")
            metrics = item["cve"].get("metrics", {})
            cvss_data = metrics.get("cvssMetricV31") or metrics.get("cvssMetricV30")
            if not cvss_data:
                continue
            score = cvss_data[0]["cvssData"]["baseScore"]
            references = item["cve"].get("references", [])
            exploit_urls = [r["url"] for r in references if "Exploit" in r.get("tags", []) and "github.com" in r["url"]]
            cves.append(CVERecord(id=cve_id, cvss=score, desc=desc, exploit_refs=exploit_urls))
        return cves
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch CVEs: {e}")
        return []
    except Exception as e:
        print(f"[ERROR] Unexpected error during CVE fetch: {e}")
        return []

def filter_by_cvss(cves: List[CVERecord], min_score: float) -> List[CVERecord]:
    """
    Filter a list of CVE records by minimum CVSS score.
    Args:
        cves (list[CVERecord]): List of CVE records.
        min_score (float): Minimum CVSS score.
    Returns:
        list[CVERecord]: Filtered list of CVE records.
    """
    return [cve for cve in cves if cve.cvss >= min_score]