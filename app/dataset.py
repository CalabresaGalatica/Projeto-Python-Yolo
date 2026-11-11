from pathlib import Path

from app.config import DATASET_IMAGES_DIR, IMAGE_EXTENSIONS


def ensure_images_dir() -> Path:
    DATASET_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    return DATASET_IMAGES_DIR


def list_images(directory: str | Path | None = None, extensions: list[str] | None = None) -> list[str]:
    folder = Path(directory) if directory is not None else ensure_images_dir()
    valid_extensions = {ext.lower() for ext in (extensions or IMAGE_EXTENSIONS)}

    if not folder.exists():
        return []

    return sorted(
        str(path)
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in valid_extensions
    )
