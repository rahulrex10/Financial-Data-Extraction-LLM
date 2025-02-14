import pdfplumber
import re
import json

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using pdfplumber.
    Returns the concatenated text from all pages.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    return text

def extract_financial_entities(text):
    """
    Extracts key financial entities from the given text.
    Looks for:
      - Company Name (e.g., Eveready Industries India Ltd. or Amara Raja Energy & Mobility Limited)
      - Report Date (via a Month Day, Year pattern)
      - Profit Before Tax (a number following "Profit before Tax")
      - Additional Detail: Revenue from Operations
    Returns a dictionary with the extracted data.
    """
    # Company Name extraction
    company_name = None
    if re.search(r"Eveready Industries India Ltd\.?", text, re.IGNORECASE):
        company_name = re.search(r"(Eveready Industries India Ltd\.?)", text, re.IGNORECASE).group(1).strip()
    elif re.search(r"Amara Raja Energy & Mobility Limited", text, re.IGNORECASE):
        company_name = re.search(r"(Amara Raja Energy & Mobility Limited)", text, re.IGNORECASE).group(1).strip()

    # Report Date extraction (looking for a date like "Month Day, Year")
    report_date = None
    date_match = re.search(r"(\w+\s+\d{1,2},\s+\d{4})", text)
    if date_match:
        report_date = date_match.group(1).strip()

    # Profit Before Tax extraction
    # Using DOTALL flag to capture numbers across lines
    profit_before_tax = None
    pbt_match = re.search(r"Profit\s+before\s+Tax(?:.*?)([\d,]+\.\d+)", text, re.IGNORECASE | re.DOTALL)
    if pbt_match:
        profit_before_tax = pbt_match.group(1).strip()

    # Additional detail: Revenue from Operations extraction
    revenue = None
    rev_match = re.search(r"Revenue\s+from\s+operations(?:[:\-\s]+)([\d,]+\.\d+)", text, re.IGNORECASE)
    if rev_match:
        revenue = rev_match.group(1).strip()

    additional_details = {}
    if revenue:
        additional_details["Revenue from Operations"] = revenue

    return {
        "Company Name": company_name,
        "Report Date": report_date,
        "Profit Before Tax": profit_before_tax,
        "Additional Details": additional_details
    }

def process_pdf(pdf_path):
    """
    Extracts text from the PDF and then extracts financial entities.
    Returns the dictionary of extracted data.
    """
    text = extract_text_from_pdf(pdf_path)
    entities = extract_financial_entities(text)
    return entities

if __name__ == "__main__":
    # List your PDF files. If they are not in the same directory, use full file paths.
    pdf_files = [
        r"C:\Users\Rahul\Downloads\Amaar raja Earnings Summary.pdf", #  eg, https://drive.google.com/file/d/1vv9Jo4TY8FZRxwigcIpSbmKfGDXGdmKw/view?usp=drive_link 
        r"C:\Users\Rahul\Downloads\1_FinancialResults_05022025142214.pdf"   # eg, https://drive.google.com/file/d/1xmce96ePG4oz-6p5zvfXWBNS_c3y5khL/view?usp=drive_link
      
    ]
    
    results = {}
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file} ...")
        extracted_data = process_pdf(pdf_file)
        results[pdf_file] = extracted_data
    
    # Save aggregated results to a JSON file
    output_file = "extracted_financial_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    
    print(f"\nExtraction complete. Results saved to {output_file}")
