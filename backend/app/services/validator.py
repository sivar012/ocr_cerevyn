import re
from typing import Dict, Any, List

def validate_data(data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate the parsed data fields for multiple records.
    Returns a dictionary indicating status of each field and overall status.
    """
    overall_status = True
    records_validation = []
    
    for data in data_list:
        record_status = {
            "is_valid": True,
            "fields": {}
        }
        
        # 1. Validate Name
        name = data.get("Name")
        if name and isinstance(name, str) and re.match(r'^[A-Za-z0-9\s]+$', name.strip()):
            record_status["fields"]["Name"] = {"valid": True, "message": "OK"}
        else:
            record_status["fields"]["Name"] = {"valid": False, "message": "Must be non-empty and alphanumeric."}
            record_status["is_valid"] = False
            overall_status = False
            
        # 2. Validate Amount
        amount = data.get("Amount")
        if amount is not None and isinstance(amount, (int, float)) and amount > 0:
            record_status["fields"]["Amount"] = {"valid": True, "message": "OK"}
        else:
            record_status["fields"]["Amount"] = {"valid": False, "message": "Must be a numeric value greater than 0."}
            record_status["is_valid"] = False
            overall_status = False
            
        # 3. Validate Date
        date_str = data.get("Date")
        if date_str and isinstance(date_str, str) and re.match(r'^\d{4}-\d{2}-\d{2}$', date_str.strip()):
            record_status["fields"]["Date"] = {"valid": True, "message": "OK"}
        else:
            record_status["fields"]["Date"] = {"valid": False, "message": "Must be in YYYY-MM-DD format."}
            record_status["is_valid"] = False
            overall_status = False
            
        # 4. Validate ID
        doc_id = data.get("ID")
        if doc_id and isinstance(doc_id, str) and doc_id.strip().isalnum():
            record_status["fields"]["ID"] = {"valid": True, "message": "OK"}
        else:
            record_status["fields"]["ID"] = {"valid": False, "message": "Must be alphanumeric and non-empty."}
            record_status["is_valid"] = False
            overall_status = False
            
        records_validation.append(record_status)
        
    return {
        "is_valid": overall_status,
        "records": records_validation
    }
