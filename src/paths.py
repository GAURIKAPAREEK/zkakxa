import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve_path(relative_path: str) -> str:
    """Resolve a path relative to the DataSentinel project root."""
    return os.path.normpath(os.path.join(PROJECT_ROOT, relative_path))
