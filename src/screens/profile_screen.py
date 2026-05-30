"""
Tela de Perfil - nome do usuário, alternância de tema, estatísticas de leitura.
"""

import tkinter as tk
from tkinter import ttk
from src.database.db import get_profile, save_profile, get_progress_stats


class ProfileScreen(tk.Frame):
    def __init__(self, parent, theme, **kwargs):
        super().__init__(parent, **kwargs)
        self.theme = theme
        self._build()
        theme.subscribe(self._apply_theme)
        self._apply_theme()

    def _build(self):
        # ── Cabeçalho ────────────────────────────────────────────────────────
        self._header = tk.Frame(self)
        self._header.pack(fill="x", padx=20, pady=(20, 10))

        self._title = tk.Label(self._header, text="👤  Meu Perfil", font=("Segoe UI", 16, "bold"))
        self._title.pack(side="left")

        # ── Card de perfil ───────────────────────────────────────────────────
        self._profile_card = tk.Frame(self, relief="flat", bd=1, pady=20)
        self._profile_card.pack(fill="x", padx=20, pady=8)

        # Avatar
        self._avatar = tk.Label(self._profile_card, text="👤", font=("Segoe UI", 36))
        self._avatar.pack(pady=(0, 8))

        # Nome
        name_frame = tk.Frame(self._profile_card)
        name_frame.pack(pady=(0, 4))

        self._name_lbl = tk.Label(name_frame, text="Nome:", font=("Segoe UI", 11))
        self._name_lbl.pack(side="left", padx=(0, 8))

        self._name_var = tk.StringVar()
        self._name_entry = tk.Entry(
            name_frame, textvariable=self._name_var,
            font=("Segoe UI", 12, "bold"), width=20,
            relief="flat", bd=4, justify="center"
        )
        self._name_entry.pack(side="left")

        self._save_btn = tk.Button(
            self._profile_card, text="💾  Salvar nome",
            font=("Segoe UI", 10), relief="flat", cursor="hand2",
            padx=16, pady=6, command=self._save_name
        )
        self._save_btn.pack(pady=(8, 0))

        self._save_msg = tk.Label(self._profile_card, text="", font=("Segoe UI", 9))
        self._save_msg.pack()

        # ── Tema ─────────────────────────────────────────────────────────────
        self._theme_card = tk.Frame(self, relief="flat", bd=1, pady=16)
        self._theme_card.pack(fill="x", padx=20, pady=8)

        theme_title = tk.Label(self._theme_card, text="🎨  Aparência", font=("Segoe UI", 12, "bold"))
        theme_title.pack(pady=(0, 8))
        self._theme_title = theme_title

        theme_row = tk.Frame(self._theme_card)
        theme_row.pack()
        self._theme_row = theme_row

        self._dark_btn = tk.Button(
            theme_row, text="🌙  Escuro",
            font=("Segoe UI", 10), relief="flat", cursor="hand2",
            padx=16, pady=6, command=lambda: self._set_theme("dark")
        )
        self._dark_btn.pack(side="left", padx=6)

        self._light_btn = tk.Button(
            theme_row, text="☀️  Claro",
            font=("Segoe UI", 10), relief="flat", cursor="hand2",
            padx=16, pady=6, command=lambda: self._set_theme("light")
        )
        self._light_btn.pack(side="left", padx=6)

        # ── Progresso geral ──────────────────────────────────────────────────
        self._stats_card = tk.Frame(self, relief="flat", bd=1, pady=16)
        self._stats_card.pack(fill="x", padx=20, pady=8)

        self._stats_title = tk.Label(self._stats_card, text="📊  Progresso de Leitura", font=("Segoe UI", 12, "bold"))
        self._stats_title.pack(pady=(0, 12))

        self._pct_lbl = tk.Label(self._stats_card, text="0%", font=("Segoe UI", 30, "bold"))
        self._pct_lbl.pack()

        self._stats_sub = tk.Label(self._stats_card, text="capítulos lidos", font=("Segoe UI", 10))
        self._stats_sub.pack()

        # Barra de progresso global
        self._bar_bg = tk.Frame(self._stats_card, height=10)
        self._bar_bg.pack(fill="x", padx=30, pady=(10, 0))
        self._bar_fill = tk.Frame(self._bar_bg, height=10)
        self._bar_fill.place(relwidth=0, relheight=1)

        self._counts_lbl = tk.Label(self._stats_card, text="", font=("Segoe UI", 10))
        self._counts_lbl.pack(pady=(6, 0))

        # ── Sobre ────────────────────────────────────────────────────────────
        self._about_card = tk.Frame(self, relief="flat", bd=1, pady=12)
        self._about_card.pack(fill="x", padx=20, pady=8)

        self._about_lbl = tk.Label(
            self._about_card,
            text="📖  Bíblia ACF  •  Almeida Corrigida Fiel\nVersão 1.0  •  Desenvolvido por Carlos Hisaba",
            font=("Segoe UI", 9), justify="center"
        )
        self._about_lbl.pack()

    def refresh(self):
        profile = get_profile()
        self._name_var.set(profile["name"])
        self.theme.set(profile["theme"])

        stats = get_progress_stats()
        self._pct_lbl.configure(text=f"{stats['percent']}%")
        self._stats_sub.configure(text=f"capítulos lidos")
        self._counts_lbl.configure(text=f"{stats['read']} de {stats['total']} capítulos")
        self._bar_fill.place(relwidth=min(stats["percent"] / 100, 1), relheight=1)
        self._apply_theme()

    def _save_name(self):
        name = self._name_var.get().strip()
        if not name:
            name = "Carlos"
        profile = get_profile()
        save_profile(name, profile["theme"])
        self._save_msg.configure(text="✔ Salvo com sucesso!")
        self.after(2000, lambda: self._save_msg.configure(text=""))

    def _set_theme(self, theme_name: str):
        self.theme.set(theme_name)
        profile = get_profile()
        save_profile(profile["name"], theme_name)
        self._apply_theme()

    # ── Tema ─────────────────────────────────────────────────────────────────

    def _apply_theme(self):
        c = self.theme.colors
        t = self.theme.name

        self.configure(bg=c["bg"])
        self._header.configure(bg=c["bg"])
        self._title.configure(bg=c["bg"], fg=c["text_heading"])

        for card in [self._profile_card, self._theme_card, self._stats_card, self._about_card]:
            card.configure(bg=c["bg_card"])

        self._avatar.configure(bg=c["bg_card"])
        self._name_lbl.configure(bg=c["bg_card"], fg=c["text"])
        self._name_entry.configure(bg=c["entry_bg"], fg=c["text_heading"], insertbackground=c["text"])
        self._save_btn.configure(bg=c["accent"], fg=c["button_text"], activebackground=c["accent_hover"])
        self._save_msg.configure(bg=c["bg_card"], fg=c["success"])

        self._theme_title.configure(bg=c["bg_card"], fg=c["text_heading"])
        self._theme_row.configure(bg=c["bg_card"])

        # Destaca o botão do tema ativo
        self._dark_btn.configure(
            bg=c["accent"] if t == "dark" else c["bg_secondary"],
            fg=c["button_text"] if t == "dark" else c["text_muted"]
        )
        self._light_btn.configure(
            bg=c["accent"] if t == "light" else c["bg_secondary"],
            fg=c["button_text"] if t == "light" else c["text_muted"]
        )

        self._stats_title.configure(bg=c["bg_card"], fg=c["text_heading"])
        self._pct_lbl.configure(bg=c["bg_card"], fg=c["accent"])
        self._stats_sub.configure(bg=c["bg_card"], fg=c["text_muted"])
        self._bar_bg.configure(bg=c["border"])
        self._bar_fill.configure(bg=c["progress_bar"])
        self._counts_lbl.configure(bg=c["bg_card"], fg=c["text_muted"])

        self._about_card.configure(bg=c["bg_card"])
        self._about_lbl.configure(bg=c["bg_card"], fg=c["text_muted"])