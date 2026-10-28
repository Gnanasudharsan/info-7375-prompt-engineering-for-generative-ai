"""Allow-listed fetcher. CONTRACT.md "Refuses": any other host raises ValueError."""
from urllib.parse import urlsplit

import requests

ALLOWED_HOSTS = frozenset({"boards-api.greenhouse.io"})

BOARD_URL = "https://boards-api.greenhouse.io/v1/boards/anthropic/jobs?content=true"


def check_allowed(url: str) -> None:
    parts = urlsplit(url)
    if parts.scheme != "https":
        raise ValueError(f"refusing non-https URL: {url!r}")
    if parts.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"refusing host not on allow-list: {parts.hostname!r}")


def fetch(url: str, session=None, timeout: float = 30.0) -> bytes:
    """Return the raw response body. The allow-list check runs before any request."""
    check_allowed(url)
    session = session or requests.Session()
    # No redirects: a redirect could otherwise lead off the allow-listed host.
    response = session.get(url, timeout=timeout, allow_redirects=False)
    response.raise_for_status()
    return response.content
