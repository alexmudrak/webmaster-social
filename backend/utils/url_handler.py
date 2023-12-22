from urllib.parse import urljoin, urlparse


async def get_correct_url(original_url: str, parsed_url: str) -> str:
    """
    Combines the original URL and a relative URL to obtain an absolute URL.

    Parameters:
    - original_url (str): The original URL, e.g., "http://domain.com/path".
    - parsed_url (str): The relative URL, e.g., "/some-path-to-node/".

    Return:
    - str: "http://domain.com/some-path-to-node/"
    """
    base_url_parsed = urlparse(original_url)
    correct_url = urljoin(base_url_parsed.geturl(), parsed_url)

    return correct_url
