# filepath: ui/game_card.py
"""
Карточка игры — Pixar 2026 стиль.
Рекурсивный hover, плавное свечение границы, мягкая подсветка.
"""

import customtkinter as ctk
from ui.theme import *


def _bind_recursive(widget, event, callback):
    """Привязать событие ко всем вложенным виджетам рекурсивно."""
    try:
        widget.bind(event, callback)
    except Exception:
        pass
    for child in widget.winfo_children():
        _bind_recursive(child, event, callback)


class GameCard(ctk.CTkFrame):
    """
    Карточка игры.
    • Hover: подсветка рамки + смена фона
    • Click: вызов on_click(game)
    • refresh_badge() обновляет счётчик применённых оптимизаций
    """

    def __init__(self, master, game: dict, on_click=None, **kwargs):
        super().__init__(
            master,
            fg_color=BG_CARD,
            corner_radius=RADIUS_LARGE,
            border_width=1,
            border_color=BORDER,
            width=CARD_W,
            height=CARD_H,
            **kwargs,
        )
        self.game     = game
        self.on_click = on_click
        self._color   = game.get("color", TEAL)

        self.grid_propagate(False)
        self.pack_propagate(False)

        self._build()
        self.after(20, self._setup_hover)

    # ── Build ─────────────────────────────────────────────

    def _build(self):
        # Цветная полоска вверху
        ctk.CTkFrame(
            self, fg_color=self._color, height=4, corner_radius=0
        ).pack(fill="x")

        # Emoji
        ctk.CTkLabel(
            self,
            text=self.game.get("emoji", "🎮"),
            font=("Segoe UI Emoji", 40),
        ).pack(pady=(14, 2))

        # Название
        ctk.CTkLabel(
            self,
            text=self.game.get("name", ""),
            font=FONT_BODY_BOLD,
            text_color=WHITE,
            wraplength=CARD_W - 16,
        ).pack(padx=8)

        # Слоган
        ctk.CTkLabel(
            self,
            text=self.game.get("description", ""),
            font=FONT_TINY,
            text_color=WHITE_FADED,
            wraplength=CARD_W - 16,
        ).pack(padx=8, pady=(2, 8))

        # Бейдж с количеством оптимизаций
        count = len(self.game.get("optimizations", []))
        self._badge = ctk.CTkFrame(
            self,
            fg_color=self._color + "22",
            corner_radius=RADIUS_SMALL,
            border_width=1,
            border_color=self._color + "55",
        )
        self._badge.pack(padx=14, pady=(0, 14))
        self._badge_lbl = ctk.CTkLabel(
            self._badge,
            text=f"⚡ {count} оптимизаций",
            font=FONT_TINY,
            text_color=self._color,
        )
        self._badge_lbl.pack(padx=8, pady=3)

    # ── Hover ─────────────────────────────────────────────

    def _setup_hover(self):
        _bind_recursive(self, "<Enter>",    self._on_enter)
        _bind_recursive(self, "<Leave>",    self._on_leave)
        _bind_recursive(self, "<Button-1>", self._on_click)

    def _on_enter(self, _=None):
        self.configure(border_color=self._color, fg_color=BG_CARD_HOV)

    def _on_leave(self, _=None):
        self.configure(border_color=BORDER, fg_color=BG_CARD)

    def _on_click(self, _=None):
        if self.on_click:
            self.on_click(self.game)

    # ── Public ────────────────────────────────────────────

    def refresh_badge(self, applied: int):
        """Обновить счётчик применённых оптимизаций."""
        total = len(self.game.get("optimizations", []))
        if applied:
            self._badge_lbl.configure(
                text=f"✅ {applied}/{total} применено",
                text_color=SUCCESS,
            )
            self._badge.configure(
                fg_color=SUCCESS + "22",
                border_color=SUCCESS + "55",
            )
        else:
            self._badge_lbl.configure(
                text=f"⚡ {total} оптимизаций",
                text_color=self._color,
            )
            self._badge.configure(
                fg_color=self._color + "22",
                border_color=self._color + "55",
            )
