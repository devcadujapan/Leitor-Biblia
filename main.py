"""
Bíblia ACF - Aplicativo Windows
Python 3.12+ — sem dependências externas.

Execução: python main.py
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from typing import Optional

from src.database.db import init_database, get_profile
from src.context.theme import ThemeManager
from src.screens.home_screen import HomeScreen
from src.screens.chapters_screen import ChaptersScreen
from src.screens.verse_list import VerseList

APP_TITLE  = "Leitura da Bíblia — Almeida Corrigida Fiel"
WIN_W, WIN_H = 1000, 740
MIN_W, MIN_H =  660,  520
BG_HEADER    = "#12122a"
BG_MAIN      = "#1e1e2e"


class BibleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        init_database()

        profile = get_profile()
        self.theme = ThemeManager(profile.get("theme", "dark"))

        self.title(APP_TITLE)
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.minsize(MIN_W, MIN_H)
        self.configure(bg=BG_MAIN)
        self._center()

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Vertical.TScrollbar",
            background="#2a2a3e", troughcolor="#1a1a2e",
            bordercolor="#1a1a2e", arrowcolor="#5c5c8a",
            relief="flat", width=10)
        self.style.map("Vertical.TScrollbar",
            background=[("active", "#3a3a5e")])

        self._nav_stack: list[dict] = []
        self._current: Optional[tk.Frame] = None
        self._active_canvas: Optional[tk.Canvas] = None

        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self._build()
        self._go_home()

    # ── Layout ───────────────────────────────────────────────────────────────

    def _build(self):
        # Cabeçalho
        hdr = tk.Frame(self, bg=BG_HEADER, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        # Ícone decorativo
        tk.Label(hdr, text="✦", font=("Segoe UI", 18),
                 bg=BG_HEADER, fg="#e8ea62").pack(side="left", padx=(18, 6))

        title_col = tk.Frame(hdr, bg=BG_HEADER)
        title_col.pack(side="left")

        self._hdr_title = tk.Label(title_col, text="Leitura da Bíblia",
            font=("Segoe UI", 22, "bold"), bg=BG_HEADER, fg="#2ecfd2")
        self._hdr_title.pack(anchor="w")

        self._hdr_sub = tk.Label(title_col, text="Almeida Corrigida Fiel",
            font=("Segoe UI", 11), bg=BG_HEADER, fg="#c34edb")
        self._hdr_sub.pack(anchor="w")

        # Separador
        tk.Frame(self, bg="#3ba159", height=3).pack(fill="x")

        # Conteúdo
        self._content = tk.Frame(self, bg=BG_MAIN)
        self._content.pack(fill="both", expand=True)

        # Telas
        self._home = HomeScreen(self._content, self.theme,
                                navigate_to=self._nav_to, bg=BG_MAIN)
        self._chaps = ChaptersScreen(self._content, self.theme,
                                     navigate_to=self._nav_to,
                                     navigate_back=self._nav_back, bg=BG_MAIN)
        self._verses = VerseList(self._content, self.theme,
                                 navigate_back=self._nav_back, bg=BG_MAIN)

    # ── Navegação ─────────────────────────────────────────────────────────────

    def _go_home(self):
        self._nav_stack.clear()
        self._home.refresh()
        self._show(self._home)
        self._hdr_title.configure(text="Leitura da Bíblia")
        self._hdr_sub.configure(text="Almeida Corrigida Fiel")

    def _nav_to(self, screen: str, **kw):
        self._nav_stack.append({"screen": screen, "kw": kw})
        if screen == "chapters":
            self._chaps.load(kw["book_name"], kw["total_chapters"])
            self._show(self._chaps)
            self._hdr_title.configure(text=f"📚  {kw['book_name']}")
            self._hdr_sub.configure(text=f"{kw['total_chapters']} capítulos")
        elif screen == "verses":
            self._verses.load(kw["book_name"], kw["chapter"], kw["total_chapters"])
            self._show(self._verses)
            self._hdr_title.configure(text=f"📖  {kw['book_name']}")
            self._hdr_sub.configure(text=f"Capítulo {kw['chapter']} de {kw['total_chapters']}")

    def _nav_back(self):
        if self._nav_stack:
            self._nav_stack.pop()
        if not self._nav_stack:
            self._go_home()
        else:
            prev = self._nav_stack[-1]
            sc, kw = prev["screen"], prev["kw"]
            if sc == "chapters":
                self._chaps.refresh()
                self._show(self._chaps)
                self._hdr_title.configure(text=f"📚  {kw['book_name']}")
                self._hdr_sub.configure(text=f"{kw['total_chapters']} capítulos")

    def _on_mousewheel(self, event):
        if self._active_canvas:
            self._active_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _show(self, frame: tk.Frame):
        if self._current:
            self._current.pack_forget()
        frame.pack(fill="both", expand=True)
        self._current = frame
        # Registra o canvas da tela ativa para o scroll do mouse
        if hasattr(frame, "_canvas"):
            self._active_canvas = frame._canvas
        else:
            self._active_canvas = None

    # ── Utilitário ────────────────────────────────────────────────────────────

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{WIN_W}x{WIN_H}+{(sw-WIN_W)//2}+{(sh-WIN_H)//2}")


if __name__ == "__main__":
    app = BibleApp()
    app.mainloop()