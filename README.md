# Smart Glass Vision Assistance Demo

> A new portfolio demo inspired by the Smart Glass project description in my resume. This is an independent, hardware-free demonstration; it is not the original Arduino/Raspberry Pi prototype.

This command-line program extracts printed text from an image with OpenCV and Tesseract OCR. It can also read a distance value entered by the user to simulate an ultrasonic sensor. Optional text-to-speech reads the guidance aloud.

## Requirements

- Python 3.10 or newer
- Tesseract OCR installed separately and available on your system path

## Setup

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python smart_glass_demo.py path/to/photo.jpg --distance-cm 80
python smart_glass_demo.py path/to/photo.jpg --distance-cm 35 --speak
```

Replace `path/to/photo.jpg` with a path to your own local image containing printed text; the repository does not include a sample image.

The distance is typed in manually. No live sensor, camera, wearable device, navigation system, or obstacle detection is connected. `--speak` uses the operating system's available speech engine and may need local audio support.

## Limitations and responsible use

- OCR can misread text, especially in poor lighting, unusual fonts, or low-resolution images.
- The distance value is simulated and may be incorrect; this demo is not a safety device and must not be used to navigate or avoid obstacles.
- The program only reports OCR text and the manually entered distance. It does not interpret scenes or provide reliable environmental awareness.
- Use only images you have permission to process, and avoid storing personal or identifying images in a public repository.

## Project structure

```text
smart_glass_demo.py   OCR and simulated distance guidance
requirements.txt      Python package dependencies
```
