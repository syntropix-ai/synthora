from typing import AnyStr
import requests
from bs4 import BeautifulSoup
from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


@tool
def webpage(url: str) -> Result[str, Exception]:
    r"""Retrieve the text content of a web page.
    
    Args:
        url (str): The URL of the web page to retrieve.
        
    Returns:
        Result[str, Exception]: A Result object containing either:
            - Ok(str): The text content of the web page if successful
            - Err(Exception): An error with description if the retrieval fails
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        text = " ".join(line for line in lines if line)[:4096] + "..."
        return Ok(text)
    except Exception as e:
        return Err(e, f"Error: {e}\n Probably it is an invalid URL.")

