"""
Gerenciador de tema - claro / escuro
Centraliza todas as cores do app.
"""


THEMES = {
    "dark": {
        "bg":           "#1a1a2e",
        "bg_secondary": "#16213e",
        "bg_card":      "#0f3460",
        "accent":       "#4A90E2",
        "accent_hover": "#357abd",
        "text":         "#e0e0e0",
        "text_muted":   "#9e9e9e",
        "text_heading": "#ffffff",
        "border":       "#2a2a4a",
        "success":      "#4caf50",
        "tab_active":   "#4A90E2",
        "tab_inactive": "#555577",
        "scrollbar":    "#2a2a4a",
        "entry_bg":     "#0f3460",
        "button_text":  "#ffffff",
        "verse_bg":     "#16213e",
        "verse_num":    "#4A90E2",
        "checkbox_on":  "#4A90E2",
        "progress_bar": "#4A90E2",
    },
    "light": {
        "bg":           "#f5f7fa",
        "bg_secondary": "#ffffff",
        "bg_card":      "#e8f0fe",
        "accent":       "#1a73e8",
        "accent_hover": "#1558b0",
        "text":         "#212121",
        "text_muted":   "#757575",
        "text_heading": "#0d0d0d",
        "border":       "#d0d7de",
        "success":      "#2e7d32",
        "tab_active":   "#1a73e8",
        "tab_inactive": "#9e9e9e",
        "scrollbar":    "#c0c0c0",
        "entry_bg":     "#ffffff",
        "button_text":  "#ffffff",
        "verse_bg":     "#ffffff",
        "verse_num":    "#1a73e8",
        "checkbox_on":  "#1a73e8",
        "progress_bar": "#1a73e8",
    },
}


class ThemeManager:
    def __init__(self, initial: str = "dark"):
        self._theme = initial
        self._listeners: list = []

    @property
    def name(self) -> str:
        return self._theme

    @property
    def colors(self) -> dict:
        return THEMES[self._theme]

    def toggle(self):
        self._theme = "light" if self._theme == "dark" else "dark"
        self._notify()

    def set(self, theme: str):
        if theme in THEMES:
            self._theme = theme
            self._notify()

    def subscribe(self, callback):
        """Registra função a ser chamada quando o tema mudar."""
        self._listeners.append(callback)

    def _notify(self):
        for cb in self._listeners:
            cb()

    def __getitem__(self, key: str):
        return self.colors[key]