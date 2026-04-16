# filepath: ui/app.py
"""
Главное окно GameOptimizer AI.
Pixar 2026 стиль — тёплый, уютный, «я краснею».
"""

import customtkinter as ctk
import threading
from ui.theme import *
from ui.game_card import GameCard
from ui.ai_friend import AIFriendPanel
from ui.widgets import PixarButton, GlowLabel, Divider
from core.ai_friend import AIFriend
from core.pc_detector import get_pc_info
from data.games_data import GAMES_DATA
import utils.settings as settings


# Настройка customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class WelcomeDialog(ctk.CTkToplevel):
    """Приветственный диалог при первом запуске."""

    def __init__(self, parent, on_name_set):
        super().__init__(parent)
        self.on_name_set = on_name_set

        self.title("Добро пожаловать! 💕")
        self.geometry("480x380")
        self.configure(fg_color=BG_MAIN)
        self.resizable(False, False)
        self.grab_set()

        self._build()

        # Центрировать
        self.after(10, self._center)

    def _center(self):
        self.update_idletasks()
        w, h = 480, 380
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        # Заголовочная иконка
        ctk.CTkLabel(
            self,
            text="🌟",
            font=("Segoe UI Emoji", 60),
        ).pack(pady=(32, 0))

        ctk.CTkLabel(
            self,
            text="GameOptimizer AI",
            font=FONT_TITLE,
            text_color=TEAL,
        ).pack(pady=(8, 0))

        ctk.CTkLabel(
            self,
            text="Привет! Я Лuma — твой личный игровой друг 💕\nДавай познакомимся — как тебя зовут?",
            font=FONT_BODY,
            text_color=WHITE_DIM,
            justify="center",
        ).pack(pady=(12, 20))

        # Поле ввода имени
        self._name_var = ctk.StringVar()
        name_entry = ctk.CTkEntry(
            self,
            textvariable=self._name_var,
            placeholder_text="Введи своё имя...",
            fg_color=BG_INPUT,
            border_color=TEAL_DIM,
            text_color=WHITE,
            placeholder_text_color=WHITE_FADED,
            corner_radius=RADIUS_MEDIUM,
            font=FONT_BODY,
            width=260,
            height=44,
            justify="center",
        )
        name_entry.pack()
        name_entry.bind("<Return>", self._confirm)
        name_entry.focus()

        PixarButton(
            self,
            text="✨ Начнём! ✨",
            style="primary",
            command=self._confirm,
            width=180,
            height=44,
        ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text="Мне не терпится помочь тебе получить больше FPS! 🚀",
            font=FONT_TINY,
            text_color=WHITE_FADED,
        ).pack()

    def _confirm(self, event=None):
        name = self._name_var.get().strip()
        if not name:
            name = "Друг"
        settings.set_val("user_name", name)
        self.on_name_set(name)
        self.destroy()


class MainApp(ctk.CTk):
    """Главное окно приложения."""

    def __init__(self):
        super().__init__()

        self.title("GameOptimizer AI ✨")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.configure(fg_color=BG_DEEP)
        self.minsize(1000, 600)

        # Центрировать
        self.after(10, self._center_window)

        # Данные
        self.user_name = settings.get("user_name", "")
        self.ai = AIFriend(self.user_name or "друг")
        self.pc = None  # загрузим в фоне

        # Построить UI
        self._build()

        # Загрузить ПК в фоне
        threading.Thread(target=self._load_pc, daemon=True).start()

        # Приветствие при первом запуске
        if not self.user_name:
            self.after(200, self._show_welcome)
        else:
            self.ai.set_name(self.user_name)

    def _center_window(self):
        self.update_idletasks()
        w, h = WINDOW_W, WINDOW_H
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        """Построить главный интерфейс."""

        # ── Верхняя навигация ──────────────────────
        self._build_navbar()

        # ── Основная область ───────────────────────
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True)

        # Левая панель игр
        self._games_panel = ctk.CTkScrollableFrame(
            body,
            fg_color=BG_MAIN,
            corner_radius=0,
        )
        self._games_panel.pack(side="left", fill="both", expand=True)

        # Правая панель AI-друга
        self._ai_panel = AIFriendPanel(body, self.ai)
        self._ai_panel.pack(side="right", fill="y")

        # Наполнить игровые карточки
        self._build_games_grid()

    def _build_navbar(self):
        """Построить навигационную панель."""
        nav = ctk.CTkFrame(self, fg_color=BG_PANEL, height=64, corner_radius=0)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        # Цветная полоска сверху
        ctk.CTkFrame(nav, fg_color=TEAL, height=2, corner_radius=0).pack(fill="x", side="top")

        nav_inner = ctk.CTkFrame(nav, fg_color="transparent")
        nav_inner.pack(fill="both", expand=True, padx=20)

        # Логотип
        logo_frame = ctk.CTkFrame(nav_inner, fg_color="transparent")
        logo_frame.pack(side="left", pady=10)

        ctk.CTkLabel(
            logo_frame,
            text="🎮",
            font=("Segoe UI Emoji", 28),
        ).pack(side="left")

        ctk.CTkLabel(
            logo_frame,
            text="GameOptimizer AI",
            font=FONT_SUBTITLE,
            text_color=TEAL,
        ).pack(side="left", padx=10)

        # Правая часть навбара
        right_frame = ctk.CTkFrame(nav_inner, fg_color="transparent")
        right_frame.pack(side="right", pady=10)

        # Имя пользователя
        self._user_label = ctk.CTkLabel(
            right_frame,
            text=f"Привет, {self.user_name or 'друг'}! 💕" if self.user_name else "💕",
            font=FONT_BODY,
            text_color=PINK_SOFT,
        )
        self._user_label.pack(side="right", padx=10)

        # Кнопка информации о ПК
        self._pc_btn = ctk.CTkButton(
            right_frame,
            text="💻 Мой ПК",
            fg_color="transparent",
            hover_color=BG_CARD_HOV,
            text_color=WHITE_DIM,
            border_width=1,
            border_color=BORDER_GLOW,
            corner_radius=RADIUS_SMALL,
            font=FONT_SMALL,
            width=90,
            command=self._show_pc_info,
        )
        self._pc_btn.pack(side="right", padx=5)

    def _build_games_grid(self):
        """Построить сетку игровых карточек."""
        # Заголовок секции
        header = ctk.CTkFrame(self._games_panel, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 8))

        ctk.CTkLabel(
            header,
            text="🎮 Выбери игру",
            font=FONT_TITLE,
            text_color=WHITE,
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text=f"{len(GAMES_DATA)} игр",
            font=FONT_SMALL,
            text_color=WHITE_FADED,
        ).pack(side="left", padx=12)

        # Контейнер сетки
        grid_frame = ctk.CTkFrame(self._games_panel, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=16, pady=8)

        # Расставляем карточки
        COLS = 4
        for i, game in enumerate(GAMES_DATA):
            row = i // COLS
            col = i % COLS

            card = GameCard(
                grid_frame,
                game=game,
                on_click=self._open_game_window,
            )
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            grid_frame.grid_columnconfigure(col, weight=1)

        # Нижний отступ
        ctk.CTkLabel(
            self._games_panel,
            text="",
            height=20,
        ).pack()

    def _open_game_window(self, game: dict):
        """Открыть окно оптимизации игры."""
        from ui.game_window import GameWindow
        win = GameWindow(self, game, user_name=self.user_name)
        win.focus()

        # AI-друг комментирует
        self.after(300, lambda: self._ai_panel.notify(
            f"О, {game['name']}! {game.get('emoji', '')} Хороший выбор, {self.user_name}! "
            f"Давай настроим её по максимуму! 🚀"
        ))

    def _show_welcome(self):
        """Показать диалог первого запуска."""
        dialog = WelcomeDialog(self, self._on_name_set)

    def _on_name_set(self, name: str):
        """Обработчик установки имени."""
        self.user_name = name
        self.ai.set_name(name)
        self._user_label.configure(text=f"Привет, {name}! 💕")

        # Приветствие от AI
        self.after(200, lambda: self._ai_panel.notify(
            f"Привет, {name}! 🎉 Я так рада познакомиться с тобой!\n"
            f"Нажми на любую игру — и мы начнём! ✨"
        ))

    def _show_pc_info(self):
        """Показать информацию о ПК."""
        if not self.pc:
            return

        info_win = ctk.CTkToplevel(self)
        info_win.title("💻 Твой ПК")
        info_win.geometry("400x320")
        info_win.configure(fg_color=BG_MAIN)
        info_win.resizable(False, False)
        info_win.grab_set()

        ctk.CTkLabel(
            info_win,
            text="💻 Твоё железо",
            font=FONT_TITLE,
            text_color=TEAL,
        ).pack(pady=(24, 16))

        tier_colors = {"low": WARNING, "mid": TEAL, "high": SUCCESS}
        tier_names = {"low": "Начальный", "mid": "Средний", "high": "Высокий"}
        tier_color = tier_colors.get(self.pc.tier, TEAL)
        tier_name = tier_names.get(self.pc.tier, "Средний")

        info_frame = ctk.CTkFrame(info_win, fg_color=BG_CARD, corner_radius=RADIUS_LARGE)
        info_frame.pack(fill="x", padx=24)

        rows = [
            ("🖥 CPU", self.pc.cpu_name[:40]),
            ("💾 RAM", f"{self.pc.ram_gb} GB"),
            ("🎮 GPU", self.pc.gpu_name[:40]),
            ("📊 VRAM", f"{self.pc.gpu_vram_gb} GB"),
            ("⚡ Тир ПК", tier_name),
        ]

        for icon_label, value in rows:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=4)

            ctk.CTkLabel(
                row,
                text=icon_label,
                font=FONT_SMALL,
                text_color=WHITE_FADED,
                width=80,
                anchor="w",
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=value,
                font=FONT_BODY_BOLD if icon_label == "⚡ Тир ПК" else FONT_SMALL,
                text_color=tier_color if icon_label == "⚡ Тир ПК" else WHITE,
                anchor="w",
            ).pack(side="left", padx=8)

        ctk.CTkLabel(
            info_win,
            text="💕 Оценки FPS подобраны специально под твоё железо!",
            font=FONT_TINY,
            text_color=WHITE_FADED,
        ).pack(pady=16)

        PixarButton(
            info_win,
            text="Отлично!",
            style="primary",
            command=info_win.destroy,
            width=120,
        ).pack()

    def _load_pc(self):
        """Загрузить информацию о ПК в фоне."""
        self.pc = get_pc_info()
        self.after(0, lambda: self._pc_btn.configure(
            text=f"💻 {self.pc.tier.upper()} тир"
        ))
