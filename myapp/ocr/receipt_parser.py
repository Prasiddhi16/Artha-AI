import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from PIL import Image
import re
from datetime import date
import os
def extract_receipt_data(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    text_lower = text.lower()
    
    matches = re.findall(r'\d{1,3}(?:,\d{3})*\.\d{2}', text)
    amounts = [float(m.replace(',', '')) for m in matches]
    
    
    final_amount = max(amounts) if amounts else 0.0

    category = "Others"
    transaction_type = "Expense" 

    if "connectips" in text_lower or "payment transaction" in text_lower:
        category = "Education/Payments" 
        transaction_type = "Expense"

    # Keywords for Income (Salary/Refunds)
    income_keywords = ["salary", "deposit into account", "refund", "credited"]
    if any(word in text_lower for word in income_keywords) and "payment" not in text_lower:
        transaction_type = "Income"

    return {
        "amount": final_amount,
        "category": category,
        "type": transaction_type,
        "date": date.today()
    }