# filepath: ui/game_card.py
"""
Карточка игры на главном экране — Pixar 2026 стиль.
"""

import customtkinter as ctk
from ui.theme import *
from ui.widgets import PixarCard, GlowLabel


class GameCard(ctk.CTkFrame):
    """
    Красивая карточка игры с Pixar-стилем.
    При наведении подсвечивается, при клике открывает окно игры.
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

        self.game = game
        self.on_click = on_click
        self.game_color = game.get("color", TEAL)
        self._hovered = False

        self.grid_propagate(False)
        self.pack_propagate(False)

        self._build()
        self._bind_hover()

    def _build(self):
        """Построить визуал карточки."""
        # Цветная полоска сверху
        accent = ctk.CTkFrame(
            self,
            fg_color=self.game_color,
            height=4,
            corner_radius=0,
        )
        accent.pack(fill="x", padx=0, pady=(0, 0))

        # Верхняя часть с иконкой
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=16, pady=(16, 0))

        # Большой emoji
        emoji_label = ctk.CTkLabel(
            top_frame,
            text=self.game.get("emoji", "🎮"),
            font=("Segoe UI Emoji", 42),
            text_color=WHITE,
        )
        emoji_label.pack()

        # Название игры
        name_label = ctk.CTkLabel(
            self,
            text=self.game.get("name", "Игра"),
            font=FONT_BODY_BOLD,
            text_color=WHITE,
            wraplength=CARD_W - 20,
        )
        name_label.pack(padx=8, pady=(8, 2))

        # Описание / слоган
        desc_label = ctk.CTkLabel(
            self,
            text=self.game.get("description", ""),
            font=FONT_TINY,
            text_color=WHITE_FADED,
            wraplength=CARD_W - 20,
        )
        desc_label.pack(padx=8, pady=(0, 8))

        # Количество оптимизаций
        opt_count = len(self.game.get("optimizations", []))
        opt_frame = ctk.CTkFrame(
            self,
            fg_color=self.game_color + "20",
            corner_radius=RADIUS_SMALL,
            border_width=1,
            border_color=self.game_color + "60",
        )
        opt_frame.pack(padx=12, pady=(0, 12))

        ctk.CTkLabel(
            opt_frame,
            text=f"⚡ {opt_count} оптимизаций",
            font=FONT_TINY,
            text_color=self.game_color,
        ).pack(padx=8, pady=3)

        # Сохраняем все дочерние виджеты для hover-эффекта
        self._all_children = [accent, top_frame, emoji_label, name_label, desc_label, opt_frame]

    def _bind_hover(self):
        """Подвязать hover-эффекты."""
        def on_enter(e):
            self._hovered = True
            self.configure(
                border_color=self.game_color,
                fg_color=BG_CARD_HOV,
            )

        def on_leave(e):
            self._hovered = False
            self.configure(
                border_color=BORDER,
                fg_color=BG_CARD,
            )

        def on_click(e):
            if self.on_click:
                self.on_click(self.game)

        # Биндим на сам виджет и все его дочерние элементы
        for widget in [self] + self.winfo_children():
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)

        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)
        self.bind("<Button-1>", on_click)
