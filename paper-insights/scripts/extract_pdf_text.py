#!/usr/bin/env python3
"""
Extract text from a PDF with optional per-page JSON output.

Tries, in order:
1) pypdf
2) pdfplumber
3) pdftotext (CLI)

Examples:
  python3 extract_pdf_text.py /path/to/paper.pdf
  python3 extract_pdf_text.py /path/to/paper.pdf --json /path/to/paper.json
  python3 extract_pdf_text.py /path/to/paper.pdf --page-separators
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def _extract_with_pypdf(pdf_path: Path) -> List[str]:
    try:
        import pypdf  # type: ignore
    except Exception:
        raise ImportError("pypdf not available")

    reader = pypdf.PdfReader(str(pdf_path))
    pages: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text.strip())
    return pages


def _extract_with_pdfplumber(pdf_path: Path) -> List[str]:
    try:
        import pdfplumber  # type: ignore
    except Exception:
        raise ImportError("pdfplumber not available")

    pages: List[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text.strip())
    return pages


def _extract_with_pdftotext(pdf_path: Path) -> List[str]:
    if shutil.which("pdftotext") is None:
        raise FileNotFoundError("pdftotext not found")

    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "pdftotext failed")

    raw = result.stdout
    pages = [page.strip() for page in raw.split("\f")]
    return pages


def extract_pages(pdf_path: Path) -> Tuple[str, List[str]]:
    errors = []
    for method_name, method in (
        ("pypdf", _extract_with_pypdf),
        ("pdfplumber", _extract_with_pdfplumber),
        ("pdftotext", _extract_with_pdftotext),
    ):
        try:
            pages = method(pdf_path)
            if pages:
                return method_name, pages
            errors.append(f"{method_name}: empty output")
        except Exception as exc:  # pragma: no cover - best-effort extraction
            errors.append(f"{method_name}: {exc}")

    error_text = "\n".join(errors)
    raise RuntimeError(
        "All extraction methods failed.\n" + error_text + "\n"
        "Install pypdf or pdfplumber, or provide a text export."
    )


def write_text(output_path: Path, pages: List[str], page_separators: bool) -> None:
    chunks = []
    for index, page in enumerate(pages, start=1):
        if page_separators:
            chunks.append(f"[Page {index}]")
        chunks.append(page)
    text = "\n\n".join(chunks).strip() + "\n"
    output_path.write_text(text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text from a PDF")
    parser.add_argument("pdf", help="Path to PDF")
    parser.add_argument(
        "--output",
        help="Output text file path (default: <pdf>.txt)",
    )
    parser.add_argument(
        "--json",
        dest="json_path",
        help="Optional JSON output path with per-page text",
    )
    parser.add_argument(
        "--page-separators",
        action="store_true",
        help="Insert [Page N] separators in the text output",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf).expanduser().resolve()
    if not pdf_path.exists():
        print(f"[ERROR] PDF not found: {pdf_path}")
        return 1

    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else pdf_path.with_suffix(".txt")
    )

    json_path = None
    if args.json_path:
        json_path = Path(args.json_path).expanduser().resolve()

    try:
        method, pages = extract_pages(pdf_path)
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_text(output_path, pages, args.page_separators)

    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "source": str(pdf_path),
            "method": method,
            "page_count": len(pages),
            "pages": pages,
        }
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    print(f"[OK] Extracted with {method}")
    print(f"[OK] Text output: {output_path}")
    if json_path:
        print(f"[OK] JSON output: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
