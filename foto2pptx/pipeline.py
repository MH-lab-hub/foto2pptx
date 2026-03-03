"""
pipeline.py
===========
Die Haupt-Pipeline: Bild -> LLM-Analyse -> Parsing -> PowerPoint.
Kann als einfache High-Level-API verwendet werden.
"""

import os

from .builder import create_powerpoint
from .constants import DEFAULT_MODELS, SUPPORTED_PROVIDERS
from .parser import parse_llm_output
from .providers import analyse_bild


def foto_zu_powerpoint(
    image_path:  str,
    output_path: str  = "output.pptx",
    provider:    str  = "anthropic",
    model_name:  str  = None,
    api_key:     str  = "",
    ollama_url:  str  = "http://localhost:11434",
) -> str:
    """
    Konvertiert ein Foto direkt in eine PowerPoint-Datei.

    Parameters
    ----------
    image_path  : str  – Pfad zum Eingabebild (jpg, png, webp, gif)
    output_path : str  – Zieldatei (Standard: "output.pptx")
    provider    : str  – LLM-Provider: "gemini", "anthropic", "openai", "llama"
    model_name  : str  – Modellname; wird auto-gewaehlt wenn None
    api_key     : str  – API-Key (nicht noetig bei Llama)
    ollama_url  : str  – Ollama-URL (nur fuer Llama)

    Returns
    -------
    str – Pfad zur erstellten PowerPoint-Datei

    Beispiel
    --------
    >>> from foto2pptx import foto_zu_powerpoint
    >>> foto_zu_powerpoint(
    ...     image_path  = "workshop.jpg",
    ...     output_path = "ergebnis.pptx",
    ...     provider    = "anthropic",
    ...     api_key     = "sk-ant-...",
    ... )
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Bild nicht gefunden: {image_path}")

    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unbekannter Provider '{provider}'. "
            f"Waehle: {', '.join(SUPPORTED_PROVIDERS)}"
        )

    model = model_name or DEFAULT_MODELS[provider]

    # Schritt 1: LLM-Analyse
    raw_output = analyse_bild(
        provider   = provider,
        model_name = model,
        image_path = image_path,
        api_key    = api_key,
        ollama_url = ollama_url,
    )

    # Schritt 2: Parsen
    print("\nParse LLM-Ausgabe ...")
    dataframes = parse_llm_output(raw_output)

    if not dataframes:
        raise RuntimeError(
            "Keine Elemente erkannt. Bitte Bild oder Modell pruefen."
        )

    # Schritt 3: PowerPoint erstellen
    print("\nErstelle PowerPoint ...")
    return create_powerpoint(dataframes, output_path)
