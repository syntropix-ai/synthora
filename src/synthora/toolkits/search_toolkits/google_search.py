from googlesearch import search
from typing import AnyStr
import requests
from bs4 import BeautifulSoup
from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


@tool
def google_search(query: str) -> Result[str, Exception]:
    r"""Search Google and return a list of URLs.
    
    Args:
        query (str): The search query to look up on Google
        
    Returns:
        Result[str, Exception]: A Result object containing either:
            - Ok(str): A list of URLs if successful
            - Err(Exception): An error with description if the search fails
    """
    try:
        return Ok('\n\n'.join([str(item) for item in search(query, advanced=True)]))
    except Exception as e:
        return Err(e, f"Error: {e}\n Probably it is an invalid query.")
