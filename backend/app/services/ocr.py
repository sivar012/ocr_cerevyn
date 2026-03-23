import cv2
import pytesseract
from PIL import Image
import numpy as np
import io
import fitz  # PyMuPDF

# Configure Tesseract path explicitly since it's not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_bytes: bytearray) -> np.ndarray:
    """
    Preprocess image for better OCR accuracy.
    Converts to grayscale and applies thresholding.
    """
    # Convert bytearray to numpy array then to cv2 image
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    # Using Otsu's thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh

def perform_ocr(image_bytes: bytearray) -> str:
    """
    Perform OCR on the uploaded image.
    """
    try:
        # Preprocess the image
        processed_img = preprocess_image(image_bytes)
        
        # Convert cv2 image back to PIL Image for tesseract
        pil_img = Image.fromarray(processed_img)
        
        # Perform OCR
        text = pytesseract.image_to_string(pil_img)
        return text
    except Exception as e:
        # Fallback if cv2 fails (e.g., for some PDFs converted to images)
        print(f"Preprocessing failed: {e}. Trying raw OCR.")
        try:
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image)
            return text
        except Exception as inner_e:
            print(f"Raw OCR also failed: {inner_e}")
            return ""

def perform_ocr_on_pdf(pdf_bytes: bytes) -> str:
    """
    Convert PDF pages to images and perform OCR on each.
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=300)
            img_bytes = pix.tobytes("png")
            page_text = perform_ocr(bytearray(img_bytes))
            full_text += f"--- Page {page_num + 1} ---\n{page_text}\n"
        return full_text
    except Exception as e:
        print(f"PDF OCR failed: {e}")
        return ""
