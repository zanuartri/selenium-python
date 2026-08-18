from pathlib import Path


def make_temp_upload_file(directory: Path, name: str = "upload_sample.txt", content: str = "selenium upload test") -> Path:
    """Create a small throwaway file to feed into a file-input element."""
    file_path = directory / name
    file_path.write_text(content, encoding="utf-8")
    return file_path
