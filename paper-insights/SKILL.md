---
name: paper-insights
description: "Analyze, summarize, and critique long AI/ML research papers (PDFs, arXiv, conference papers) with structured outputs, key contributions, method/experiment breakdowns, limitations, and reproduction notes. Use when the user provides a paper PDF or asks for TL;DR, deep analysis, review-style critique, or replication guidance for AI papers."
---

# Paper Insights

## Overview

Provide high-quality understanding of long AI papers: structured summaries, critical analysis, and reproduction guidance. Prefer concise but rigorous reasoning. Default output is Chinese structured summary + critical analysis + reproduction notes unless the user requests another format or language.

## Workflow Decision Tree

1. Identify input type:
- If the user provides a PDF path, extract text with `scripts/extract_pdf_text.py`.
- If the user provides pasted text or a section, skip extraction.
2. Choose output mode (use user preference when provided):
- Quick TL;DR
- Deep analysis (default)
- Review-style critique
- Reproduction notes
3. Produce the output using the templates in `references/output_templates.md`.

## Step 1: Acquire Text

Use `scripts/extract_pdf_text.py` to extract text from a PDF. It tries `pypdf`, then `pdfplumber`, then `pdftotext` if available.

Example:
- `python3 scripts/extract_pdf_text.py /path/to/paper.pdf --json /path/to/paper.json`

If extraction fails, ask the user for a text export or request permission to install a PDF library.

## Step 2: Build a Paper Card

Summarize essential metadata before deeper analysis:
- Title, authors, venue/year (if available)
- Problem statement / task
- Main contributions (3-6 bullets)
- Key datasets, baselines, metrics

## Step 3: Produce the Requested Output

Use the templates in `references/output_templates.md`.

Guidelines:
- Keep math readable: explain equations in plain language and define symbols.
- Emphasize empirical evidence: cite key numbers and compare baselines.
- Point out assumptions, missing ablations, or unclear settings.
- When possible, reference section names or page numbers.

## Step 4: Critical Questions

Include a short list of questions that would help validate or extend the work:
- Robustness, generalization, ablation gaps
- Data/label leakage risks
- Reproducibility gaps (hyperparameters, compute, preprocessing)

## Resources

### scripts/
- `extract_pdf_text.py`: Extract text (and per-page text) from PDFs.

### references/
- `output_templates.md`: Output formats for quick, deep, review, and reproduction modes.
