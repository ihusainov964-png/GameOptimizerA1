# filepath: ui/app.py
"""
Главное окно GameOptimizer AI  —  Pixar 2026 «я краснею» стиль.
"""

import threading
import customtkinter as ctk

from ui.theme import *
from ui.game_card   import GameCard
from ui.ai_friend   import AIFriendPanel
from ui.widgets     import PixarButton, Divider
from core.ai_friend import AIFriend
from core.pc_detector import get_pc_info
from data.games_data  import GAMES_DATA
import utils.settings as settings

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# ═══════════════════════════════════════════════════════════
#  SPLASH SCREEN
# ═══════════════════════════════════════════════════════════

class SplashScreen(ctk.CTkToplevel):
    """Красивый экран загрузки при старте."""

    def __init__(self, parent, on_done):
        super().__init__(parent)
        self._on_done  = on_done
        self._step     = 0
        self._steps    = [
            "Просыпаюсь... ☀️",
            "Знакомлюсь с твоим железом 💻",
            "Читаю базу оптимизаций 📚",
            "Готовлю Pixar-магию ✨",
            "Почти готово! 💕",
        ]

        self.overrideredirect(True)          # без рамки окна
        self.configure(fg_color=BG_DEEP)
        self.geometry("440x320")
        self._center()
        self.lift()
        self.grab_set()

        self._build()
        self.after(200, self._tick)

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"440x320+{(sw-440)//2}+{(sh-320)//2}")

    def _build(self):
        # Внешняя рамка цвета TEAL
        border = ctk.CTkFrame(self, fg_color=TEAL, corner_radius=RADIUS_LARGE)
        border.pack(fill="both", expand=True, padx=0, pady=0)

        # Внутренний тёмный фрейм с отступом 2px
        inner = ctk.CTkFrame(border, fg_color=BG_DEEP, corner_radius=RADIUS_LARGE - 2)
        inner.pack(fill="both", expand=True, padx=2, pady=2)

        # Спейсер сверху
        ctk.CTkLabel(inner, text="", height=30).pack()

        # Иконка
        ctk.CTkLabel(
            inner, text="🌟",
            font=("Segoe UI Emoji", 56),
        ).pack()

        # Название
        ctk.CTkLabel(
            inner, text="GameOptimizer AI",
            font=("Segoe UI", 22, "bold"),
            text_color=TEAL,
        ).pack(pady=(8, 2))

        # Подпись
        ctk.CTkLabel(
            inner, text="Твой Pixar-друг для максимального FPS 💕",
            font=FONT_SMALL,
            text_color=WHITE_FADED,
        ).pack(pady=(0, 16))

        # Прогресс-бар
        self._bar = ctk.CTkProgressBar(
            inner,
            progress_color=TEAL,
            fg_color=BORDER,
            corner_radius=RADIUS_ROUND,
            height=6,
            width=320,
        )
        self._bar.pack(pady=(0, 8))
        self._bar.set(0)

        # Статус
        self._msg = ctk.CTkLabel(
            inner, text="Запускаю...",
            font=FONT_TINY,
            text_color=WHITE_FADED,
        )
        self._msg.pack()

    def _tick(self):
        if self._step >= len(self._steps):
            self.grab_release()
            self.destroy()
            self._on_done()
            return
        pct = (self._step + 1) / len(self._steps)
        self._bar.set(pct)
        self._msg.configure(text=self._steps[self._step])
        self._step += 1
        self.after(380, self._tick)


# ═══════════════════════════════════════════════════════════
#  WELCOME DIALOG
# ═══════════════════════════════════════════════════════════

class WelcomeDialog(ctk.CTkToplevel):
    """Диалог первого знакомства."""

    def __init__(self, parent, on_name_set):
        super().__init__(parent)
        self._on_name_set = on_name_set

        self.title("Привет! 💕")
        self.geometry("480x390")
        self.configure(fg_color=BG_MAIN)
        self.resizable(False, False)
        self.grab_set()
        self.after(10, self._center)
        self._build()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"480x390+{(sw-480)//2}+{(sh-390)//2}")

    def _build(self):
        # Pink accent top bar
        ctk.CTkFrame(self, fg_color=PINK, height=3, corner_radius=0).pack(fill="x")

        ctk.CTkLabel(self, text="🌟",
                     font=("Segoe UI Emoji", 54)).pack(pady=(28, 0))

        ctk.CTkLabel(self, text="GameOptimizer AI",
                     font=("Segoe UI", 20, "bold"),
                     text_color=TEAL).pack(pady=(6, 0))

        ctk.CTkLabel(
            self,
            text="Привет! Я Лuma — твой личный игровой друг 💕\n"
                 "Давай познакомимся — как тебя зовут?",
            font=FONT_BODY,
            text_color=WHITE_DIM,
            justify="center",
        ).pack(pady=(10, 18))

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
            width=260, height=44,
            justify="center",
        )
        entry.pack()
        entry.bind("<Return>", self._confirm)
        entry.focus_set()

        PixarButton(
            self, text="✨ Начнём! ✨",
            style="primary",
            command=self._confirm,
            width=180, height=44,
        ).pack(pady=18)

        ctk.CTkLabel(
            self,
            text="Мне не терпится помочь тебе получить больше FPS! 🚀",
            font=FONT_TINY,
            text_color=WHITE_FADED,
        ).pack()

    def _confirm(self, _=None):
        name = self._var.get().strip() or "Друг"
        settings.set_val("user_name", name)
        self._on_name_set(name)
        self.destroy()


# ═══════════════════════════════════════════════════════════
#  MAIN APP
# ═══════════════════════════════════════════════════════════

class MainApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("GameOptimizer AI ✨")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.configure(fg_color=BG_DEEP)
        self.minsize(1000, 600)
        self.after(10, self._center)

        self.user_name  = settings.get("user_name", "")
        self.ai         = AIFriend(self.user_name or "друг")
        self.pc         = None
        self._cards: dict[str, GameCard] = {}   # game_id → card

        # Hide main window behind splash
        self.withdraw()
        SplashScreen(self, self._after_splash)

    # ── Window helpers ────────────────────────────────────

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{WINDOW_W}x{WINDOW_H}+{(sw-WINDOW_W)//2}+{(sh-WINDOW_H)//2}")

    def _after_splash(self):
        """Вызывается когда сплэш закрыт."""
        self.deiconify()
        self._build()
        threading.Thread(target=self._load_pc, daemon=True).start()
        if not self.user_name:
            self.after(300, self._show_welcome)
        else:
            self.ai.set_name(self.user_name)
            self.after(600, lambda: self._ai_panel.notify(self.ai.get_greeting()))

    # ── Build UI ──────────────────────────────────────────

    def _build(self):
        self._build_navbar()

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True)

        self._games_panel = ctk.CTkScrollableFrame(
            body, fg_color=BG_MAIN, corner_radius=0)
        self._games_panel.pack(side="left", fill="both", expand=True)

        self._ai_panel = AIFriendPanel(body, self.ai)
        self._ai_panel.pack(side="right", fill="y")

        self._build_games_grid()

    def _build_navbar(self):
        nav = ctk.CTkFrame(self, fg_color=BG_PANEL, height=62, corner_radius=0)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        ctk.CTkFrame(nav, fg_color=TEAL, height=2, corner_radius=0).pack(fill="x", side="top")

        inner = ctk.CTkFrame(nav, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20)

        # Logo
        logo = ctk.CTkFrame(inner, fg_color="transparent")
        logo.pack(side="left", pady=8)
        ctk.CTkLabel(logo, text="🎮",
                     font=("Segoe UI Emoji", 26)).pack(side="left")
        ctk.CTkLabel(logo, text="GameOptimizer AI",
                     font=FONT_SUBTITLE, text_color=TEAL).pack(side="left", padx=8)

        # Right side
        right = ctk.CTkFrame(inner, fg_color="transparent")
        right.pack(side="right", pady=8)

        self._user_label = ctk.CTkLabel(
            right,
            text=f"Привет, {self.user_name}! 💕" if self.user_name else "💕",
            font=FONT_BODY,
            text_color=PINK_SOFT,
        )
        self._user_label.pack(side="right", padx=10)

        self._pc_btn = ctk.CTkButton(
            right,
            text="💻 Мой ПК",
            fg_color="transparent",
            hover_color=BG_CARD_HOV,
            text_color=WHITE_DIM,
            border_width=1,
            border_color=BORDER_GLOW,
            corner_radius=RADIUS_SMALL,
            font=FONT_SMALL,
            width=96,
            command=self._show_pc_info,
        )
        self._pc_btn.pack(side="right", padx=5)

    def _build_games_grid(self):
        header = ctk.CTkFrame(self._games_panel, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 6))

        ctk.CTkLabel(header, text="🎮 Выбери игру",
                     font=FONT_TITLE, text_color=WHITE).pack(side="left")
        ctk.CTkLabel(header, text=f"{len(GAMES_DATA)} игр",
                     font=FONT_SMALL, text_color=WHITE_FADED).pack(side="left", padx=10)

        grid = ctk.CTkFrame(self._games_panel, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=16, pady=8)

        COLS = 4
        for i, game in enumerate(GAMES_DATA):
            row, col = divmod(i, COLS)
            card = GameCard(grid, game=game, on_click=self._open_game)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            grid.grid_columnconfigure(col, weight=1)
            self._cards[game["id"]] = card

        # Padding row
        ctk.CTkLabel(self._games_panel, text="", height=20).pack()

    # ── Actions ───────────────────────────────────────────

    def _open_game(self, game: dict):
        from ui.game_window import GameWindow
        win = GameWindow(self, game, user_name=self.user_name,
                         on_applied=self._on_optimization_applied)
        win.focus()
        self.after(300, lambda: self._ai_panel.notify(
            f"О, {game['name']}! {game.get('emoji','')} Отличный выбор, "
            f"{self.user_name or 'друг'}! Давай настроим всё по максимуму 🚀"
        ))

    def _on_optimization_applied(self, game_id: str):
        """Обновить бейдж карточки после применения оптимизации."""
        card = self._cards.get(game_id)
        if card:
            applied = len(settings.get_applied_optimizations(game_id))
            card.refresh_badge(applied)

    def _show_welcome(self):
        WelcomeDialog(self, self._on_name_set)

    def _on_name_set(self, name: str):
        self.user_name = name
        self.ai.set_name(name)
        self._user_label.configure(text=f"Привет, {name}! 💕")
        self.after(200, lambda: self._ai_panel.notify(
            f"Привет, {name}! 🎉 Я так рада познакомиться с тобой!\n"
            "Нажми на любую игру — и мы начнём! ✨"
        ))

    def _show_pc_info(self):
        if not self.pc:
            return

        win = ctk.CTkToplevel(self)
        win.title("💻 Твой ПК")
        win.geometry("400x330")
        win.configure(fg_color=BG_MAIN)
        win.resizable(False, False)
        win.grab_set()
        win.after(5, lambda: win.geometry(
            f"400x330+{(win.winfo_screenwidth()-400)//2}+"
            f"{(win.winfo_screenheight()-330)//2}"
        ))

        ctk.CTkFrame(win, fg_color=TEAL, height=3, corner_radius=0).pack(fill="x")
        ctk.CTkLabel(win, text="💻 Твоё железо",
                     font=FONT_TITLE, text_color=TEAL).pack(pady=(20, 12))

        tier_col  = {"low": WARNING, "mid": TEAL, "high": SUCCESS}.get(self.pc.tier, TEAL)
        tier_name = {"low": "Начальный 🐣", "mid": "Средний 🚀", "high": "Высокий 🔥"}.get(
            self.pc.tier, "Средний")

        card = ctk.CTkFrame(win, fg_color=BG_CARD, corner_radius=RADIUS_LARGE)
        card.pack(fill="x", padx=24)

        rows = [
            ("🖥  CPU",  self.pc.cpu_name[:38]),
            ("💾  RAM",  f"{self.pc.ram_gb} GB"),
            ("🎮  GPU",  self.pc.gpu_name[:38]),
            ("📊  VRAM", f"{self.pc.gpu_vram_gb} GB"),
            ("⚡  Тир",  tier_name),
        ]
        for label, value in rows:
            r = ctk.CTkFrame(card, fg_color="transparent")
            r.pack(fill="x", padx=16, pady=3)
            ctk.CTkLabel(r, text=label, font=FONT_SMALL,
                         text_color=WHITE_FADED, width=72, anchor="w").pack(side="left")
            ctk.CTkLabel(r, text=value,
                         font=FONT_BODY_BOLD if "Тир" in label else FONT_SMALL,
                         text_color=tier_col if "Тир" in label else WHITE,
                         anchor="w").pack(side="left", padx=6)

        ctk.CTkLabel(win,
                     text="💕 Оценки FPS подобраны специально под твоё железо!",
                     font=FONT_TINY, text_color=WHITE_FADED).pack(pady=14)

        PixarButton(win, text="Отлично!", style="primary",
                    command=win.destroy, width=120).pack()

    def _load_pc(self):
        self.pc = get_pc_info()
        tier_label = {"low": "Начальный", "mid": "Средний", "high": "Высокий"}.get(
            self.pc.tier, "ПК")
        self.after(0, lambda: self._pc_btn.configure(
            text=f"💻 {tier_label} тир"
        ))
