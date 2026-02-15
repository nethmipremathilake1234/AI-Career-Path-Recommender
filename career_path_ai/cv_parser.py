import PyPDF2
import docx

def extract_text(file):

    name = file.filename.lower()

    if name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join(p.extract_text() or "" for p in reader.pages)

    elif name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join(p.text for p in doc.paragraphs)

    return ""
