"""
Tela inicial — 66 livros com filtro AT/NT funcionando corretamente.
Design moderno com cards coloridos.
"""

import tkinter as tk
from tkinter import ttk
from src.database.db import get_books, get_book_progress

BG       = "#1e1e2e"
BG2      = "#252538"
BG_ENTRY = "#2a2a3e"

# Cards do Antigo Testamento — tons de roxo/índigo
AT_CARDS = [
    "#2d1b4e", "#261a45", "#2a1e50", "#231742", "#2f1d52",
    "#261c48", "#2d1f4a", "#22163e", "#301e54", "#281b46",
]
AT_TAG_BG = "#87d9dd"
AT_TAG_FG = "#000000"

# Cards do Novo Testamento — tons de verde esmeralda/teal
NT_CARDS = [
    "#0f3a2a", "#0e3527", "#10382a", "#0d3326", "#103a2c",
    "#0f3628", "#113b2b", "#0d3224", "#103a2d", "#0e3426",
]
NT_TAG_BG = "#79ea79"
NT_TAG_FG = "#000000"

# Cores dos botões de filtro — ajuste aqui à vontade
FILTER_CORES = {
    "Todos": {
        "bg_ativo":   "#e0ae8d",
        "fg_ativo":   "#000000",
        "bg_inativo": "#1e1e2e",
        "fg_inativo": "#e0ae8d",
    },
    "AT": {
        "bg_ativo":   "#87d9dd",
        "fg_ativo":   "#000000",
        "bg_inativo": "#1e1e2e",
        "fg_inativo": "#87d9dd",
    },
    "NT": {
        "bg_ativo":   "#79ea79",
        "fg_ativo":   "#000000",
        "bg_inativo": "#1e1e2e",
        "fg_inativo": "#79ea79",
    },
}


class HomeScreen(tk.Frame):
    def __init__(self, parent, theme, navigate_to, **kwargs):
        kwargs.pop("bg", None)
        super().__init__(parent, bg=BG, **kwargs)
        self.theme = theme
        self.navigate_to = navigate_to
        self._all_books = []
        self._filter = "Todos"
        self._placeholder_active = True
        self._build()
        self._load_books()

    def _build(self):
        # ── Título ───────────────────────────────────────────────────────────
        title_row = tk.Frame(self, bg=BG)
        title_row.pack(fill="x", padx=22, pady=(16, 6))
        tk.Label(title_row, text="Livros da Bíblia",
                 font=("Segoe UI", 22, "bold"), bg=BG, fg="#e2e2ff").pack(side="left")
        self._count_lbl = tk.Label(title_row, text="",
                 font=("Segoe UI", 14, "bold"), bg=BG, fg="#BE4141")
        self._count_lbl.pack(side="left", padx=12)

        # ── Busca ────────────────────────────────────────────────────────────
        search_wrap = tk.Frame(self, bg="#2a2a3e",
                               highlightthickness=1, highlightbackground="#3a3a5e")
        search_wrap.pack(fill="x", padx=22, pady=(0, 10), ipady=1)

        tk.Label(search_wrap, text="🔍", font=("Segoe UI", 13, "bold"),
                 bg=BG_ENTRY, fg="#3cd2c8").pack(side="left", padx=(10, 4))

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._safe_render())

        self._entry = tk.Entry(search_wrap, textvariable=self._search_var,
                               font=("Segoe UI", 13), relief="flat",
                               bg=BG_ENTRY, fg="#c8c8ff",
                               insertbackground="#a78bfa",
                               disabledforeground="#5c5c8a")
        self._entry.pack(side="left", fill="x", expand=True, ipady=7)
        self._entry.insert(0, "Buscar livro...")
        self._entry.bind("<FocusIn>",  self._clear_ph)
        self._entry.bind("<FocusOut>", self._restore_ph)

        # ── Filtros ───────────────────────────────────────────────────────────
        frow = tk.Frame(self, bg=BG)
        frow.pack(fill="x", padx=22, pady=(0, 12))

        self._filter_btns: dict[str, tk.Button] = {}
        labels = {
            "Todos": "Todos os livros",
            "AT":    "Antigo Testamento",
            "NT":    "Novo Testamento",
        }
        for key, label in labels.items():
            b = tk.Button(frow, text=label,
                          font=("Segoe UI", 12, "bold"),
                          relief="flat", cursor="hand2",
                          padx=16, pady=7,
                          command=lambda k=key: self._set_filter(k))
            b.pack(side="left", padx=(0, 8))
            self._filter_btns[key] = b

        self._refresh_filter_btns()

        # ── Lista scrollable ──────────────────────────────────────────────────
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True, padx=22, pady=(0, 12))

        self._canvas = tk.Canvas(wrap, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._lf = tk.Frame(self._canvas, bg=BG)
        self._win = self._canvas.create_window((0,0), window=self._lf, anchor="nw")

        self._lf.bind("<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>",
            lambda e: self._canvas.itemconfig(self._win, width=e.width))

    # ── Dados ─────────────────────────────────────────────────────────────────

    def _load_books(self):
        self._all_books = get_books()
        self._render()

    def _safe_render(self):
        if hasattr(self, "_lf"):
            self._render()

    def _render(self):
        for w in self._lf.winfo_children():
            w.destroy()

        # 1) Filtra por testamento
        filt = self._filter
        if filt == "AT":
            books = [b for b in self._all_books if b[2] == "AT"]
        elif filt == "NT":
            books = [b for b in self._all_books if b[2] == "NT"]
        else:
            books = list(self._all_books)

        # 2) Filtra por busca
        if not self._placeholder_active:
            q = self._search_var.get().strip().lower()
            if q:
                books = [b for b in books if q in b[1].lower()]

        self._count_lbl.configure(text=f"{len(books)} livro{'s' if len(books)!=1 else ''}")

        for idx, (book_id, name, testament, chapters) in enumerate(books):
            prog = get_book_progress(name, chapters)
            pct  = int(prog["read"] / max(prog["total"], 1) * 100)
            done = prog["read"] == prog["total"] and prog["total"] > 0

            if testament == "AT":
                card_bg = AT_CARDS[idx % len(AT_CARDS)]
                tag_bg  = AT_TAG_BG
                tag_fg  = AT_TAG_FG
                arrow_c = AT_TAG_BG
            else:
                card_bg = NT_CARDS[idx % len(NT_CARDS)]
                tag_bg  = NT_TAG_BG
                tag_fg  = NT_TAG_FG
                arrow_c = NT_TAG_BG

            hover_bg = self._lighten(card_bg, 18)

            outer = tk.Frame(self._lf, bg=BG, pady=3)
            outer.pack(fill="x")

            card = tk.Frame(outer, bg=card_bg, cursor="hand2")
            card.pack(fill="x", ipady=10, ipadx=16)

            row1 = tk.Frame(card, bg=card_bg)
            row1.pack(fill="x")

            tag_lbl = tk.Label(row1, text=f" {testament} ",
                font=("Segoe UI", 8, "bold"), bg=tag_bg, fg=tag_fg, padx=4)
            tag_lbl.pack(side="left", padx=(0, 10))

            name_lbl = tk.Label(row1, text=name,
                font=("Segoe UI", 14, "bold"), bg=card_bg, fg="#eeeeff", anchor="w")
            name_lbl.pack(side="left", fill="x", expand=True)

            if done:
                tk.Label(row1, text="✅", font=("Segoe UI", 12),
                         bg=card_bg).pack(side="right", padx=6)

            arrow = tk.Label(row1, text="›",
                font=("Segoe UI", 22, "bold"), bg=card_bg, fg=arrow_c)
            arrow.pack(side="right", padx=6)

            row2 = tk.Frame(card, bg=card_bg)
            row2.pack(fill="x", pady=(4, 0))
            info_lbl = tk.Label(row2,
                text=f"{chapters} capítulos  •  {pct}% lido",
                font=("Segoe UI", 10), bg=card_bg, fg="#8888bb")
            info_lbl.pack(side="left")

            bar_outer = tk.Frame(card, bg="#2a2a4a", height=5)
            bar_outer.pack(fill="x", pady=(6, 0))
            bar_outer.pack_propagate(False)
            if pct > 0:
                bar_in = tk.Frame(bar_outer, bg=tag_bg, height=5)
                bar_in.place(relwidth=pct/100, relheight=1)

            bd = (book_id, name, testament, chapters)
            clickable = [card, row1, row2, name_lbl, tag_lbl, arrow, info_lbl, bar_outer]
            for w in clickable:
                w.bind("<Button-1>", lambda e, b=bd: self._open(b))

            hover_targets = [card, row1, row2, name_lbl, arrow, info_lbl]
            def _on_enter(e, ht=hover_targets, hbg=hover_bg):
                for w in ht:
                    try: w.configure(bg=hbg)
                    except: pass
            def _on_leave(e, ht=hover_targets, cbg=card_bg):
                for w in ht:
                    try: w.configure(bg=cbg)
                    except: pass
            for w in [card, row1, name_lbl]:
                w.bind("<Enter>", _on_enter)
                w.bind("<Leave>", _on_leave)

        self._canvas.yview_moveto(0)

    def _open(self, bd):
        _, name, _, chapters = bd
        self.navigate_to("chapters", book_name=name, total_chapters=chapters)

    # ── Filtro ────────────────────────────────────────────────────────────────

    def _set_filter(self, key: str):
        self._filter = key
        self._refresh_filter_btns()
        self._render()

    def _refresh_filter_btns(self):
        for key, btn in self._filter_btns.items():
            c = FILTER_CORES[key]
            if key == self._filter:
                btn.configure(bg=c["bg_ativo"], fg=c["fg_ativo"])
            else:
                btn.configure(bg=c["bg_inativo"], fg=c["fg_inativo"])

    # ── Busca ─────────────────────────────────────────────────────────────────

    def _clear_ph(self, e):
        if self._placeholder_active:
            self._entry.delete(0, "end")
            self._entry.configure(fg="#c8c8ff")
            self._placeholder_active = False

    def _restore_ph(self, e):
        if not self._search_var.get():
            self._entry.insert(0, "Buscar livro...")
            self._entry.configure(fg="#5c5c8a")
            self._placeholder_active = True
            self._render()

    # ── Utilidades ────────────────────────────────────────────────────────────

    def _lighten(self, hex_c: str, amt: int = 20) -> str:
        try:
            h = hex_c.lstrip("#")
            r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
            return f"#{min(255,r+amt):02x}{min(255,g+amt):02x}{min(255,b+amt):02x}"
        except:
            return hex_c

    def refresh(self):
        self._load_books()