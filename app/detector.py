from __future__ import annotations

from typing import Any

from ultralytics import YOLO

from app.config import TRADUCOES, YOLO_CONFIDENCE, YOLO_MODEL_NAME


def prepare_model(model: YOLO) -> YOLO:
    for class_id, name in model.names.items():
        if name in TRADUCOES:
            model.names[class_id] = TRADUCOES[name]
    return model


def load_model(model_name: str = YOLO_MODEL_NAME) -> YOLO:
    model = YOLO(model_name)
    return prepare_model(model)


def detect_frame(model: YOLO, frame: Any, conf: float = YOLO_CONFIDENCE):
    resultados = model.predict(source=frame, conf=conf, verbose=False)
    if not resultados:
        return frame
    return resultados[0].plot(conf=True, line_width=2, font_size=1.0)


def detect_image_file(model: YOLO, image_path: str, conf: float = YOLO_CONFIDENCE):
    resultados = model.predict(source=image_path, conf=conf, verbose=False)
    if not resultados:
        return None
    return resultados[0].plot(conf=True, line_width=2, font_size=1.0)
