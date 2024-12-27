from trafilatura import fetch_url, extract, html2txt
from synthora.toolkits.decorators import tool
from synthora.toolkits.base import BaseToolkit

class TrafilaturaWebpageReader(BaseToolkit):
    r""" Extracts the main content from a webpage using the trafilatura library.
    """
    def __init__(self, full_text: bool = False):
        self.full_text = full_text
        super().__init__()
        
    @tool
    def trafilatura_webpage_reader(self, url: str) -> str:
        r""" Extracts the main content from a webpage using the trafilatura library.
        
        Args:
            url (str): The URL of the webpage to read.
            
        Returns:
            str: The main content of the webpage.
        """
        html = fetch_url(url)
        text = extract(html) if not self.full_text else html2txt(html)
        return text
