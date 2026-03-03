"""
cli.py
======
Kommandozeilen-Interface fuer foto2pptx.
Wird nach der Installation als `foto2pptx` Befehl verfuegbar.
"""

import argparse
import sys

from .constants import DEFAULT_MODELS, SUPPORTED_PROVIDERS
from .pipeline import foto_zu_powerpoint


def parse_args():
    parser = argparse.ArgumentParser(
        description="Foto -> PowerPoint via LLM Vision (Gemini | Anthropic | OpenAI | Llama)",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--provider", choices=SUPPORTED_PROVIDERS,
                        help=f"LLM-Anbieter: {', '.join(SUPPORTED_PROVIDERS)}")
    parser.add_argument("--api-key",   help="API-Key (nicht benoetigt bei Llama/Ollama)")
    parser.add_argument("--model",     help="Modellname (z. B. gemini-2.5-flash, gpt-4o)")
    parser.add_argument("--image",     help="Pfad zum Eingabebild")
    parser.add_argument("--output",    help="Pfad zur Ausgabe-PPTX (Standard: output.pptx)")
    parser.add_argument("--ollama-url", default="http://localhost:11434",
                        help="Ollama-Server-URL (nur fuer Llama)")
    return parser.parse_args()


def prompt_provider() -> str:
    notes = {
        "gemini":    "Google Gemini Vision  (API-Key erforderlich)",
        "anthropic": "Anthropic Claude      (API-Key erforderlich)",
        "openai":    "OpenAI GPT-4o         (API-Key erforderlich)",
        "llama":     "Llama via Ollama      (lokal, kein API-Key noetig)",
    }
    print("\nVerfuegbare LLM-Provider:")
    for i, p in enumerate(SUPPORTED_PROVIDERS, 1):
        print(f"  [{i}] {p:<12} - {notes[p]}  (Standard-Modell: {DEFAULT_MODELS[p]})")

    while True:
        choice = input("\nProvider waehlen (1-4 oder Name): ").strip().lower()
        if choice in [str(i) for i in range(1, len(SUPPORTED_PROVIDERS) + 1)]:
            return SUPPORTED_PROVIDERS[int(choice) - 1]
        if choice in SUPPORTED_PROVIDERS:
            return choice
        print("  Ungueltige Eingabe.")


def main():
    args = parse_args()

    print("=" * 62)
    print("  foto2pptx  –  Foto -> PowerPoint via LLM Vision")
    print("=" * 62)

    provider = args.provider or prompt_provider()

    default_model = DEFAULT_MODELS[provider]
    model_name    = args.model or (
        input(f"Modell [{default_model}]: ").strip() or default_model
    )

    if provider == "llama":
        api_key    = ""
        ollama_url = args.ollama_url
        if ollama_url == "http://localhost:11434":
            ollama_url = input("Ollama-URL [http://localhost:11434]: ").strip() or ollama_url
    else:
        api_key    = args.api_key or input(f"{provider.capitalize()} API-Key: ").strip()
        ollama_url = ""
        if not api_key:
            sys.exit("API-Key darf nicht leer sein.")

    image_path  = args.image  or input("Bildpfad: ").strip().strip('"')
    output_path = args.output or (input("Ausgabedatei [output.pptx]: ").strip() or "output.pptx")

    foto_zu_powerpoint(
        image_path  = image_path,
        output_path = output_path,
        provider    = provider,
        model_name  = model_name,
        api_key     = api_key,
        ollama_url  = ollama_url,
    )


if __name__ == "__main__":
    main()
