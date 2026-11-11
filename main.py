import tkinter as tk

from app.camera_app import Aplicacao


if __name__ == "__main__":
    raiz = tk.Tk()
    app = Aplicacao(raiz)
    raiz.protocol("WM_DELETE_WINDOW", app.fechar)
    raiz.mainloop()