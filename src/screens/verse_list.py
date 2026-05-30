"""
Tela de versículos — leitura com tipografia agradável e navegação entre capítulos.
"""

import tkinter as tk
from tkinter import ttk
from src.database.db import get_verses, is_chapter_read, mark_chapter_read


class VerseList(tk.Frame):
    def __init__(self, parent, theme, navigate_back, **kwargs):
        super().__init__(parent, **kwargs)
        self.theme = theme
        self.navigate_back = navigate_back
        self._book_name = ""
        self._chapter = 0
        self._total_chapters = 0
        self._build()

    def _build(self):
        BG      = "#1e1e2e"
        BG_CARD = "#252538"

        # Barra de ações
        action_bar = tk.Frame(self, bg=BG)
        action_bar.pack(fill="x", padx=20, pady=(14, 8))

        self._back_btn = tk.Button(
            action_bar, text="← Voltar",
            font=("Segoe UI", 11, "bold"),
            bg="#2a2a4e", fg="#a78bfa",
            activebackground="#3a3a6e", activeforeground="#c8b8ff",
            relief="flat", cursor="hand2", padx=14, pady=6,
            command=self.navigate_back
        )
        self._back_btn.pack(side="left")

        self._read_btn = tk.Button(
            action_bar, text="○  Marcar como lido",
            font=("Segoe UI", 11, "bold"),
            relief="flat", cursor="hand2",
            padx=14, pady=6,
            command=self._toggle_read
        )
        self._read_btn.pack(side="right")

        # Navegação entre capítulos
        nav = tk.Frame(self, bg=BG_CARD)
        nav.pack(fill="x", padx=20, pady=(0, 10))

        self._prev_btn = tk.Button(
            nav, text="‹  Anterior",
            font=("Segoe UI", 11),
            bg=BG_CARD, fg="#7c7caa",
            activebackground="#2a2a4e", activeforeground="#a78bfa",
            relief="flat", cursor="hand2", padx=16, pady=8,
            command=self._prev_chapter
        )
        self._prev_btn.pack(side="left")

        self._chapter_lbl = tk.Label(nav, text="",
            font=("Segoe UI", 12, "bold"),
            bg=BG_CARD, fg="#c8b8ff")
        self._chapter_lbl.pack(side="left", expand=True)

        self._next_btn = tk.Button(
            nav, text="Próximo  ›",
            font=("Segoe UI", 11),
            bg=BG_CARD, fg="#7c7caa",
            activebackground="#2a2a4e", activeforeground="#a78bfa",
            relief="flat", cursor="hand2", padx=16, pady=8,
            command=self._next_chapter
        )
        self._next_btn.pack(side="right")

        # Área dos versículos (scrollable)
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 14))

        self._canvas = tk.Canvas(container, highlightthickness=0, bg=BG_CARD)
        sb = ttk.Scrollbar(container, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._verse_frame = tk.Frame(self._canvas, bg=BG_CARD)
        self._win = self._canvas.create_window((0, 0), window=self._verse_frame, anchor="nw")

        self._verse_frame.bind("<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>",
            lambda e: self._canvas.itemconfig(self._win, width=e.width))

    def load(self, book_name: str, chapter: int, total_chapters: int):
        self._book_name      = book_name
        self._chapter        = chapter
        self._total_chapters = total_chapters
        self._render()
        self._canvas.yview_moveto(0)

    def _render(self):
        BG_CARD = "#252538"
        BG_ROW  = "#2a2a40"

        # Atualiza navegação
        self._chapter_lbl.configure(
            text=f"Capítulo {self._chapter}  /  {self._total_chapters}"
        )
        self._prev_btn.configure(state="normal" if self._chapter > 1 else "disabled")
        self._next_btn.configure(state="normal" if self._chapter < self._total_chapters else "disabled")
        self._update_read_btn()

        # Versículos
        for w in self._verse_frame.winfo_children():
            w.destroy()

        verses = get_verses(self._book_name, self._chapter)

        for i, texto in enumerate(verses, start=1):
            # Linhas alternadas levemente
            row_bg = BG_ROW if i % 2 == 0 else BG_CARD

            row = tk.Frame(self._verse_frame, bg=row_bg, pady=2)
            row.pack(fill="x")

            # Número destacado
            num = tk.Label(row, text=f"{i}",
                font=("Segoe UI", 11, "bold"),
                width=4, anchor="ne",
                bg=row_bg, fg="#7c5cbf",
                pady=8)
            num.pack(side="left", anchor="n")

            # Separador vertical
            sep = tk.Frame(row, bg="#3a3a5e", width=2)
            sep.pack(side="left", fill="y", padx=(0, 12), pady=4)

            # Texto do versículo
            txt = tk.Label(row,
                text=texto,
                font=("Georgia", 13),
                bg=row_bg, fg="#dcd8ff",
                justify="left", anchor="w",
                wraplength=700, pady=8)
            txt.pack(side="left", fill="x", expand=True, padx=(0, 12))

            # Atualiza wraplength dinamicamente
            row.bind("<Configure>",
                lambda e, l=txt: l.configure(wraplength=max(e.width - 80, 200)))

    def _update_read_btn(self):
        read = is_chapter_read(self._book_name, self._chapter)
        if read:
            self._read_btn.configure(
                text="✅  Lido!", bg="#1a4a2a", fg="#34d399",
                activebackground="#1e5e30")
        else:
            self._read_btn.configure(
                text="○  Marcar como lido", bg="#2a2a4e", fg="#a78bfa",
                activebackground="#3a3a6e")

    def _toggle_read(self):
        read = is_chapter_read(self._book_name, self._chapter)
        mark_chapter_read(self._book_name, self._chapter, not read)
        self._update_read_btn()

    def _prev_chapter(self):
        if self._chapter > 1:
            self._chapter -= 1
            self._render()
            self._canvas.yview_moveto(0)

    def _next_chapter(self):
        if self._chapter < self._total_chapters:
            self._chapter += 1
            self._render()
            self._canvas.yview_moveto(0)