# AI Document Processing (OCR Cerevyn)

An AI-powered document processing web application that extracts and validates structured data from uploaded images and PDFs using Optical Character Recognition (OCR).

## Overview

This project consists of two main parts:
- **Backend (Python / FastAPI)**: Handles file uploads, performs OCR (via Tesseract/OpenCV), parses text, and validates document entities (Name, Amount, Date, ID).
- **Frontend (HTML / JS / CSS)**: A clean and responsive web interface for uploading documents via drag-and-drop and displaying the extracted, validated data alongside the raw OCR text.

## Features

- **Upload Interface**: Drag-and-drop or click to browse for Image/PDF files.
- **OCR Engine**: Utilizes Tesseract and PyMuPDF for robust text extraction.
- **Data Validation**: Automatically categorizes and validates fields (Name, Amount, Date, ID) found in the processed document.
- **RESTful API**: Fast and scalable API built with FastAPI.

## Tech Stack

### Backend
- **Framework**: FastAPI
- **OCR & Image Processing**: PyTesseract, OpenCV (cv2), Pillow, PyMuPDF (fitz)
- **Validation**: Pydantic
- **Server**: Uvicorn

### Frontend
- **Structure & Styling**: HTML5, Vanilla CSS
- **Logic**: Vanilla JavaScript
- **Typography**: Google Fonts (Inter)

## Project Structure

```
ocr_cerevyn/
├── backend/
│   ├── app/                 # FastAPI routes and server logic
│   ├── requirements.txt     # Python dependencies
│   └── venv/                # (Optional) Virtual environment
├── frontend/
│   ├── src/                 # CSS and JS source files
│   ├── public/              # Static assets (if any)
│   └── index.html           # Main entry point for the frontend UI
└── README.md                # Project documentation
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js (Optional, only for serving frontend via a simple server if needed)
- Tesseract OCR engine installed on your system.

### Running the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   The API will be available at `http://localhost:8000`.

### Running the Frontend

1. Simply open `frontend/index.html` in your web browser.
2. Alternatively, you can serve it via a local static file server:
   ```bash
   cd frontend
   npx serve .
   ```
   Or using Python's built-in HTTP server:
   ```bash
   cd frontend
   python -m http.server 3000
   ```

## License
MIT License
