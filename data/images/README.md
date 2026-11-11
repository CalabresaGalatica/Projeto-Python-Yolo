# Imagens para alimentar o YOLO

Coloque aqui as imagens que você quiser usar para alimentar o modelo YOLO ou para testes manuais.

Caminho do diretório:

- `data/images`

Você pode adicionar imagens em qualquer formato suportado, como `.jpg`, `.jpeg` ou `.png`.

Exemplo de uso:

```python
from pathlib import Path
from app.config import DATASET_IMAGES_DIR

print(DATASET_IMAGES_DIR)
```

Esse diretório pode ser usado para:
- testar detecção em imagens estáticas;
- preparar dados para treinamento ou validação;
- manter imagens de referência para o projeto.
