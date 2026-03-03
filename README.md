# foto2pptx

Konvertiert Workshop-Fotos automatisch in PowerPoint-Praesentationen mithilfe von LLM Vision APIs.

**Unterstuetzte Anbieter:** Google Gemini · Anthropic Claude · OpenAI · Llama (lokal via Ollama)

---

## Installation

```bash
# Basis-Installation
pip install -e .

# Mit einem spezifischen Provider
pip install -e ".[anthropic]"
pip install -e ".[gemini]"
pip install -e ".[openai]"
pip install -e ".[llama]"

# Alle Provider auf einmal
pip install -e ".[all]"
```

---

## Verwendung

### Als Python-Library (empfohlen)

```python
from foto2pptx import foto_zu_powerpoint

# Einfachste Nutzung – ein Aufruf, fertig!
foto_zu_powerpoint(
    image_path  = "workshop.jpg",
    output_path = "ergebnis.pptx",
    provider    = "anthropic",
    api_key     = "sk-ant-...",
)
```

### Fortgeschrittene / modulare Nutzung

```python
from foto2pptx import analyse_bild, parse_llm_output, create_powerpoint

# Schritt 1: Bild analysieren
raw_text = analyse_bild(
    provider   = "openai",
    model_name = "gpt-4o",
    image_path = "bild.jpg",
    api_key    = "sk-...",
)

# Schritt 2: LLM-Ausgabe parsen
dataframes = parse_llm_output(raw_text)

# Schritt 3: PowerPoint erstellen
create_powerpoint(dataframes, "output.pptx")
```

### Kommandozeile

Nach der Installation steht der `foto2pptx` Befehl global zur Verfuegung:

```bash
# Interaktiv (alle Parameter werden abgefragt)
foto2pptx

# Mit Argumenten
foto2pptx \
    --provider  anthropic \
    --api-key   sk-ant-... \
    --model     claude-opus-4-6 \
    --image     workshop.jpg \
    --output    ergebnis.pptx

# Mit Gemini
foto2pptx --provider gemini --api-key AIza... --image foto.png

# Mit lokalem Llama (kein API-Key noetig)
foto2pptx --provider llama --model llama3.2-vision --image foto.jpg
```

---

## Provider & Modelle

| Provider    | Empfohlenes Modell        | API-Key noetig |
|-------------|---------------------------|----------------|
| `anthropic` | `claude-opus-4-6`        | Ja             |
| `gemini`    | `gemini-2.5-flash`        | Ja             |
| `openai`    | `gpt-4o`                  | Ja             |
| `llama`     | `llama3.2-vision`         | Nein (lokal)   |

---

## Projektstruktur

```
foto2pptx/
├── foto2pptx/
│   ├── __init__.py     ← Oeffentliche API
│   ├── constants.py    ← Farben, Prompts, Konfiguration
│   ├── utils.py        ← Datei-Hilfsfunktionen
│   ├── providers.py    ← LLM-Abstraktionsschicht
│   ├── parser.py       ← LLM-Output -> DataFrames
│   ├── converter.py    ← Pixel/EMU, Farben, Formen
│   ├── builder.py      ← PowerPoint-Erstellung
│   ├── pipeline.py     ← High-Level-Pipeline
│   └── cli.py          ← Kommandozeilen-Interface
├── tests/
│   └── test_converter.py
├── setup.py
├── pyproject.toml
└── README.md
```
