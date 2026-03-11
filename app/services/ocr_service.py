from __future__ import annotations

from pathlib import Path
from typing import List, Optional
import os

import cv2
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_path


POPPLER_PATH = os.getenv("POPPLER_PATH")
TESSERACT_CMD = os.getenv("TESSERACT_CMD")

if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
ALLOWED_PDF_EXTENSIONS = {".pdf"}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_PDF_EXTENSIONS


def validate_file_extension(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type. Please upload an image or PDF.")
    return suffix


def load_file(file_path: str, filename: str) -> tuple[Image.Image, Optional[List[Image.Image]]]:
    suffix = validate_file_extension(filename)

    if suffix in ALLOWED_PDF_EXTENSIONS:
        pages = convert_from_path(
            file_path,
            dpi=300,
            poppler_path=POPPLER_PATH
        )
        if not pages:
            raise ValueError("Failed to read PDF pages.")
        return pages[0], pages

    image = Image.open(file_path).convert("RGB")
    return image, None


def preprocess_image(pil_image: Image.Image, steps: list[str]) -> Image.Image:
    img = np.array(pil_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if "Grayscale" in steps:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if "Resize" in steps:
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    if "Denoise" in steps:
        img = cv2.medianBlur(img, 3)

    if "Deskew" in steps:
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )[1]

        coords = np.column_stack(np.where(thresh > 0))

        if len(coords) > 0:
            angle = cv2.minAreaRect(coords)[-1]

            if angle < -45:
                angle = 90 + angle

            angle = -angle

            h, w = img.shape[:2]
            center = (w // 2, h // 2)

            matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

            img = cv2.warpAffine(
                img,
                matrix,
                (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE,
            )

    if "Threshold" in steps:
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img = cv2.adaptiveThreshold(
            img,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )

    return Image.fromarray(img)


def extract_text_from_pages(
    pages: list[Image.Image],
    language: str,
    steps: list[str]
) -> str:
    custom_config = r"--oem 3 --psm 6"
    full_text: list[str] = []

    for page in pages:
        processed = preprocess_image(page, steps)
        text = pytesseract.image_to_string(
            processed,
            lang=language,
            config=custom_config
        ).strip()
        if text:
            full_text.append(text)

    return "\n\n".join(full_text).strip()


def extract_text_from_image(
    image: Image.Image,
    language: str,
    steps: list[str]
) -> str:
    custom_config = r"--oem 3 --psm 6"
    processed = preprocess_image(image, steps)
    return pytesseract.image_to_string(
        processed,
        lang=language,
        config=custom_config
    ).strip()


def run_ocr(
    file_path: str,
    filename: str,
    language: str = "eng",
    steps: Optional[list[str]] = None,
) -> dict:
    steps = steps or ["Grayscale", "Resize"]

    original_image, pdf_pages = load_file(file_path, filename)

    if pdf_pages:
        extracted_text = extract_text_from_pages(pdf_pages, language, steps)
        page_count = len(pdf_pages)
        file_type = "pdf"
    else:
        extracted_text = extract_text_from_image(original_image, language, steps)
        page_count = 1
        file_type = "image"

    return {
        "filename": filename,
        "file_type": file_type,
        "page_count": page_count,
        "language": language,
        "preprocessing_steps": steps,
        "extracted_text": extracted_text,
    }