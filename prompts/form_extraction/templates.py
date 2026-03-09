"""Prompt templates for LLM-based form text extraction."""

from __future__ import annotations

EXTRACTION_PROMPT_TEMPLATE = """You are an AI assistant tasked with extracting structured data from a form document.

Document:
{document}

Schema:
{schema}

Return a JSON object containing the extracted field values. If a field is missing, use null.
"""

FEW_SHOT_TEMPLATE = """Example
-------
Document:
{document}

Expected Output:
{output}
"""
