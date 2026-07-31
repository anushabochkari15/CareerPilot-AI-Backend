"""
CareerPilot AI — PDF Extraction Service

Extracts text from uploaded PDF resume files using PyPDF2.
"""

import io
import logging
from typing import Optional

from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_bytes: bytes) -> Optional[str]:
    """
    Extract text content from a PDF file.

    Args:
        file_bytes: Raw PDF file bytes

    Returns:
        Extracted text or None if extraction fails
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text_parts = []

        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                text_parts.append(text)

        full_text = "\n".join(text_parts).strip()

        if not full_text:
            logger.warning("PDF text extraction returned empty result — file may be scanned/image-based")
            return None

        logger.info(f"Extracted {len(full_text)} characters from PDF")
        return full_text

    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        return None
