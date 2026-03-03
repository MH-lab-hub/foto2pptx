from setuptools import setup, find_packages

setup(
    name="foto2pptx",
    version="1.0.0",
    description="Konvertiert Workshop-Fotos automatisch in PowerPoint via LLM Vision",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Dein Name",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "python-pptx",
        "Pillow",
    ],
    extras_require={
        "gemini":    ["google-generativeai"],
        "anthropic": ["anthropic"],
        "openai":    ["openai"],
        "llama":     ["ollama"],
        "all":       ["google-generativeai", "anthropic", "openai", "ollama"],
    },
    entry_points={
        "console_scripts": [
            "foto2pptx=foto2pptx.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
