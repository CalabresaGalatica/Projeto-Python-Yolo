# Reconhecimento de Objetos com IA - YOLO

Projeto em Python para detecção de objetos em tempo real usando YOLO e OpenCV, com interface gráfica em Tkinter.

## Requisitos

- Python 3.11+
- pip

## Instalação

```bash
python -m pip install -r requirements.txt
```

## Execução

```bash
python main.py
```

## Estrutura do projeto

- `main.py` - ponto de entrada do programa
- `app/` - módulos da aplicação
- `data/images/` - pasta para imagens de teste e referência
- `requirements.txt` - dependências do projeto

## Observações

- O modelo YOLO `yolo11n.pt` pode ser baixado automaticamente na primeira execução.
- A pasta `data/images` é o local recomendado para adicionar imagens para testes e alimentação do modelo.
