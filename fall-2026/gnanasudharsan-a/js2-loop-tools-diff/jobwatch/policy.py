"""GATE §6 permission policy, enforced in code. Cases B1-B16 in BOUNDARY_TESTS.md.

Every refusal raises PolicyViolation, so a refusal is never confused with a crash.
"""
from pathlib import Path
from urllib.parse import urlsplit

ALLOWED_HOSTS = frozenset({"boards-api.greenhouse.io", "api.ashbyhq.com", "api.lever.co"})
ALLOWED_METHODS = frozenset({"GET"})
READ_DIRS = ("persona", "prompts", "state")
READ_FILES = ("gate_config.json", "boards.json")
WRITE_DIRS = ("runs", "state")
DELETE_DIRS = ("state",)


class PolicyViolation(Exception):
    """An action GATE §6 does not allow. Stops the whole run (GATE §5)."""


class Policy:
    def __init__(self, root):
        self.root = Path(root).resolve()

    # --- network ---------------------------------------------------------------

    def check_url(self, url: str, method: str = "GET") -> None:
        if method.upper() not in ALLOWED_METHODS:
            raise PolicyViolation(f"method not allowed: {method!r}")
        parts = urlsplit(url)
        if parts.scheme != "https":
            raise PolicyViolation(f"not https: {url!r}")
        if parts.username is not None or parts.password is not None:
            raise PolicyViolation(f"credentials in URL: {url!r}")
        try:
            port = parts.port
        except ValueError as exc:
            raise PolicyViolation(f"bad port in URL: {url!r}") from exc
        if port not in (None, 443):
            raise PolicyViolation(f"non-default port: {url!r}")
        # Exact hostname match (GATE §7 #3): no substring, suffix, or prefix test.
        if parts.hostname not in ALLOWED_HOSTS:
            raise PolicyViolation(f"host not on allow-list: {parts.hostname!r}")

    # --- files -----------------------------------------------------------------

    def _resolve(self, path) -> Path:
        p = Path(path)
        if not p.is_absolute():
            p = self.root / p
        # Resolves symlinks and ".." (GATE §7 #2); works for paths that do not exist yet.
        return p.resolve()

    def _inside(self, resolved: Path, dirname: str) -> bool:
        # The allowed root is root/<dirname> taken literally, not resolved, so a
        # symlinked runs/ or state/ that points elsewhere allows nothing.
        # Path-component comparison, never a string prefix (GATE §7 #1).
        allowed = self.root / dirname
        return allowed in resolved.parents

    def check_path(self, path, mode: str) -> Path:
        """Return the resolved path if `mode` ("read" or "write") is allowed."""
        resolved = self._resolve(path)
        if mode == "read":
            if any(self._inside(resolved, d) for d in READ_DIRS):
                return resolved
            if any(resolved == self.root / f for f in READ_FILES):
                return resolved
        elif mode == "write":
            if any(self._inside(resolved, d) for d in WRITE_DIRS):
                return resolved
        else:
            raise ValueError(f"mode must be 'read' or 'write', not {mode!r}")
        raise PolicyViolation(f"{mode} not allowed: {path} (resolves to {resolved})")

    def check_delete(self, path, approved: bool = False) -> Path:
        """Deleting or resetting a file in state/ needs approved=True (--i-approve)."""
        resolved = self._resolve(path)
        if not any(self._inside(resolved, d) for d in DELETE_DIRS):
            raise PolicyViolation(f"delete not allowed outside state/: {path}")
        if approved is not True:
            raise PolicyViolation(f"delete of {path} needs --i-approve")
        return resolved
