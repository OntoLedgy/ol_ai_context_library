"""Prompt templates for LLM-based document text extraction."""

from __future__ import annotations

#TODO: move to ol_ai_services\prompts\text_extraction
DOCUMENT_EXTRACTION_PROMPT = """You are an AI assistant tasked with extracting structured content from a technical document.

Document:
{document}

Extraction Schema:
{schema}

Return the extracted document structure as a JSON object matching the schema."""

TABLE_EXTRACTION_PROMPT = """You are an AI assistant tasked with extracting table data from a technical document.

Table:
{table}

Extraction Schema:
{schema}

Return the table data as a JSON array preserving headers, rows, and columns."""

EQUATION_EXTRACTION_PROMPT = """You are an AI assistant tasked with extracting mathematical equations from a technical document.

Equation Context:
{equation}

Extraction Schema:
{schema}

Return each equation in LaTeX format with its associated label and surrounding context as JSON."""
