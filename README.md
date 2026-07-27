# 🎮 Game Translator AI

A real-time game translation application that captures text directly from a selected game window, extracts it using OCR, and translates it while preserving gameplay context.

> 🚧 This project is currently under active development.

## Overview

Game Translator AI aims to make games more accessible across language barriers without requiring manual screenshots or copy-pasting text.

The application allows the user to select a running game window, captures its content in real time, and extracts visible text using OCR.

The long-term goal is to combine real-time OCR with AI-powered, context-aware translation and display the translated text through an in-game overlay.

## Current Features

- 🪟 Detects open Windows applications
- 🎯 Allows the user to select a specific game/window
- 📷 Captures the selected window in real time
- 👁️ Extracts visible text using EasyOCR
- 🧵 Runs capture processing separately from the main UI
- ▶️ Start/Stop controls
- 🖥️ Simple desktop interface

## How It Works

```text
Game Window
     ↓
Window Selection
     ↓
Real-Time Capture
     ↓
OCR
     ↓
Detected Text
```

The current version implements the capture and OCR pipeline.

Future versions will extend the pipeline to:

```text
Game Window
     ↓
Real-Time Capture
     ↓
OCR
     ↓
Context-Aware AI Translation
     ↓
Translation Overlay
```

## Why AI Translation?

Game dialogue often depends on context.

For example:

```text
Take him out.
```

A literal translation may interpret this as:

```text
Onu dışarı çıkar.
```

But depending on the gameplay context, the intended meaning could be:

```text
Onu etkisiz hale getir.
```

The planned AI translation engine will use recent dialogue and game context to produce translations that better preserve meaning, terminology, and tone.

## Tech Stack

- Python
- OpenCV
- EasyOCR
- PyWin32
- NumPy
- Tkinter
- PyTorch

## Project Structure

```text
game-translator-ai/
│
├── src/
│   ├── main.py
│   ├── window_selector.py
│   ├── capture.py
│   ├── ocr.py
│   ├── translator.py
│   └── overlay.py
│
├── tests/
├── assets/
├── requirements.txt
├── .gitignore
└── README.md
```

## Roadmap

- [x] Window detection and selection
- [x] Real-time window capture
- [x] OCR text extraction
- [x] Basic desktop interface
- [ ] AI-powered translation
- [ ] Translation context memory
- [ ] Translation caching
- [ ] Real-time translation overlay
- [ ] Multiple source and target languages
- [ ] Game-specific terminology support
- [ ] Performance optimization
- [ ] Packaged Windows application

## Status

**Early Development — Prototype**

The core window capture and OCR pipeline is currently functional. Translation and overlay systems are under development.

## Author

**Özge Akçay**

Mathematics student interested in Artificial Intelligence, Machine Learning, Computer Vision, Biometrics, and software development.
