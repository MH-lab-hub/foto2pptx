"""
constants.py
============
Globale Konstanten und Konfigurationen fuer foto2pptx.
"""

PIXEL_TO_EMU = 9525  # 1 Pixel = 9525 EMU (PowerPoint-Standard)

SUPPORTED_PROVIDERS = ["gemini", "anthropic", "openai", "llama"]

DEFAULT_MODELS = {
    "gemini":    "gemini-2.5-flash",
    "anthropic": "claude-opus-4-6",
    "openai":    "gpt-4o",
    "llama":     "llama3.2-vision",
}

COLOR_MAP = {
    "schwarz": (0, 0, 0),        "weiss": (255, 255, 255),
    "grau": (128, 128, 128),     "dunkelgrau": (64, 64, 64),
    "hellgrau": (192, 192, 192),
    "rot": (255, 0, 0),          "dunkelrot": (139, 0, 0),
    "hellrot": (255, 127, 127),  "lightrot": (255, 127, 127),
    "gruen": (0, 128, 0),        "hellgruen": (144, 238, 144),
    "dunkelgruen": (0, 100, 0),  "lime": (0, 255, 0),
    "blau": (0, 0, 255),         "dunkelblau": (0, 0, 139),
    "hellblau": (173, 216, 230), "lightblue": (173, 216, 230),
    "cyan": (0, 255, 255),       "tuerkis": (64, 224, 208),
    "teal": (0, 128, 128),
    "gelb": (255, 255, 0),       "gold": (255, 215, 0),
    "khaki": (240, 230, 200),
    "orange": (255, 165, 0),     "dunkelorange": (255, 140, 0),
    "lightorange": (255, 200, 124),
    "rosa": (255, 192, 203),     "magenta": (255, 0, 255),
    "violett": (238, 130, 238),  "lila": (200, 162, 200),
    "purple": (128, 0, 128),
    "braun": (165, 42, 42),      "schokolade": (210, 105, 30),
    "sienna": (160, 82, 45),
    "beige": (245, 245, 220),    "creme": (255, 253, 208),
    "marineblau": (0, 0, 128),   "olivgruen": (128, 128, 0),
    "unklar": (128, 128, 128),
}

ANALYSE_PROMPT = """
Analysiere das Bild vollstaendig als Workshopdokumentation und gib die Ergebnisse ausschliesslich in tabellarischer, strukturierter Form zurueck.
Keine Erklaerungen, keine Interpretation ausserhalb der Tabellen, kein zusaetzlicher Text.

Die Ausgabe besteht aus genau fuenf Teilen (A-E), in der angegebenen Reihenfolge.
Jeder Teil beginnt exakt mit der jeweiligen Ueberschrift.

--------------------------------------------------
TEIL A Bilddaten
--------------------------------------------------
Erstelle eine sachliche Einschaetzung zu:
- Seitenverhaeltnis
- Gesamtgroesse in Pixeln (geschaetzt)

Ausgabeformat:

| Parameter | Wert |
|----------|-------|
| Seitenverhaeltnis | ... |
| Breite (px) | ... |
| Hoehe (px) | ... |

--------------------------------------------------
TEIL B Reiner Text
--------------------------------------------------
Alle sichtbaren Elemente, die NUR aus Text bestehen (ohne umgebende Form).

| Element_ID | Farbe_Text | x | y | Breite | Hoehe | Textinhalt |
|------------|------------|---|---|--------|-------|------------|

Regeln:
- Jede Element_ID: E1, E2, E3, ...
- Farben: einfache Farbnamen oder Hexwerte; sonst "unklar".
- Koordinaten: Ursprung (0,0) oben links, realistische numerische Schaetzung.

--------------------------------------------------
TEIL C Text_in_Form
--------------------------------------------------
Alle Elemente, bei denen Text vollstaendig in einer Form enthalten ist.

| Element_ID | Form_Typ | Farbe_Form | Farbe_Text | x | y | Breite | Hoehe | Textinhalt |
|------------|----------|------------|------------|---|---|--------|-------|------------|

Erlaubte Werte Form_Typ:
- Rechteck, Kreis, Andere

Regeln:
- Text + Form = EIN Element.
- Koordinaten und Farben wie oben.

--------------------------------------------------
TEIL D Formen (ohne Text)
--------------------------------------------------
Alle Formen, die keinen Text enthalten (z. B. Rechtecke, Kreise, Icons, Symbole).

| Element_ID | Form_Typ | Farbe_Form | x | y | Breite | Hoehe |
|------------|----------|------------|---|---|--------|-------|

--------------------------------------------------
TEIL E Pfeile & Verbindungen
--------------------------------------------------
Analysiere alle Pfeile oder verbindenden Linien zwischen Elementen.

| Pfeil_ID | Von_Element_ID | Zu_Element_ID | Pfeil_Typ |
|----------|----------------|---------------|-----------|

Erlaubte Pfeil_Typ:
- gerichtet, ungerichtet, unklar

--------------------------------------------------
GESAMTREGELN
--------------------------------------------------
- Ausschliesslich Tabellen ausgeben.
- Keine Einleitung, kein Fazit.
- Kein zusaetzlicher Text.
- Keine Emojis.
- Keine Annahmen ueber Inhalte oder Zielsetzungen.
"""
