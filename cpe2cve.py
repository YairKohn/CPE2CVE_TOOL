"""
CPE2CVE Tool
Author: Yair Kohn
Main entry point for the CPE2CVE tool. Orchestrates the workflow: search CPEs, fetch CVEs, filter, rank exploits, and render output.
"""
from input_handler import parse_args
from cpe_lookup import search_cpe, choose_cpe
from cve_fetcher import fetch_cves_for_cpe, filter_by_cvss
from exploit_ranker import rank_exploits
from output_renderer import render_output


def main() -> None:
    """
    Main workflow for the CPE2CVE tool.
    Parses arguments, searches CPEs, fetches and filters CVEs, ranks exploits, and renders output.
    """
    args = parse_args()

    # 1. Search CPEs
    cpe_entries = search_cpe(args.keyword)
    if not cpe_entries:
        print(f"No CPEs found for keyword: '{args.keyword}'")
        return
    print(f"Found {len(cpe_entries)} CPEs for keyword '{args.keyword}':")
    chosen = choose_cpe(cpe_entries)

    # 2. Fetch CVEs
    cve_list = fetch_cves_for_cpe(chosen.uri)

    # 3. Optional filtering
    if args.min_cvss is not None:
        cve_list = filter_by_cvss(cve_list, args.min_cvss)

    # 4. Rank exploits for each CVE
    for cve in cve_list:
        if cve.exploit_refs:
            cve.exploit_info = rank_exploits(set(cve.exploit_refs))
            
    # 5. Render
    render_output(chosen.title, cve_list)


if __name__ == "__main__":
    main()
