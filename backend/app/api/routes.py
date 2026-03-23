from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from app.services.ocr import perform_ocr
from app.services.parser import parse_extracted_text
from app.services.validator import validate_data
from app.schemas.document import ParseRequest, ValidateRequest

router = APIRouter()

@router.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    """
    Endpoint to perform OCR and extract text from an image or PDF file.
    """
    if not (file.content_type.startswith("image/") or file.content_type == "application/pdf"):
        return JSONResponse(status_code=400, content={"error": "Only image and PDF files are supported currently."})
        
    try:
        contents = await file.read()
        if file.content_type == "application/pdf":
            from app.services.ocr import perform_ocr_on_pdf
            raw_text = perform_ocr_on_pdf(contents)
        else:
            raw_text = perform_ocr(contents)
            
        return {"raw_text": raw_text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/parse")
async def parse_text(request: ParseRequest):
    """
    Endpoint to parse extracted OCR text into structured data.
    """
    try:
        parsed_data = parse_extracted_text(request.text)
        return {"structured_data": parsed_data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/validate")
async def validate_parsed_data(request: ValidateRequest):
    """
    Endpoint to validate parsed structured data.
    """
    try:
        validation_results = validate_data(request.data_list)
        return {"validation_status": validation_results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/process")
async def process_document(file: UploadFile = File(...)):
    """
    Endpoint to process an uploaded document through the entire pipeline (OCR -> Parse -> Validate).
    """
    if not (file.content_type.startswith("image/") or file.content_type == "application/pdf"):
        return JSONResponse(status_code=400, content={"error": "Only image and PDF files are supported currently."})
        
    try:
        contents = await file.read()
        
        # 1. Perform OCR
        if file.content_type == "application/pdf":
            from app.services.ocr import perform_ocr_on_pdf
            raw_text = perform_ocr_on_pdf(contents)
        else:
            raw_text = perform_ocr(contents)
        
        # 2. Parse extracted text
        parsed_data = parse_extracted_text(raw_text)
        
        # 3. Validate data
        validation_results = validate_data(parsed_data)
        
        return {
            "raw_text": raw_text,
            "structured_data": parsed_data,
            "validation_status": validation_results
        }
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
