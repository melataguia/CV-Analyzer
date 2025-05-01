import os
import pdfplumber
import docx
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import re
from unidecode import unidecode
from groq import Groq

# Initialisation du client Groq avec la clé API depuis l'environnement
client = Groq(
    api_key="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"
)

# Fonction pour envoyer le texte extrait à l'API Groq et obtenir un résumé structuré
def get_summary_from_groq(text):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Please summarize this CV and extract key points: {text}",
                }
            ],
            model="deepseek-r1-distill-llama-70b"  # Vérifie que le modèle est correct (nom actualisé possible)
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Erreur avec l'API Groq: {e}")

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Erreur extraction PDF classique : {e}")

    if not text.strip():
        text = extract_text_with_ocr(file_path)

    return text

def extract_text_with_ocr(file_path):
    text = ""
    try:
        images = convert_from_path(file_path)
        for image in images:
            text += pytesseract.image_to_string(image, lang='fra+eng') + "\n"
    except Exception as e:
        raise RuntimeError(f"OCR error: {e}")
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def clean_text(text):
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return unidecode(text).strip()

def parse_cv(file_path):
    _, ext = os.path.splitext(file_path.lower())

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF or DOCX.")
    
    cleaned_text = clean_text(text)
    summary = get_summary_from_groq(cleaned_text)
    return summary
