"""
foto2pptx
=========
Konvertiert Workshop-Fotos automatisch in PowerPoint-Praesentationen
mithilfe von LLM Vision APIs (Gemini, Anthropic, OpenAI, Llama).

Schnellstart
------------
    from foto2pptx import foto_zu_powerpoint

    foto_zu_powerpoint(
        image_path  = "workshop.jpg",
        output_path = "ergebnis.pptx",
        provider    = "anthropic",
        api_key     = "sk-ant-...",
    )

Fortgeschrittene Nutzung
------------------------
    from foto2pptx import analyse_bild, parse_llm_output, create_powerpoint

    raw    = analyse_bild("anthropic", "claude-opus-4-6", "bild.jpg", api_key="...")
    frames = parse_llm_output(raw)
    create_powerpoint(frames, "output.pptx")
"""

__version__ = "1.0.0"
__author__  = "foto2pptx"

# High-Level-API (empfohlen fuer einfache Nutzung)
from .pipeline import foto_zu_powerpoint

# Low-Level-API (fuer erweiterte / individuelle Nutzung)
from .providers import analyse_bild
from .parser import parse_llm_output
from .builder import create_powerpoint
from .converter import color_to_rgb, add_emu_columns, prepare_dataframe
from .constants import (
    SUPPORTED_PROVIDERS,
    DEFAULT_MODELS,
    COLOR_MAP,
    PIXEL_TO_EMU,
)

__all__ = [
    # High-Level
    "foto_zu_powerpoint",
    # Low-Level
    "analyse_bild",
    "parse_llm_output",
    "create_powerpoint",
    # Hilfsfunktionen
    "color_to_rgb",
    "add_emu_columns",
    "prepare_dataframe",
    # Konstanten
    "SUPPORTED_PROVIDERS",
    "DEFAULT_MODELS",
    "COLOR_MAP",
    "PIXEL_TO_EMU",
]
