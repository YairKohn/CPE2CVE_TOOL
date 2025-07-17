import argparse
from argparse import Namespace

def parse_args() -> Namespace:
    """
    Parse command-line arguments for the CPE2CVE tool.
    Returns:
        argparse.Namespace: Parsed arguments with 'keyword' and optional 'min_cvss'.
    """
    parser = argparse.ArgumentParser(description="Fetch CVEs for a given CPE keyword.")
    parser.add_argument("keyword", type=str, help="CPE search keyword, e.g. 'log4j'")
    parser.add_argument("--min-cvss", type=float, help="Minimum CVSS score to filter CVEs (default: 0.0)") 
    return parser.parse_args()


