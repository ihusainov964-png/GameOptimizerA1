# filepath: ui/ai_friend.py
"""
Панель AI-друга — правый сайдбар с чатом.
Pixar-характер: тёплый, заботливый, игривый.
"""

import customtkinter as ctk
from ui.theme import *
from core.ai_friend import AIFriend


class AIFriendPanel(ctk.CTkFrame):
    """Боковая панель чата с AI-другом."""

    def __init__(self, master, ai: AIFriend, **kwargs):
        super().__init__(
            master,
            fg_color=BG_PANEL,
            corner_radius=0,
            border_width=1,
            border_color=BORDER,
            width=280,
            **kwargs,
        )
        self.ai = ai
        self.pack_propagate(False)
        self._build()

    def _build(self):
        # ── Заголовок ──────────────────────────────
        header = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Цветная полоска
        ctk.CTkFrame(header, fg_color=PINK, height=3, corner_radius=0).pack(fill="x", side="top")

        header_inner = ctk.CTkFrame(header, fg_color="transparent")
        header_inner.pack(fill="both", expand=True, padx=12, pady=0)

        # Аватар (эмодзи)
        avatar_frame = ctk.CTkFrame(
            header_inner,
            fg_color=PINK + "30",
            corner_radius=RADIUS_ROUND,
            width=44,
            height=44,
            border_width=2,
            border_color=PINK_DIM,
        )
        avatar_frame.pack(side="left", pady=12)
        avatar_frame.pack_propagate(False)

        ctk.CTkLabel(
            avatar_frame,
            text="🌟",
            font=("Segoe UI Emoji", 22),
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Имя и статус
        name_frame = ctk.CTkFrame(header_inner, fg_color="transparent")
        name_frame.pack(side="left", padx=10, pady=12)

        ctk.CTkLabel(
            name_frame,
            text="Лuma",
            font=FONT_BODY_BOLD,
            text_color=PINK_SOFT,
        ).pack(anchor="w")

        status_row = ctk.CTkFrame(name_frame, fg_color="transparent")
        status_row.pack(anchor="w")

        # Пульсирующий зелёный кружок (статус онлайн)
        ctk.CTkLabel(
            status_row,
            text="●",
            font=("Segoe UI", 8),
            text_color=SUCCESS,
        ).pack(side="left")

        ctk.CTkLabel(
            status_row,
            text=" онлайн",
            font=FONT_TINY,
            text_color=WHITE_FADED,
        ).pack(side="left")

        # ── История чата ───────────────────────────
        self._chat_area = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self._chat_area.pack(fill="both", expand=True, pady=0)

        # ── Поле ввода ─────────────────────────────
        input_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=60)
        input_frame.pack(fill="x", side="bottom")
        input_frame.pack_propagate(False)

        self._input_var = ctk.StringVar()

        self._input = ctk.CTkEntry(
            input_frame,
            textvariable=self._input_var,
            placeholder_text="Напиши что-нибудь... 💬",
            fg_color=BG_INPUT,
            border_color=BORDER_GLOW,
            text_color=WHITE,
            placeholder_text_color=WHITE_FADED,
            corner_radius=RADIUS_MEDIUM,
            font=FONT_BODY,
        )
        self._input.pack(side="left", fill="x", expand=True, padx=(10, 6), pady=10)
        self._input.bind("<Return>", self._send_message)

        send_btn = ctk.CTkButton(
            input_frame,
            text="→",
            fg_color=PINK,
            hover_color=PINK_SOFT,
            text_color="white",
            width=40,
            height=36,
            corner_radius=RADIUS_MEDIUM,
            font=("Segoe UI", 16, "bold"),
            command=self._send_message,
        )
        send_btn.pack(side="right", padx=(0, 10), pady=10)

        # Добавляем приветственное сообщение
        self.add_ai_message(self.ai.get_greeting())

    def add_ai_message(self, text: str):
        """Добавить сообщение от AI."""
        self._add_message(text, is_user=False)

    def add_user_message(self, text: str):
        """Добавить сообщение от пользователя."""
        self._add_message(text, is_user=True)

    def _add_message(self, text: str, is_user: bool):
        """Добавить пузырь сообщения."""
        row = ctk.CTkFrame(self._chat_area, fg_color="transparent")
        row.pack(fill="x", padx=8, pady=3)

        # Выравнивание: пользователь справа, AI слева
        bubble_frame = ctk.CTkFrame(
            row,
            fg_color=BG_CARD_HOV if is_user else BG_CARD,
            corner_radius=RADIUS_MEDIUM,
            border_width=1,
            border_color=(TEAL + "60") if is_user else BORDER,
        )

        if is_user:
            bubble_frame.pack(side="right", padx=(30, 0))
        else:
            bubble_frame.pack(side="left", padx=(0, 30))

        ctk.CTkLabel(
            bubble_frame,
            text=text,
            font=FONT_SMALL,
            text_color=WHITE if is_user else WHITE_DIM,
            wraplength=200,
            justify="left",
        ).pack(padx=10, pady=7)

        # Прокрутить вниз
        self._chat_area.after(50, lambda: self._chat_area._parent_canvas.yview_moveto(1.0))

    def _send_message(self, event=None):
        """Отправить сообщение и получить ответ."""
        msg = self._input_var.get().strip()
        if not msg:
            return

        self._input_var.set("")
        self.add_user_message(msg)

        # Получить ответ от AI
        response = self.ai.get_response(msg)
        self.after(400, lambda: self.add_ai_message(response))

    def notify(self, text: str):
        """Показать уведомление от AI (вызывается извне)."""
        self.add_ai_message(text)
