from pypdf import PdfReader

def extract_pages(pdf_path):
    """
        Read one PDF. Returns a list of (page_number, text).
        page numbers start at 1.
    """
    reader = PdfReader(str(pdf_path))
    pages = []
    for num, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append((num, text))
    return pages

def chunk_text(text, size=800, overlap=100):
    """
        Split text into pieces of about `size` characters, overlapping a little.
        We try to cut a line break so a table row is not split in the middle.
    """
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            newline = text.rfind("\n", start, end)
            if newline > start + size // 2:
                end = newline
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = max(end - overlap, start + 1)
    return [c for c in chunks if c]