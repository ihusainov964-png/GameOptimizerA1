# filepath: ui/app.py
"""
Главное окно GameOptimizer AI — Pixar 2026 стиль.
Полностью переписан для стабильной работы.
"""

import threading
import customtkinter as ctk

from ui.theme import *
from ui.game_card   import GameCard
from ui.ai_friend   import AIFriendPanel
from ui.widgets     import PixarButton
from core.ai_friend import AIFriend
from core.pc_detector import get_pc_info
from data.games_data  import GAMES_DATA
import utils.settings as settings

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# ═══════════════════════════════════════════════
#  WELCOME DIALOG — первое знакомство
# ═══════════════════════════════════════════════

class WelcomeDialog(ctk.CTkToplevel):

    def __init__(self, parent, on_name_set):
        super().__init__(parent)
        self._on_name_set = on_name_set
        self.title("Привет! 💕")
        self.geometry("460x360")
        self.configure(fg_color=BG_MAIN)
        self.resizable(False, False)
        self.grab_set()
        self.after(50, self._center)
        self._build()

    def _center(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"460x360+{(sw-460)//2}+{(sh-360)//2}")

    def _build(self):
        ctk.CTkFrame(self, fg_color=PINK, height=3,
                     corner_radius=0).pack(fill="x")

        ctk.CTkLabel(self, text="🌟",
                     font=("Segoe UI Emoji", 52)).pack(pady=(24, 0))

        ctk.CTkLabel(self, text="GameOptimizer AI",
                     font=("Segoe UI", 20, "bold"),
                     text_color=TEAL).pack(pady=(6, 0))

        ctk.CTkLabel(self,
                     text="Привет! Я Лuma — твой личный игровой друг 💕\n"
                          "Давай познакомимся — как тебя зовут?",
                     font=FONT_BODY,
                     text_color=WHITE_DIM,
                     justify="center").pack(pady=(10, 16))

        self._var = ctk.StringVar()
        entry = ctk.CTkEntry(
            self,
            textvariable=self._var,
            placeholder_text="Введи своё имя...",
            fg_color=BG_INPUT,
            border_color=TEAL_DIM,
            text_color=WHITE,
            placeholder_text_color=WHITE_FADED,
            corner_radius=RADIUS_MEDIUM,
            font=FONT_BODY,
            width=240, height=42,
            justify="center",
        )
        entry.pack()
        entry.bind("<Return>", self._confirm)
        entry.focus_set()

        PixarButton(self, text="✨ Начнём!",
                    style="primary",
                    command=self._confirm,
                    width=160, height=42).pack(pady=16)

        ctk.CTkLabel(self,
                     text="Мне не терпится помочь тебе получить больше FPS! 🚀",
                     font=FONT_TINY,
                     text_color=WHITE_FADED).pack()

    def _confirm(self, _=None):
        name = self._var.get().strip() or "Друг"
        settings.set_val("user_name", name)
        self._on_name_set(name)
        self.destroy()


# ═══════════════════════════════════════════════
#  MAIN APP
# ═══════════════════════════════════════════════

class MainApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("GameOptimizer AI ✨")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.configure(fg_color=BG_DEEP)
        self.minsize(1000, 600)

        self.user_name = settings.get("user_name", "")
        self.ai        = AIFriend(self.user_name or "друг")
        self.pc        = None
        self._cards: dict = {}

        # Строим UI сразу
        self._build()

        # Загружаем ПК в фоне
        threading.Thread(target=self._load_pc, daemon=True).start()

        # Центрируем окно
        self.after(10, self._center)

        # Welcome если первый запуск
        if not self.user_name:
            self.after(200, self._show_welcome)

    def _center(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = WINDOW_W, WINDOW_H
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    # ── Build ────────────────────────────────────────

    def _build(self):
        self._build_navbar()

        # Тело: игры слева, AI справа
        self._body = ctk.CTkFrame(self, fg_color="transparent")
        self._body.pack(fill="both", expand=True)

        # Область с карточками
        self._games_panel = ctk.CTkScrollableFrame(
            self._body, fg_color=BG_MAIN, corner_radius=0)
        self._games_panel.pack(side="left", fill="both", expand=True)

        # AI-панель
        self._ai_panel = AIFriendPanel(self._body, self.ai)
        self._ai_panel.pack(side="right", fill="y")

        # Наполняем карточками
        self._build_games_grid()

    def _build_navbar(self):
        nav = ctk.CTkFrame(self, fg_color=BG_PANEL,
                           height=62, corner_radius=0)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        # Верхняя цветная линия
        ctk.CTkFrame(nav, fg_color=TEAL,
                     height=2, corner_radius=0).pack(fill="x", side="top")

        row = ctk.CTkFrame(nav, fg_color="transparent")
        row.pack(fill="both", expand=True, padx=20)

        # Логотип
        ctk.CTkLabel(row, text="🎮",
                     font=("Segoe UI Emoji", 24)).pack(side="left", pady=8)
        ctk.CTkLabel(row, text="GameOptimizer AI",
                     font=FONT_SUBTITLE,
                     text_color=TEAL).pack(side="left", padx=8, pady=8)

        # Правая сторона
        self._user_label = ctk.CTkLabel(
            row,
            text=f"Привет, {self.user_name}! 💕" if self.user_name else "💕",
            font=FONT_BODY,
            text_color=PINK_SOFT)
        self._user_label.pack(side="right", padx=10)

        self._pc_btn = ctk.CTkButton(
            row,
            text="💻 Мой ПК",
            fg_color="transparent",
            hover_color=BG_CARD_HOV,
            text_color=WHITE_DIM,
            border_width=1,
            border_color=BORDER_GLOW,
            corner_radius=RADIUS_SMALL,
            font=FONT_SMALL,
            width=96,
            command=self._show_pc_info)
        self._pc_btn.pack(side="right", padx=5)

    def _build_games_grid(self):
        # Заголовок
        hdr = ctk.CTkFrame(self._games_panel, fg_color="transparent")
        hdr.pack(fill="x", padx=24, pady=(20, 8))

        ctk.CTkLabel(hdr, text="🎮 Выбери игру",
                     font=FONT_TITLE,
                     text_color=WHITE).pack(side="left")
        ctk.CTkLabel(hdr, text=f"{len(GAMES_DATA)} игр",
                     font=FONT_SMALL,
                     text_color=WHITE_FADED).pack(side="left", padx=10)

        # Сетка
        grid = ctk.CTkFrame(self._games_panel, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=16, pady=4)

        COLS = 4
        for i, game in enumerate(GAMES_DATA):
            r, c = divmod(i, COLS)
            card = GameCard(grid, game=game, on_click=self._open_game)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            grid.grid_columnconfigure(c, weight=1)
            self._cards[game["id"]] = card

        ctk.CTkLabel(self._games_panel, text="", height=20).pack()

    # ── Actions ──────────────────────────────────────

    def _open_game(self, game: dict):
        from ui.game_window import GameWindow
        win = GameWindow(self, game,
                         user_name=self.user_name,
                         on_applied=self._on_optimization_applied)
        win.focus()
        name = self.user_name or "друг"
        self.after(300, lambda: self._ai_panel.notify(
            f"О, {game['name']}! {game.get('emoji','')} Отличный выбор, "
            f"{name}! Давай настроим всё по максимуму 🚀"))

    def _on_optimization_applied(self, game_id: str):
        card = self._cards.get(game_id)
        if card:
            n = len(settings.get_applied_optimizations(game_id))
            card.refresh_badge(n)

    def _show_welcome(self):
        WelcomeDialog(self, self._on_name_set)

    def _on_name_set(self, name: str):
        self.user_name = name
        self.ai.set_name(name)
        self._user_label.configure(text=f"Привет, {name}! 💕")
        self.after(200, lambda: self._ai_panel.notify(
            f"Привет, {name}! 🎉 Я так рада познакомиться с тобой!\n"
            "Нажми на любую игру — и мы начнём! ✨"))

    def _show_pc_info(self):
        if not self.pc:
            return
        win = ctk.CTkToplevel(self)
        win.title("💻 Твой ПК")
        win.geometry("400x330")
        win.configure(fg_color=BG_MAIN)
        win.resizable(False, False)
        win.grab_set()
        win.after(10, lambda: win.geometry(
            f"400x330+{(win.winfo_screenwidth()-400)//2}+"
            f"{(win.winfo_screenheight()-330)//2}"))

        ctk.CTkFrame(win, fg_color=TEAL, height=3,
                     corner_radius=0).pack(fill="x")
        ctk.CTkLabel(win, text="💻 Твоё железо",
                     font=FONT_TITLE, text_color=TEAL).pack(pady=(18, 10))

        tc = {"low": WARNING, "mid": TEAL, "high": SUCCESS}.get(self.pc.tier, TEAL)
        tn = {"low": "Начальный 🐣", "mid": "Средний 🚀",
              "high": "Высокий 🔥"}.get(self.pc.tier, "Средний")

        card = ctk.CTkFrame(win, fg_color=BG_CARD,
                            corner_radius=RADIUS_LARGE)
        card.pack(fill="x", padx=20)

        for label, value in [
            ("🖥  CPU",  self.pc.cpu_name[:36]),
            ("💾  RAM",  f"{self.pc.ram_gb} GB"),
            ("🎮  GPU",  self.pc.gpu_name[:36]),
            ("📊  VRAM", f"{self.pc.gpu_vram_gb} GB"),
            ("⚡  Тир",  tn),
        ]:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=3)
            ctk.CTkLabel(row, text=label, font=FONT_SMALL,
                         text_color=WHITE_FADED,
                         width=70, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value, font=FONT_SMALL,
                         text_color=tc if "Тир" in label else WHITE,
                         anchor="w").pack(side="left", padx=6)

        ctk.CTkLabel(win,
                     text="💕 Оценки FPS подобраны под твоё железо!",
                     font=FONT_TINY,
                     text_color=WHITE_FADED).pack(pady=12)
        PixarButton(win, text="Отлично!", style="primary",
                    command=win.destroy, width=120).pack()

    def _load_pc(self):
        self.pc = get_pc_info()
        tn = {"low": "Начальный", "mid": "Средний",
              "high": "Высокий"}.get(self.pc.tier, "ПК")
        self.after(0, lambda: self._pc_btn.configure(
            text=f"💻 {tn} тир"))
