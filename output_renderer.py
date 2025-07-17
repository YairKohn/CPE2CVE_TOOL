from typing import Dict, List
from rich.console import Console
from rich.table import Table

console = Console()

def metric_to_emoji(count: int, emoji: str, step: int = 400, max_emojis: int = 5) -> str:
    """
    Convert a numeric metric (e.g., stars, forks) to a string of emojis with normalization.
    Args:
        count (int): The metric count (e.g., stars).
        emoji (str): The emoji to use.
        step (int): The normalization step size.
        max_emojis (int): Maximum number of emojis to display.
    Returns:
        str: A string of emojis representing the metric.
    """
    normalized = min(max_emojis, max(1, count // step))
    return emoji * normalized

def format_description_with_exploits(desc: str, exploit_info: Dict) -> str:
    """
    Format the CVE description to include exploit information if available.
    Args:
        desc (str): The CVE description.
        exploit_info (dict): Mapping of exploit URLs to ExploitInfo objects.
    Returns:
        str: The formatted description with exploit details.
    """
    if not exploit_info:
        return desc

    sorted_exploits = sorted(exploit_info.values(), key=lambda e: (e.stars, e.forks), reverse=True)
    exploits_lines = []
    for ex in sorted_exploits:
        star_emojis = metric_to_emoji(ex.stars, "\u2b50")
        fork_emojis = metric_to_emoji(ex.forks, "\U0001f374")
        line = f"{ex.url} ({star_emojis} - {ex.stars} stars, {fork_emojis} - {ex.forks} forks)"
        exploits_lines.append(line)

    github_section = "GitHub Resources:\n" + "\n".join(exploits_lines) + "\n"
    return f"{desc}\n{github_section}"

def color_cvss(score: float) -> str:
    """
    Colorize the CVSS score for terminal output based on severity.
    Args:
        score (float): The CVSS score.
    Returns:
        str: The colorized score string for rich output.
    """
    if score >= 9:
        return f"[bold red]{score:.1f}[/]"
    elif score >= 7:
        return f"[bold yellow]{score:.1f}[/]"
    else:
        return f"[bold green]{score:.1f}[/]"

def render_output(title: str, cves: List) -> None:
    """
    Render the output table of CVEs and their details to the terminal.
    Args:
        title (str): The title of the CPE.
        cves (list): List of CVE records.
    """
    if not cves:
        console.print("[bold red]No vulnerabilities found.[/]")
        return

    console.print(f"\n[bold underline]Vulnerabilities found for:[/] {title}\n")

    table = Table(show_lines=True, expand=True)
    table.add_column("CVE ID", style="bold cyan", no_wrap=True)
    table.add_column("Severity", justify="center")
    table.add_column("Description", style="white")

    for cve in sorted(cves, key=lambda cve: cve.cvss, reverse=True):
        desc_with_exploits = format_description_with_exploits(cve.desc, cve.exploit_info)
        table.add_row(cve.id, color_cvss(cve.cvss), desc_with_exploits)

    console.print(table)


