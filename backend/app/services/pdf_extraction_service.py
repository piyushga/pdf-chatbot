from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True, slots=True)
class ExtractedPage:
    page_number: int
    text: str


def clean_text(text: str) -> str:
    text_without_nulls = text.replace("\x00", " ")
    return " ".join(text_without_nulls.split())


def extract_pages(pdf_path: Path) -> list[ExtractedPage]:
    reader = PdfReader(pdf_path)
    extracted_pages: list[ExtractedPage] = []

    for page_number, page in enumerate(reader.pages, start=1):
        cleaned_text = clean_text(page.extract_text() or "")
        if cleaned_text:
            extracted_pages.append(
                ExtractedPage(page_number=page_number, text=cleaned_text)
            )

    return extracted_pages
