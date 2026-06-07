from crewai_tools import SerperDevTool
from crewai.tools import tool
import fitz
from dotenv import load_dotenv

load_dotenv()

search_tool = SerperDevTool()

@tool("read_resume")
def resume_read_tool(file_path: str) -> str:
    """Reads and returns the full text content of a PDF resume file."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading file: {str(e)}"