# filepath: ui/ai_friend.py
"""
Панель AI-друга Лumы — боковой чат.
"""

import customtkinter as ctk
from ui.theme import *
from core.ai_friend import AIFriend


class AIFriendPanel(ctk.CTkFrame):

    def __init__(self, master, ai: AIFriend, **kwargs):
        super().__init__(
            master,
            fg_color=BG_PANEL,
            corner_radius=0,
            border_width=1,
            border_color=BORDER,
            width=270,
            **kwargs,
        )
        self.ai = ai
        self.pack_propagate(False)
        self._build()

    def _build(self):
        # ── Шапка ──────────────────────────────
        header = ctk.CTkFrame(self, fg_color=BG_CARD,
                              corner_radius=0, height=68)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkFrame(header, fg_color=PINK,
                     height=3, corner_radius=0).pack(fill="x", side="top")

        row = ctk.CTkFrame(header, fg_color="transparent")
        row.pack(fill="both", expand=True, padx=12)

        # Аватар
        av = ctk.CTkFrame(row,
                          fg_color=PINK + "30",
                          corner_radius=22,
                          width=44, height=44,
                          border_width=2,
                          border_color=PINK_DIM)
        av.pack(side="left", pady=10)
        av.pack_propagate(False)
        ctk.CTkLabel(av, text="🌟",
                     font=("Segoe UI Emoji", 20)).place(relx=0.5, rely=0.5,
                                                        anchor="center")

        # Имя + статус
        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", padx=10)
        ctk.CTkLabel(info, text="Лuma",
                     font=FONT_BODY_BOLD,
                     text_color=PINK_SOFT).pack(anchor="w")
        ctk.CTkLabel(info, text="● онлайн",
                     font=FONT_TINY,
                     text_color=SUCCESS).pack(anchor="w")

        # ── Область чата ───────────────────────
        self._chat = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0)
        self._chat.pack(fill="both", expand=True)

        # ── Поле ввода ─────────────────────────
        inp_frame = ctk.CTkFrame(self, fg_color=BG_CARD,
                                 corner_radius=0, height=58)
        inp_frame.pack(fill="x", side="bottom")
        inp_frame.pack_propagate(False)

        self._var = ctk.StringVar()
        self._entry = ctk.CTkEntry(
            inp_frame,
            textvariable=self._var,
            placeholder_text="Напиши что-нибудь... 💬",
            fg_color=BG_INPUT,
            border_color=BORDER_GLOW,
            text_color=WHITE,
            placeholder_text_color=WHITE_FADED,
            corner_radius=RADIUS_MEDIUM,
            font=FONT_SMALL,
        )
        self._entry.pack(side="left", fill="x", expand=True,
                         padx=(8, 4), pady=10)
        self._entry.bind("<Return>", self._send)

        ctk.CTkButton(
            inp_frame,
            text="→",
            fg_color=PINK, hover_color=PINK_SOFT,
            text_color="white",
            width=36, height=34,
            corner_radius=RADIUS_MEDIUM,
            font=("Segoe UI", 15, "bold"),
            command=self._send,
        ).pack(side="right", padx=(0, 8), pady=10)

        # Приветствие
        self.after(100, lambda: self._add_msg(self.ai.get_greeting(), False))

    # ── Сообщения ──────────────────────────────

    def _add_msg(self, text: str, is_user: bool):
        outer = ctk.CTkFrame(self._chat, fg_color="transparent")
        outer.pack(fill="x", padx=6, pady=3)

        bubble = ctk.CTkFrame(
            outer,
            fg_color=BG_CARD_HOV if is_user else BG_CARD,
            corner_radius=RADIUS_MEDIUM,
            border_width=1,
            border_color=(TEAL + "55") if is_user else BORDER,
        )
        if is_user:
            bubble.pack(side="right", padx=(28, 0))
        else:
            bubble.pack(side="left", padx=(0, 28))

        ctk.CTkLabel(
            bubble,
            text=text,
            font=FONT_SMALL,
            text_color=WHITE if is_user else WHITE_DIM,
            wraplength=190,
            justify="left",
        ).pack(padx=10, pady=7)

        # Прокрутить вниз
        self._chat.after(60, lambda: self._chat._parent_canvas.yview_moveto(1.0))

    def _send(self, _=None):
        msg = self._var.get().strip()
        if not msg:
            return
        self._var.set("")
        self._add_msg(msg, True)
        resp = self.ai.get_response(msg)
        self.after(350, lambda: self._add_msg(resp, False))

    def notify(self, text: str):
        """Добавить сообщение от AI (вызывается извне)."""
        self._add_msg(text, False)
