import os
import re
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from ocrmac import OCR  # Correct import
import numpy as np

def extract_text_from_pdf(pdf_path):
    """Extract text from a digitized PDF using macOS built-in OCR."""
    # Initialize OCR
    ocr = ocrmac.OCR()  # Correct initialization
    
    # Convert PDF to images
    pages = convert_from_path(pdf_path)
    
    # Extract text from each page
    text_by_page = []
    for page in pages:
        # Convert PIL Image to numpy array
        page_array = np.array(page)
        # Perform OCR
        result = ocr.recognize(page_array)  # Correct method name
        text_by_page.append(result)
    
    return text_by_page

def get_student_name(text):
    """Extract student name from text."""
    name_match = re.search(r"Nome do\(a\) Aluno\(a\):\s*(.+?)\s*Matrícula", text)
    return name_match.group(1).strip() if name_match else None

def process_historico(reader, text_by_page, start_index, output_dir):
    """Process a single historico with retry logic."""
    attempts = 0
    max_attempts = 5
    current_writer = PdfWriter()
    current_pages = []
    
    while attempts < max_attempts:
        current_writer = PdfWriter()
        current_pages = []
        i = start_index
        
        while i < len(text_by_page):
            page_counter_match = re.search(r"Pág\. (\d+) de (\d+)", text_by_page[i])
            
            if len(current_pages) >= 4:
                attempts += 1
                break
            
            current_writer.add_page(reader.pages[i])
            current_pages.append(i)
            
            if page_counter_match:
                current_page = int(page_counter_match.group(1))
                total_pages = int(page_counter_match.group(2))
                
                if current_page == total_pages:
                    # Get student name from first page
                    student_name = get_student_name(text_by_page[current_pages[0]])
                    if not student_name:
                        student_name = f"Unknown_Student_{start_index}"
                    
                    if len(current_pages) <= 4:
                        output_path = os.path.join(output_dir, f"{student_name}.pdf")
                        with open(output_path, "wb") as f:
                            current_writer.write(f)
                        print(f"Saved: {student_name}.pdf ({len(current_pages)} pages)")
                        return i + 1
                    break
            i += 1
        
        attempts += 1
        if attempts == max_attempts:
            print(f"Warning: Skipping historico after {max_attempts} attempts (start_index: {start_index})")
            for j in range(start_index + 1, len(text_by_page)):
                if re.search(r"Pág\. 1 de \d+", text_by_page[j]):
                    return j
            return len(text_by_page)
    
    return len(text_by_page)

def split_pdf_by_historico(pdf_path, output_dir):
    """Split the PDF into individual historicos."""
    text_by_page = extract_text_from_pdf(pdf_path)
    reader = PdfReader(pdf_path)
    
    current_index = 0
    while current_index < len(text_by_page):
        current_index = process_historico(reader, text_by_page, current_index, output_dir)

if __name__ == "__main__":
    # Input PDF file
    input_pdf = "/path/to/pdf/example.pdf"
    
    # Output directory for separated PDFs
    output_directory = "/path/to/Gisele"
    os.makedirs(output_directory, exist_ok=True)
    
    # Split the PDF
    split_pdf_by_historico(input_pdf, output_directory)
