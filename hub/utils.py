import pytesseract
from pdf2image import convert_from_path
import os
from django.conf import settings

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using OCR.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        str: Extracted text from the PDF.
    """
    text = ""
    try:
        # Convert PDF to images
        # poppler_path might need to be configured depending on OS/Install
        # For now assuming it's in PATH
        images = convert_from_path(file_path)
        
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
            
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
        
    return text

def get_ai_tags(text):
    """
    STUB: Uses an LLM to generate tags for the given text.
    
    Args:
        text (str): The text content to analyze.
        
    Returns:
        str: Comma-separated tags.
    """
    # Placeholder logic
    tags = []
    text_lower = text.lower()
    
    if "solar" in text_lower:
        tags.append("Solar")
    if "pump" in text_lower:
        tags.append("Pump Control")
    if "inverter" in text_lower or "vfd" in text_lower:
        tags.append("Hardware")
    if "fault" in text_lower or "error" in text_lower:
        tags.append("Troubleshooting")
        
    if not tags:
        tags.append("General")
        
    return ", ".join(tags)

def get_rag_answer(query, context_text):
    """
    STUB: Simulate RAG response.
    
    Args:
        query (str): User question.
        context_text (str): Relevant text from DB.
        
    Returns:
        str: AI generated answer.
    """
    return f"AI Answer to '{query}' based on available documentation. (This is a stub response)."

def generate_faqs(text):
    """
    STUB: Analyzes text to auto-generate FAQs.
    
    Args:
        text (str): Content text from manual.
        
    Returns:
        list: List of dicts {'question': str, 'answer': str, 'category': str}
    """
    # Placeholder logic that pretends to find FAQs
    faqs = []
    text_lower = text.lower()
    
    if "error" in text_lower or "fault" in text_lower:
        faqs.append({
            'question': "What do I do if I see an Error Code?",
            'answer': "Refer to the troubleshooting section of this manual for specific error codes.",
            'category': "Troubleshooting"
        })
    
    if "install" in text_lower or "wiring" in text_lower:
        faqs.append({
            'question': "How do I install this device?",
            'answer': "Ensure all wiring follows the diagram in the Installation chapter.",
            'category': "Installation"
        })
        
    # Fallback to ensure we see the feature working if extracted text exists but is weird
    if not faqs and len(text) > 10:
        faqs.append({
            'question': "General Information",
            'answer': "This is an auto-generated placeholder. The system detected content but no specific keywords for FAQs.",
            'category': "General"
        })
        
    return faqs
