import threading
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
from PIL import Image, ImageTk

from app.config import DATASET_IMAGES_DIR, YOLO_CONFIDENCE
from app.dataset import ensure_images_dir, list_images
from app.detector import detect_frame, load_model


class Aplicacao:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Reconhecimento de Objetos com IA - YOLO")
        self.janela.geometry("800x600")

        self.modelo = None
        self.modelo_carregando = False
        self.camera = None
        self.camera_ativa = False
        self.processando_frame = False
        self._lock = threading.Lock()

        self.area_imagem = tk.Label(self.janela, text="Câmera Desligada", bg="black", fg="white")
        self.area_imagem.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        painel_botoes = tk.Frame(self.janela)
        painel_botoes.pack(fill=tk.X, padx=10, pady=10)

        self.btn_iniciar = tk.Button(
            painel_botoes,
            text="Iniciar Câmera",
            command=self.iniciar_camera,
            bg="#4CAF50",
            fg="white",
        )
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)

        self.btn_parar = tk.Button(
            painel_botoes,
            text="Parar Câmera",
            command=self.parar_camera,
            bg="#ff9800",
            fg="white",
        )
        self.btn_parar.pack(side=tk.LEFT, padx=5)

        self.btn_imagem = tk.Button(
            painel_botoes,
            text="Detectar Imagem",
            command=self.selecionar_imagem,
            bg="#2196F3",
            fg="white",
        )
        self.btn_imagem.pack(side=tk.LEFT, padx=5)

        self.btn_sair = tk.Button(
            painel_botoes,
            text="Sair",
            command=self.fechar,
            bg="#f44336",
            fg="white",
        )
        self.btn_sair.pack(side=tk.RIGHT, padx=5)

        self._mostrar_diretorio_imagens()

    def _mostrar_diretorio_imagens(self):
        ensure_images_dir()
        imagens = list_images(DATASET_IMAGES_DIR)
        if imagens:
            print(f"Diretório de imagens do YOLO: {DATASET_IMAGES_DIR}")
        else:
            print(f"Diretório vazio: {DATASET_IMAGES_DIR}")

    def carregar_modelo(self):
        if self.modelo is not None:
            return

        self.modelo_carregando = True
        self.btn_iniciar.config(text="Carregando IA...", state="disabled")

        def tarefa():
            modelo = load_model()
            with self._lock:
                self.modelo = modelo
                self.modelo_carregando = False

            self.janela.after(0, self._finalizar_carregamento)

        threading.Thread(target=tarefa, daemon=True).start()

    def _finalizar_carregamento(self):
        self.btn_iniciar.config(text="Iniciar Câmera", state="normal")
        if self.modelo is not None:
            self.iniciar_camera()

    def iniciar_camera(self):
        if self.camera_ativa:
            return

        if self.modelo is None:
            self.carregar_modelo()
            return

        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            messagebox.showerror("Erro", "Não foi possível acessar a câmera.")
            return

        self.camera_ativa = True
        self.janela.after(30, self.atualizar_video)

    def selecionar_imagem(self):
        if self.modelo is None:
            self.carregar_modelo()
            return

        caminho = filedialog.askopenfilename(
            initialdir=str(DATASET_IMAGES_DIR),
            title="Selecione uma imagem para detectar",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp"), ("Todos os arquivos", "*.*")],
        )

        if not caminho:
            return

        self.parar_camera()
        self.area_imagem.configure(text="Processando imagem...")
        threading.Thread(target=self._processar_imagem_arquivo, args=(caminho,), daemon=True).start()

    def _processar_imagem_arquivo(self, caminho_arquivo):
        try:
            imagem = cv2.imread(caminho_arquivo)
            if imagem is None:
                raise ValueError("Arquivo de imagem inválido.")

            frame_anotado = detect_frame(self.modelo, imagem, conf=YOLO_CONFIDENCE)
            frame_rgb = cv2.cvtColor(frame_anotado, cv2.COLOR_BGR2RGB)
            imagem_pil = Image.fromarray(frame_rgb)
            imagem_tk = ImageTk.PhotoImage(image=imagem_pil)

            self.janela.after(0, lambda: self._atualizar_area_imagem(imagem_tk))
        except Exception as exc:
            self.janela.after(0, lambda: messagebox.showerror("Erro", f"Não foi possível processar a imagem: {exc}"))

    def processar_frame(self, frame):
        if self.modelo is None:
            return

        try:
            frame_anotado = detect_frame(self.modelo, frame, conf=YOLO_CONFIDENCE)
            frame_rgb = cv2.cvtColor(frame_anotado, cv2.COLOR_BGR2RGB)
            imagem_pil = Image.fromarray(frame_rgb)
            imagem_tk = ImageTk.PhotoImage(image=imagem_pil)

            self.janela.after(0, lambda: self._atualizar_area_imagem(imagem_tk))
        finally:
            self.processando_frame = False

    def _atualizar_area_imagem(self, imagem_tk):
        self.area_imagem.configure(image=imagem_tk, text="")
        self.area_imagem.image = imagem_tk

    def atualizar_video(self):
        if not self.camera_ativa or self.camera is None:
            return

        sucesso, frame = self.camera.read()
        if sucesso and not self.processando_frame:
            self.processando_frame = True
            threading.Thread(target=self.processar_frame, args=(frame.copy(),), daemon=True).start()

        self.janela.after(30, self.atualizar_video)

    def parar_camera(self):
        self.camera_ativa = False
        self.processando_frame = False
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self.area_imagem.configure(image="", text="Câmera Desligada")

    def fechar(self):
        self.parar_camera()
        self.janela.destroy()
