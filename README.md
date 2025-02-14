# Financial Data Extraction Using Open-Source LLMs

## Overview
This project processes the provided PDF files and extracts key financial entities using Python. The key data points include:
- **Company Name**
- **Report Date**
- **Profit Before Tax**
- **Additional Details** (e.g., Revenue from Operations)

The extracted information is saved in a structured JSON format.

## Setup and Installation

1. **Download the PDF Files**
   - Download the PDFs from the provided links.
   - Rename them as needed (e.g., `Amaar raja Earnings Summary.pdf` and `1_FinancialResults_05022025142214.pdf`) and place them in the same directory as the Python script.

2. **Install Dependencies**
   Ensure you have Python 3.8+ installed, then install the required library:
   ```bash
   pip install pdfplumber
