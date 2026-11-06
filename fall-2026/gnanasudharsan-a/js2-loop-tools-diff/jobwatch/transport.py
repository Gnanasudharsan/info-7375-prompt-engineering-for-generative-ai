"""The real transport: one HTTPS GET with urllib, stdlib only (GATE §6).

policy.check_url runs before every request. Redirects are never followed: a
redirect to another host raises PolicyViolation (stops the run); a same-host
redirect is returned as its 3xx Response for the loop to record. No cookie
jar, no auth headers, no environment proxies.
"""
import http.client
import socket
import ssl
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlsplit

from .policy import PolicyViolation

USER_AGENT = "jobwatch-js2/1.0 (INFO 7375 course project)"
CHUNK_BYTES = 64 * 1024


@dataclass
class Response:
    status: int
    body: bytes
    headers: dict = field(default_factory=dict)


class TransportTimeout(Exception):
    """The request did not finish within its timeout."""


class TransportError(Exception):
    """Connection-level failure (DNS, refused, TLS, reset)."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # urllib then raises HTTPError carrying the 3xx response


def _read_with_deadline(fp, deadline: float) -> bytes:
    # The socket timeout bounds each read, not the whole body; this bounds the total.
    chunks = []
    while True:
        if time.monotonic() > deadline:
            raise TransportTimeout("body read exceeded the request timeout")
        chunk = fp.read(CHUNK_BYTES)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


class UrllibTransport:
    """Callable as transport(url, timeout) -> Response, the interface run_loop uses."""

    def __init__(self, policy):
        self.policy = policy
        self.opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),  # ignore HTTPS_PROXY: connect to the allowed host only
            urllib.request.HTTPSHandler(context=ssl.create_default_context()),
            _NoRedirect(),
        )

    def __call__(self, url: str, timeout: float) -> Response:
        self.policy.check_url(url, method="GET")
        request = urllib.request.Request(url, method="GET", headers={
            "User-Agent": USER_AGENT, "Accept": "application/json"})
        deadline = time.monotonic() + timeout
        try:
            with self.opener.open(request, timeout=timeout) as resp:
                body = _read_with_deadline(resp, deadline)
                return Response(resp.status, body, dict(resp.headers.items()))
        except urllib.error.HTTPError as err:
            headers = dict(err.headers.items()) if err.headers else {}
            if 300 <= err.code < 400:
                self._check_redirect(url, headers)
            try:
                body = _read_with_deadline(err, deadline)
            except (OSError, http.client.HTTPException):
                body = b""
            return Response(err.code, body, headers)
        except urllib.error.URLError as err:
            if isinstance(err.reason, (socket.timeout, TimeoutError)):
                raise TransportTimeout(str(err.reason)) from err
            raise TransportError(str(err.reason)) from err
        except (socket.timeout, TimeoutError) as err:
            raise TransportTimeout(str(err)) from err
        except (OSError, http.client.HTTPException) as err:
            raise TransportError(f"{type(err).__name__}: {err}") from err

    def _check_redirect(self, url: str, headers: dict) -> None:
        location = next((v for k, v in headers.items() if k.lower() == "location"), None)
        if location is None:
            return
        target = urljoin(url, location)
        if urlsplit(target).hostname != urlsplit(url).hostname:
            raise PolicyViolation(f"redirect to another host refused: {url} -> {target}")
        self.policy.check_url(target, method="GET")
