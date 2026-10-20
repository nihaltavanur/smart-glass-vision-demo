import argparse
from pathlib import Path

import cv2
import pyttsx3
import pytesseract


def read_printed_text(image_path: Path) -> str:
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not open image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    enlarged = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    prepared = cv2.threshold(enlarged, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return pytesseract.image_to_string(prepared, config="--oem 3 --psm 6").strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read text from an image and simulate distance-sensor guidance."
    )
    parser.add_argument("image", type=Path, help="Path to an image containing printed text")
    parser.add_argument(
        "--distance-cm",
        type=float,
        help="Manually supplied distance in centimeters (simulated sensor reading)",
    )
    parser.add_argument(
        "--threshold-cm",
        type=float,
        default=100.0,
        help="Demo threshold for the manually supplied distance (default: 100 cm)",
    )
    parser.add_argument(
        "--speak",
        action="store_true",
        help="Read the OCR result and guidance with the local speech engine",
    )
    args = parser.parse_args()

    if not args.image.is_file():
        raise SystemExit(f"Image file not found: {args.image}")
    if args.distance_cm is not None and args.distance_cm < 0:
        raise SystemExit("Distance must be zero or greater.")
    if args.threshold_cm < 0:
        raise SystemExit("Threshold must be zero or greater.")

    try:
        recognized_text = read_printed_text(args.image)
    except (ValueError, pytesseract.TesseractNotFoundError) as error:
        raise SystemExit(str(error)) from error

    spoken_parts = []
    if recognized_text:
        print(f"Recognized text: {recognized_text}")
        spoken_parts.append(f"Text detected: {recognized_text}")
    else:
        print("Recognized text: no readable text detected")
        spoken_parts.append("No readable text detected.")

    if args.distance_cm is None:
        guidance = "No distance value supplied; sensor guidance is unavailable in this demo."
    elif args.distance_cm <= args.threshold_cm:
        guidance = (
            f"Simulated distance is {args.distance_cm:g} centimeters. "
            "Pause and check your surroundings."
        )
    else:
        guidance = (
            f"Simulated distance is {args.distance_cm:g} centimeters, "
            "above the demo threshold."
        )
    print(f"Guidance: {guidance}")
    spoken_parts.append(guidance)

    if args.speak:
        engine = pyttsx3.init()
        engine.say(" ".join(spoken_parts))
        engine.runAndWait()


if __name__ == "__main__":
    main()
