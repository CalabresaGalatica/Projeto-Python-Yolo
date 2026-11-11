from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_IMAGES_DIR = BASE_DIR / "data" / "images"
YOLO_MODEL_NAME = "yolo11n.pt"
YOLO_CONFIDENCE = 0.25
IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp"]

TRADUCOES = {
    "person": "Pessoa",
    "cell phone": "Celular",
    "bottle": "Garrafa",
    "cup": "Xicara",
    "laptop": "Notebook",
    "mouse": "Mouse",
    "keyboard": "Teclado",
    "book": "Livro",
    "chair": "Cadeira",
    "tv": "Televisao",
    "backpack": "Mochila",
    "scissors": "Tesoura",
    "clock": "Relogio",
    "pen": "Caneta",
}
