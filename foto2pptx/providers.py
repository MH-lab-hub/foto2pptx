"""
providers.py
============
LLM-Provider-Abstraktionsschicht.
Unterstuetzt: Google Gemini, Anthropic Claude, OpenAI, Llama (Ollama).
"""

import sys

from .constants import ANALYSE_PROMPT, SUPPORTED_PROVIDERS
from .utils import get_mime_type, image_to_base64, read_image_bytes


def analyse_mit_gemini(api_key: str, model_name: str, image_path: str) -> str:
    """Sendet das Bild an die Google Gemini Vision API."""
    try:
        import google.generativeai as genai
    except ImportError:
        sys.exit("Installiere: pip install google-generativeai")

    genai.configure(api_key=api_key)
    image_bytes = read_image_bytes(image_path)
    mime_type   = get_mime_type(image_path)

    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config={"temperature": 0.0, "top_p": 1.0, "top_k": 1},
    )
    response = model.generate_content([
        ANALYSE_PROMPT,
        {"mime_type": mime_type, "data": image_bytes},
    ])
    return response.text


def analyse_mit_anthropic(api_key: str, model_name: str, image_path: str) -> str:
    """Sendet das Bild an die Anthropic Claude Vision API."""
    try:
        import anthropic
    except ImportError:
        sys.exit("Installiere: pip install anthropic")

    client    = anthropic.Anthropic(api_key=api_key)
    b64_image = image_to_base64(image_path)
    mime_type = get_mime_type(image_path)

    message = client.messages.create(
        model=model_name,
        max_tokens=8192,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type":       "base64",
                        "media_type": mime_type,
                        "data":       b64_image,
                    },
                },
                {"type": "text", "text": ANALYSE_PROMPT},
            ],
        }],
    )
    return message.content[0].text


def analyse_mit_openai(api_key: str, model_name: str, image_path: str) -> str:
    """Sendet das Bild an die OpenAI GPT-4 Vision API."""
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("Installiere: pip install openai")

    client    = OpenAI(api_key=api_key)
    b64_image = image_to_base64(image_path)
    mime_type = get_mime_type(image_path)

    response = client.chat.completions.create(
        model=model_name,
        max_tokens=8192,
        temperature=0.0,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url":    f"data:{mime_type};base64,{b64_image}",
                        "detail": "high",
                    },
                },
                {"type": "text", "text": ANALYSE_PROMPT},
            ],
        }],
    )
    return response.choices[0].message.content


def analyse_mit_llama(
    model_name: str,
    image_path: str,
    ollama_url: str = "http://localhost:11434",
) -> str:
    """Sendet das Bild an ein lokales Llama-Modell via Ollama."""
    try:
        import ollama
    except ImportError:
        sys.exit("Installiere: pip install ollama  (und starte Ollama lokal)")

    client = ollama.Client(host=ollama_url)
    response = client.chat(
        model=model_name,
        messages=[{
            "role":    "user",
            "content": ANALYSE_PROMPT,
            "images":  [image_path],
        }],
        options={"temperature": 0.0},
    )
    return response["message"]["content"]


def analyse_bild(
    provider:   str,
    model_name: str,
    image_path: str,
    api_key:    str = "",
    ollama_url: str = "http://localhost:11434",
) -> str:
    """
    Einheitlicher Einstiegspunkt – waehlt automatisch den richtigen LLM-Provider.

    Parameters
    ----------
    provider   : str  – "gemini", "anthropic", "openai" oder "llama"
    model_name : str  – Modellname (z. B. "gemini-2.5-flash", "gpt-4o")
    image_path : str  – Pfad zur Bilddatei
    api_key    : str  – API-Key (nicht noetig bei Llama)
    ollama_url : str  – Ollama-Server-URL (nur fuer Llama)

    Returns
    -------
    str – Rohe LLM-Ausgabe mit den Markdown-Tabellen
    """
    print(f"\n[{provider.upper()}] Analysiere Bild mit Modell '{model_name}' ...")

    if provider == "gemini":
        result = analyse_mit_gemini(api_key, model_name, image_path)
    elif provider == "anthropic":
        result = analyse_mit_anthropic(api_key, model_name, image_path)
    elif provider == "openai":
        result = analyse_mit_openai(api_key, model_name, image_path)
    elif provider == "llama":
        result = analyse_mit_llama(model_name, image_path, ollama_url)
    else:
        raise ValueError(
            f"Unbekannter Provider '{provider}'. "
            f"Waehle: {', '.join(SUPPORTED_PROVIDERS)}"
        )

    print("Analyse abgeschlossen.")
    return result
