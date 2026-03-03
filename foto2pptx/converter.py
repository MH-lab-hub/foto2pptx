"""
converter.py
============
Konvertierungsfunktionen fuer Koordinaten, Farben und Form-Typen.
"""

import pandas as pd

from .constants import COLOR_MAP, PIXEL_TO_EMU


def convert_to_emu(series: pd.Series) -> pd.Series:
    """Konvertiert Pixel-Werte in EMU (English Metric Units fuer PowerPoint)."""
    numeric = pd.to_numeric(series, errors="coerce").fillna(0)
    return (numeric * PIXEL_TO_EMU).round().astype("Int64")


def add_emu_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Fuegt EMU-Spalten fuer x, y, Breite und Hoehe hinzu."""
    df      = df.copy()
    col_map = {c.lower(): c for c in df.columns}
    for field in ["x", "y", "breite", "hoehe"]:
        if field in col_map:
            df[f"{field}_emu"] = convert_to_emu(df[col_map[field]])
    return df


def color_to_rgb(color_name) -> tuple[int, int, int]:
    """
    Wandelt einen Farbnamen oder Hex-Wert in ein RGB-Tupel um.

    Unterstuetzt:
    - Deutsche Farbnamen (z. B. "blau", "dunkelrot")
    - Hex-Werte (z. B. "#FF0000" oder "FF0000")
    - Fallback: Grau (128, 128, 128)
    """
    if pd.isna(color_name) or color_name == "":
        return (128, 128, 128)

    name = str(color_name).lower().strip()
    name_clean = name.lstrip("#")

    # Hex-Wert direkt verarbeiten
    if len(name_clean) == 6 and all(c in "0123456789abcdef" for c in name_clean):
        r = int(name_clean[0:2], 16)
        g = int(name_clean[2:4], 16)
        b = int(name_clean[4:6], 16)
        return (r, g, b)

    # Umlaute normalisieren
    normalized = (name
                  .replace("\u00e4", "ae").replace("\u00f6", "oe")
                  .replace("\u00fc", "ue").replace("\u00df", "ss"))

    return COLOR_MAP.get(normalized, COLOR_MAP.get(name, (128, 128, 128)))


def normalize_shape_type(shape_type) -> str:
    """Normalisiert den Form-Typ auf 'Kreis' oder 'Rechteck'."""
    if pd.isna(shape_type):
        return "Rechteck"
    s = str(shape_type).lower().strip()
    if any(k in s for k in ["kreis", "circle", "oval", "rund"]):
        return "Kreis"
    return "Rechteck"


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bereitet einen DataFrame vor:
    - Konvertiert Farbnamen zu RGB-Tupeln
    - Normalisiert Form-Typen
    """
    df = df.copy()
    if "Farbe_Form" in df.columns:
        df["rgb_form"] = df["Farbe_Form"].apply(color_to_rgb)
    if "Farbe_Text" in df.columns:
        df["rgb_text"] = df["Farbe_Text"].apply(color_to_rgb)
    if "Form_Typ" in df.columns:
        df["Form_Typ"]  = df["Form_Typ"].apply(normalize_shape_type)
    return df
