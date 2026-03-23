from pydantic import BaseModel
from typing import List, Dict, Any

class ParseRequest(BaseModel):
    text: str

class ValidateRequest(BaseModel):
    data_list: List[Dict[str, Any]]
