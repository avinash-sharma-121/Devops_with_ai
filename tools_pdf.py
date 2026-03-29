from strands import tool
from PyPDF2 import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

@tool
def read_pdf(file_path: str) -> str:
    """Read a PDF file and return extracted text"""
    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text[:5000]  # limit for LLM
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    

@tool
def generate_pdf(topic: str, output_file: str = "output.pdf") -> str:
    """Generate a PDF report based on a topic"""
    try:
        # basic content (LLM will expand via prompt)
        content = f"""
        Report: {topic}

        This report covers key aspects of {topic}.
        - Overview
        - Best Practices
        - Tools and Technologies
        - Conclusion
        """

        doc = SimpleDocTemplate(output_file)
        styles = getSampleStyleSheet()

        elements = []
        elements.append(Paragraph(content, styles["Normal"]))

        doc.build(elements)

        return f"PDF generated successfully: {output_file}"
    except Exception as e:
        return f"Error generating PDF: {str(e)}"
