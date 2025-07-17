# CPE2CVE Tool

A command-line tool to search for CPEs (Common Platform Enumerations), fetch related CVEs (Common Vulnerabilities and Exposures), and rank available exploits from GitHub.

## Features

- Search CPEs by keyword
- Fetch CVEs for a selected CPE
- Filter CVEs by CVSS score
- Rank exploits by GitHub stars and forks
- Rich terminal output

## Installation

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python cpe2cve.py <keyword> [--min-cvss <score>]
```

- `<keyword>`: The CPE search keyword (e.g., `log4j`)
- `--min-cvss <score>`: (Optional) Minimum CVSS score to filter CVEs (e.g., `--min-cvss 7.0`)

### Example

```bash
python cpe2cve.py log4j --min-cvss 7.0
```

## Configuration

To enable GitHub exploit ranking, set your GitHub token as an environment variable:

**Linux/macOS:**
```bash
export GITHUB_TOKEN=your_token_here
```

**Windows (cmd):**
```cmd
set GITHUB_TOKEN=your_token_here
```

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="your_token_here"
```

> **Note:** The tool will still work without a token, but GitHub API rate limits will be much lower.

## Modules

- `cpe_lookup.py`: Search and select CPEs from the NVD API
- `cve_fetcher.py`: Fetch and filter CVEs for a given CPE
- `exploit_ranker.py`: Rank exploits from GitHub by stars and forks
- `output_renderer.py`: Render results in the terminal using rich tables
- `input_handler.py`: Parse command-line arguments
- `cpe2cve.py`: Main entry point and workflow

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Author

Yair Kohn 