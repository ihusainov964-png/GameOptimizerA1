# filepath: ui/widgets.py
"""
Кастомные Pixar-стиль виджеты для GameOptimizer AI.
"""

import customtkinter as ctk
from ui.theme import *


class PixarButton(ctk.CTkButton):
    """Кнопка в стиле Pixar — тёплая, округлая, с мягким свечением."""

    def __init__(self, master, text="", style="primary", **kwargs):
        colors = {
            "primary":  (TEAL,       TEAL_BRIGHT,    "#0D0F1A", "#0D0F1A"),
            "secondary":(BG_CARD_HOV,BORDER_GLOW,    WHITE_DIM, WHITE),
            "orange":   (ORANGE,     ORANGE_WARM,    "#0D0F1A", "#0D0F1A"),
            "pink":     (PINK,       PINK_SOFT,      "#0D0F1A", "#0D0F1A"),
            "danger":   (ERROR,      "#FF8888",       "#0D0F1A", "#0D0F1A"),
            "success":  (SUCCESS,    "#7EFFF6",       "#0D0F1A", "#0D0F1A"),
        }

        fg, hov, txt_fg, txt_hov = colors.get(style, colors["primary"])

        super().__init__(
            master,
            text=text,
            fg_color=fg,
            hover_color=hov,
            text_color=txt_fg,
            corner_radius=RADIUS_MEDIUM,
            font=FONT_BODY_BOLD,
            **kwargs,
        )


class PixarCard(ctk.CTkFrame):
    """Карточка в стиле Pixar — тёмная с мягкой границей."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=BG_CARD,
            corner_radius=RADIUS_LARGE,
            border_width=1,
            border_color=BORDER,
            **kwargs,
        )


class GlowLabel(ctk.CTkLabel):
    """Заголовок с акцентным цветом."""

    def __init__(self, master, text="", color=TEAL, size=16, bold=True, **kwargs):
        weight = "bold" if bold else "normal"
        super().__init__(
            master,
            text=text,
            text_color=color,
            font=("Segoe UI", size, weight),
            **kwargs,
        )


class SectionHeader(ctk.CTkLabel):
    """Заголовок секции."""

    def __init__(self, master, text="", **kwargs):
        super().__init__(
            master,
            text=text,
            text_color=WHITE,
            font=FONT_SUBTITLE,
            **kwargs,
        )


class StatusBadge(ctk.CTkLabel):
    """Маленький бейдж статуса."""

    def __init__(self, master, text="", status="info", **kwargs):
        colors = {
            "success": SUCCESS,
            "warning": WARNING,
            "error":   ERROR,
            "info":    TEAL,
        }
        color = colors.get(status, TEAL)

        super().__init__(
            master,
            text=text,
            text_color=color,
            font=FONT_SMALL,
            **kwargs,
        )


class FPSBadge(ctk.CTkFrame):
    """Бейдж с ожидаемым приростом FPS."""

    def __init__(self, master, fps_text="+10 FPS", **kwargs):
        super().__init__(
            master,
            fg_color=ORANGE + "30",
            corner_radius=RADIUS_SMALL,
            border_width=1,
            border_color=ORANGE,
            **kwargs,
        )
        self.label = ctk.CTkLabel(
            self,
            text=fps_text,
            text_color=ORANGE_WARM,
            font=FONT_SMALL,
        )
        self.label.pack(padx=8, pady=2)

    def update_text(self, text: str):
        self.label.configure(text=text)


class SafeBadge(ctk.CTkFrame):
    """Бейдж «Безопасно для античита»."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=SUCCESS + "20",
            corner_radius=RADIUS_SMALL,
            border_width=1,
            border_color=SUCCESS,
            **kwargs,
        )
        ctk.CTkLabel(
            self,
            text="🛡️ Безопасно",
            text_color=SUCCESS,
            font=FONT_TINY,
        ).pack(padx=6, pady=2)


class ChatBubble(ctk.CTkFrame):
    """Пузырь сообщения в чате."""

    def __init__(self, master, text="", is_user=False, **kwargs):
        bg = BG_CARD_HOV if is_user else BG_PANEL
        border = TEAL if is_user else BORDER

        super().__init__(
            master,
            fg_color=bg,
            corner_radius=RADIUS_MEDIUM,
            border_width=1,
            border_color=border,
            **kwargs,
        )

        ctk.CTkLabel(
            self,
            text=text,
            text_color=WHITE if is_user else WHITE_DIM,
            font=FONT_BODY,
            wraplength=280,
            justify="left",
        ).pack(padx=12, pady=8)


class ProgressRing(ctk.CTkProgressBar):
    """Красивый прогресс-бар в стиле Pixar."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            progress_color=TEAL,
            fg_color=BORDER,
            corner_radius=RADIUS_ROUND,
            height=8,
            **kwargs,
        )
        self.set(0)


class Divider(ctk.CTkFrame):
    """Горизонтальный разделитель."""

    def __init__(self, master, color=BORDER, **kwargs):
        super().__init__(
            master,
            fg_color=color,
            height=1,
            corner_radius=0,
            **kwargs,
        )
