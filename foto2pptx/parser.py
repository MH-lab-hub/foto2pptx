"""
parser.py
=========
Parst die rohe LLM-Ausgabe (Markdown-Tabellen) in pandas DataFrames.
"""

import re

import pandas as pd


def extract_section(text: str, section_title: str) -> str | None:
    """Extrahiert einen Abschnitt aus dem LLM-Output anhand seines Titels."""
    pattern = rf"{re.escape(section_title)}(.+?)(?=TEIL [A-E]|$)"
    match   = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None


def parse_markdown_table(table_text: str) -> pd.DataFrame:
    """Wandelt eine Markdown-Tabelle in einen pandas DataFrame um."""
    lines   = [l.strip() for l in table_text.splitlines() if l.strip()]
    headers = [h.strip() for h in lines[0].strip("|").split("|")]
    rows    = []
    for line in lines[2:]:
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(headers):
            cells = cells[:len(headers)] + [""] * (len(headers) - len(cells))
        rows.append(cells)
    return pd.DataFrame(rows, columns=headers)


def extract_all_tables(section_text: str) -> list[str]:
    """Findet alle Markdown-Tabellen in einem Textabschnitt."""
    return re.findall(r"(\|.+?\|(?:\n\|.*\|)+)", section_text, re.DOTALL)


def parse_llm_output(output_text: str) -> dict[str, pd.DataFrame]:
    """
    Parst die gesamte LLM-Ausgabe und gibt ein Dict mit DataFrames zurueck.

    Returns
    -------
    dict mit den Schluesseln: "TEIL A", "TEIL B", "TEIL C", "TEIL D", "TEIL E"
    (nur Teile mit Daten sind enthalten)
    """
    sections = {
        "TEIL A": "TEIL A Bilddaten",
        "TEIL B": "TEIL B Reiner Text",
        "TEIL C": "TEIL C Text_in_Form",
        "TEIL D": "TEIL D Formen (ohne Text)",
        "TEIL E": "TEIL E Pfeile & Verbindungen",
    }

    dataframes: dict[str, pd.DataFrame] = {}

    for key, title in sections.items():
        section_text = extract_section(output_text, title)
        if not section_text:
            print(f"  [!] {key}: Abschnitt nicht gefunden")
            continue
        tables = extract_all_tables(section_text)
        if tables:
            df = parse_markdown_table(tables[0])
            if len(df) > 0:
                dataframes[key] = df
                print(f"  [OK] {key}: {len(df)} Zeilen geparst")
            else:
                print(f"  [!] {key}: Tabelle leer (nur Header)")
        else:
            print(f"  [!] {key}: Keine Tabelle gefunden")

    return dataframes
