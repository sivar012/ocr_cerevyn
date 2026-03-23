import re
from typing import Dict, Any, List

def parse_extracted_text(text: str) -> List[Dict[str, Any]]:
    """
    Parse OCR text to extract structured data using regex and heuristics.
    Handles multiple invoices in the same document.
    """
    # Split text into blocks by "Page" or "INVOICE #" to isolate multiple invoices
    blocks = re.split(r'(?i)--- page \d+ ---|invoice\s*#\d+', text)
    
    results = []
    
    for block in blocks:
        if not block.strip():
            continue
            
        parsed_data = {
            "Name": None,
            "Amount": None,
            "Date": None,
            "ID": None
        }
        
        # Look for Name (allowing numbers now for "Customer 1")
        name_match = re.search(r'(?i)(?:name|customer)\s*[:\-]?\s*([A-Za-z0-9\s]+)(?:\n|$)', block)
        if name_match:
            parsed_data["Name"] = name_match.group(1).strip()
            
        # Look for Amount
        amount_match = re.search(r'(?i)(?:total|amount|due)\s*[:\-]?\s*[\$]?\s*([\d\,\.]+)', block)
        if amount_match:
            try:
                val_str = amount_match.group(1).replace(',', '')
                parsed_data["Amount"] = float(val_str)
            except ValueError:
                pass
                
        # Look for Date
        date_match = re.search(r'(?i)(?:date)\s*[:\-]?\s*(\d{2,4}[\-\/]\d{1,2}[\-\/]\d{1,4})', block)
        if date_match:
            parsed_data["Date"] = date_match.group(1).strip()
            
        # Look for ID (ignore invoice # as we split by it, just look for ID:)
        id_match = re.search(r'(?i)(?:id)\s*[:\-]?\s*#?\s*([A-Za-z0-9\-\_]+)', block)
        if id_match:
            parsed_data["ID"] = id_match.group(1).strip()
            
        # Only add to results if we found at least one feature
        if any(parsed_data.values()):
            results.append(parsed_data)
            
    # Default fallback
    if not results:
        results.append({"Name": None, "Amount": None, "Date": None, "ID": None})
        
    return results
