"""
Tela de capítulos — grade colorida com status de leitura.
"""

import tkinter as tk
from tkinter import ttk
from src.database.db import is_chapter_read, mark_chapter_read


class ChaptersScreen(tk.Frame):
    def __init__(self, parent, theme, navigate_to, navigate_back, **kwargs):
        super().__init__(parent, **kwargs)
        self.theme = theme
        self.navigate_to = navigate_to
        self.navigate_back = navigate_back
        self._book_name = ""
        self._total_chapters = 0
        self._build()

    def _build(self):
        BG = "#1e1e2e"

        # Botão voltar
        top_bar = tk.Frame(self, bg=BG)
        top_bar.pack(fill="x", padx=20, pady=(14, 6))

        self._back_btn = tk.Button(
            top_bar, text="← Voltar",
            font=("Segoe UI", 11, "bold"),
            bg="#2a2a4e", fg="#a78bfa",
            activebackground="#3a3a6e", activeforeground="#c8b8ff",
            relief="flat", cursor="hand2", padx=14, pady=6,
            command=self.navigate_back
        )
        self._back_btn.pack(side="left")

        self._progress_lbl = tk.Label(top_bar, text="",
            font=("Segoe UI", 11), bg=BG, fg="#6c6c9a")
        self._progress_lbl.pack(side="right")

        # Barra de progresso global do livro
        self._bar_bg = tk.Frame(self, bg="#2a2a3e", height=6)
        self._bar_bg.pack(fill="x", padx=20, pady=(0, 14))
        self._bar_fill = tk.Frame(self._bar_bg, bg="#a78bfa", height=6)
        self._bar_fill.place(relwidth=0, relheight=1)

        # Grade scrollable
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 14))

        self._canvas = tk.Canvas(container, highlightthickness=0, bg=BG)
        sb = ttk.Scrollbar(container, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._grid_frame = tk.Frame(self._canvas, bg=BG)
        win = self._canvas.create_window((0, 0), window=self._grid_frame, anchor="nw")
        self._grid_frame.bind("<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>",
            lambda e: self._canvas.itemconfig(win, width=e.width))

    def load(self, book_name: str, total_chapters: int):
        self._book_name = book_name
        self._total_chapters = total_chapters
        self._build_grid()

    def _build_grid(self):
        for w in self._grid_frame.winfo_children():
            w.destroy()

        BG = "#1e1e2e"
        COLS = 6
        read_count = 0

        for ch in range(1, self._total_chapters + 1):
            read = is_chapter_read(self._book_name, ch)
            if read:
                read_count += 1

            row_idx = (ch - 1) // COLS
            col_idx = (ch - 1) % COLS

            cell = tk.Frame(self._grid_frame, bg=BG, padx=5, pady=5)
            cell.grid(row=row_idx, column=col_idx, sticky="nsew")

            if read:
                bg_c, fg_c, hover_c = "#2d1b6e", "#c4b5fd", "#3d2b8e"
            else:
                bg_c, fg_c, hover_c = "#2a2a3e", "#9898c8", "#3a3a5e"

            btn = tk.Button(
                cell,
                text=str(ch),
                font=("Segoe UI", 12, "bold" if read else "normal"),
                width=4, height=2,
                bg=bg_c, fg=fg_c,
                activebackground=hover_c,
                activeforeground="#e8e8ff",
                relief="flat", cursor="hand2",
                command=lambda c=ch: self._open_chapter(c)
            )
            btn.pack(fill="both", expand=True)

            # Marca com check se lido
            if read:
                btn.configure(text=f"✓{ch}")

        for col in range(COLS):
            self._grid_frame.columnconfigure(col, weight=1)

        pct = int(read_count / max(self._total_chapters, 1) * 100)
        self._progress_lbl.configure(
            text=f"{read_count} / {self._total_chapters} capítulos lidos  ({pct}%)"
        )
        self._bar_fill.place(relwidth=min(pct/100, 1), relheight=1)

    def _open_chapter(self, chapter: int):
        self.navigate_to("verses",
            book_name=self._book_name,
            chapter=chapter,
            total_chapters=self._total_chapters)

    def refresh(self):
        self._build_grid()