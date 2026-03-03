"""
utils.py
========
Hilfsfunktionen fuer Dateioperationen und Bildverarbeitung.
"""

import base64
import os


def get_mime_type(image_path: str) -> str:
    """Gibt den MIME-Typ anhand der Dateiendung zurueck."""
    ext = os.path.splitext(image_path)[1].lower()
    return {
        ".jpg":  "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png":  "image/png",
        ".webp": "image/webp",
        ".gif":  "image/gif",
    }.get(ext, "image/jpeg")


def image_to_base64(image_path: str) -> str:
    """Liest ein Bild und gibt es als Base64-String zurueck."""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def read_image_bytes(image_path: str) -> bytes:
    """Liest ein Bild als Bytes."""
    with open(image_path, "rb") as f:
        return f.read()
