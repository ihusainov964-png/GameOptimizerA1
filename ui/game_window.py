# filepath: ui/game_window.py
"""
Окно оптимизации конкретной игры.
"""

import tkinter as tk
import customtkinter as ctk
import random
import threading
from ui.theme import *
from ui.widgets import (
    PixarButton, GlowLabel, FPSBadge, SafeBadge,
    ProgressRing, Divider, SectionHeader,
)
from core.optimizer_engine import apply_optimization, apply_all_optimizations
from core.launcher import launch_game
from core.pc_detector import get_pc_info, get_fps_estimate
from utils.settings import get_applied_optimizations, mark_optimization_applied


class GameWindow(ctk.CTkToplevel):
    """Окно оптимизации с вкладками по категориям."""

    def __init__(self, parent, game: dict, user_name: str = ""):
        super().__init__(parent)

        self.game = game
        self.user_name = user_name
        self.pc = get_pc_info()
        self.applied = set(get_applied_optimizations(game["id"]))
        self.game_color = game.get("color", TEAL)

        self.title(f"✨ {game['name']} — GameOptimizer AI")
        self.geometry("900x680")
        self.configure(fg_color=BG_MAIN)
        self.resizable(True, True)
        self.grab_set()  # Модальное окно

        self._build()

    def _build(self):
        """Построить интерфейс окна."""

        # ── Заголовок ──────────────────────────────
        header = ctk.CTkFrame(self, fg_color=BG_PANEL, corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Цветная полоска
        accent_bar = ctk.CTkFrame(header, fg_color=self.game_color, height=3, corner_radius=0)
        accent_bar.pack(fill="x", side="top")

        header_inner = ctk.CTkFrame(header, fg_color="transparent")
        header_inner.pack(fill="both", expand=True, padx=20)

        # Emoji + название
        ctk.CTkLabel(
            header_inner,
            text=self.game.get("emoji", "🎮"),
            font=("Segoe UI Emoji", 32),
        ).pack(side="left", pady=10)

        title_frame = ctk.CTkFrame(header_inner, fg_color="transparent")
        title_frame.pack(side="left", padx=12, pady=10)

        ctk.CTkLabel(
            title_frame,
            text=self.game["name"],
            font=FONT_TITLE,
            text_color=WHITE,
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text=f"CPU: {self.pc.cpu_name[:30]}  |  GPU: {self.pc.gpu_name[:25]}  |  RAM: {self.pc.ram_gb}GB",
            font=FONT_TINY,
            text_color=WHITE_FADED,
        ).pack(anchor="w")

        # Кнопки справа
        btn_frame = ctk.CTkFrame(header_inner, fg_color="transparent")
        btn_frame.pack(side="right", padx=0, pady=10)

        PixarButton(
            btn_frame,
            text="🚀 Запустить игру",
            style="orange",
            command=self._launch_game,
            width=150,
        ).pack(side="right", padx=5)

        PixarButton(
            btn_frame,
            text="⚡ Оптимизировать всё",
            style="primary",
            command=self._optimize_all,
            width=170,
        ).pack(side="right", padx=5)

        # ── Основная область ───────────────────────
        main_area = ctk.CTkFrame(self, fg_color="transparent")
        main_area.pack(fill="both", expand=True, padx=0, pady=0)

        # Левая панель — список категорий
        self._sidebar = ctk.CTkScrollableFrame(
            main_area,
            fg_color=BG_PANEL,
            width=190,
            corner_radius=0,
        )
        self._sidebar.pack(side="left", fill="y")

        # Правая панель — список оптимизаций
        self._content = ctk.CTkScrollableFrame(
            main_area,
            fg_color=BG_MAIN,
            corner_radius=0,
        )
        self._content.pack(side="left", fill="both", expand=True)

        # ── Статус-бар ─────────────────────────────
        self._status_bar = ctk.CTkLabel(
            self,
            text=f"💕 Готово к оптимизации, {self.user_name}! Выбери категорию слева.",
            text_color=WHITE_FADED,
            font=FONT_SMALL,
            fg_color=BG_PANEL,
            anchor="w",
        )
        self._status_bar.pack(fill="x", padx=16, pady=4)

        # ── Наполнение ─────────────────────────────
        self._categories = self._get_categories()
        self._build_sidebar()
        self._current_category = self._categories[0] if self._categories else None
        self._show_category(self._current_category)

    def _get_categories(self) -> list:
        """Получить уникальные категории оптимизаций."""
        cats = []
        for opt in self.game.get("optimizations", []):
            c = opt.get("category", "Другое")
            if c not in cats:
                cats.append(c)
        return cats

    def _build_sidebar(self):
        """Построить боковую панель с категориями."""
        ctk.CTkLabel(
            self._sidebar,
            text="Категории",
            font=FONT_SMALL,
            text_color=WHITE_FADED,
        ).pack(anchor="w", padx=12, pady=(16, 8))

        self._cat_buttons = {}

        for cat in self._categories:
            icon = CATEGORY_ICONS.get(cat, "•")
            color = CATEGORY_COLORS.get(cat, TEAL)

            btn = ctk.CTkButton(
                self._sidebar,
                text=f"{icon}  {cat}",
                fg_color="transparent",
                hover_color=BG_CARD_HOV,
                text_color=WHITE_DIM,
                anchor="w",
                corner_radius=RADIUS_SMALL,
                font=FONT_BODY,
                command=lambda c=cat: self._show_category(c),
            )
            btn.pack(fill="x", padx=8, pady=2)
            self._cat_buttons[cat] = (btn, color)

        # Кнопка очистки паразитов
        Divider(self._sidebar).pack(fill="x", padx=12, pady=12)

        ctk.CTkButton(
            self._sidebar,
            text="🧹  Очистить паразитов",
            fg_color=PINK + "20",
            hover_color=PINK + "40",
            text_color=PINK_SOFT,
            corner_radius=RADIUS_SMALL,
            font=FONT_BODY,
            border_width=1,
            border_color=PINK_DIM,
            command=self._cleanup_only,
        ).pack(fill="x", padx=8, pady=2)

    def _show_category(self, category: str):
        """Показать оптимизации выбранной категории."""
        self._current_category = category

        # Обновить выделение в сайдбаре
        for cat, (btn, color) in self._cat_buttons.items():
            if cat == category:
                btn.configure(
                    fg_color=color + "25",
                    text_color=color,
                    border_width=1,
                    border_color=color,
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=WHITE_DIM,
                    border_width=0,
                )

        # Очистить контент
        for widget in self._content.winfo_children():
            widget.destroy()

        # Заголовок категории
        icon = CATEGORY_ICONS.get(category, "•")
        color = CATEGORY_COLORS.get(category, TEAL)

        header = ctk.CTkFrame(self._content, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(
            header,
            text=f"{icon}  {category}",
            font=FONT_TITLE,
            text_color=color,
        ).pack(side="left")

        # Считаем применённые
        cat_opts = [o for o in self.game.get("optimizations", []) if o.get("category") == category]
        done = sum(1 for o in cat_opts if o["id"] in self.applied)

        ctk.CTkLabel(
            header,
            text=f"{done}/{len(cat_opts)} применено",
            font=FONT_SMALL,
            text_color=WHITE_FADED,
        ).pack(side="left", padx=16)

        Divider(self._content, color=BORDER_GLOW).pack(fill="x", padx=20, pady=(0, 12))

        # Карточки оптимизаций
        for opt in cat_opts:
            self._build_opt_card(opt, color)

        if not cat_opts:
            ctk.CTkLabel(
                self._content,
                text="Нет оптимизаций в этой категории",
                text_color=WHITE_FADED,
                font=FONT_BODY,
            ).pack(pady=40)

    def _build_opt_card(self, opt: dict, accent_color: str):
        """Построить карточку одной оптимизации."""
        is_applied = opt["id"] in self.applied
        fps_text = get_fps_estimate(opt, self.pc.tier)

        # Внешний контейнер
        outer = ctk.CTkFrame(
            self._content,
            fg_color=BG_CARD if not is_applied else BG_CARD_HOV,
            corner_radius=RADIUS_MEDIUM,
            border_width=1,
            border_color=(SUCCESS + "60") if is_applied else BORDER,
        )
        outer.pack(fill="x", padx=20, pady=6)

        # Внутренний layout
        inner = ctk.CTkFrame(outer, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=12)

        # Строка 1: Заголовок + бейджи
        row1 = ctk.CTkFrame(inner, fg_color="transparent")
        row1.pack(fill="x")

        ctk.CTkLabel(
            row1,
            text=opt.get("title", "Оптимизация"),
            font=FONT_BODY_BOLD,
            text_color=WHITE if not is_applied else SUCCESS,
        ).pack(side="left")

        if is_applied:
            ctk.CTkLabel(
                row1,
                text="✅ Применено",
                font=FONT_SMALL,
                text_color=SUCCESS,
            ).pack(side="left", padx=8)

        # FPS бейдж справа
        fps_frame = ctk.CTkFrame(
            row1,
            fg_color=ORANGE + "20",
            corner_radius=RADIUS_SMALL,
            border_width=1,
            border_color=ORANGE_DIM,
        )
        fps_frame.pack(side="right")
        ctk.CTkLabel(
            fps_frame,
            text=fps_text,
            font=FONT_SMALL,
            text_color=ORANGE_WARM,
        ).pack(padx=8, pady=2)

        # Строка 2: Описание
        ctk.CTkLabel(
            inner,
            text=opt.get("description", ""),
            font=FONT_SMALL,
            text_color=WHITE_FADED,
            wraplength=560,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(6, 8))

        # Строка 3: Кнопки + безопасность
        row3 = ctk.CTkFrame(inner, fg_color="transparent")
        row3.pack(fill="x")

        # Кнопка применить / отменить
        if not is_applied:
            PixarButton(
                row3,
                text="⚡ Применить",
                style="primary",
                command=lambda o=opt: self._apply_single(o),
                width=130,
                height=32,
            ).pack(side="left")
        else:
            PixarButton(
                row3,
                text="↩ Отменить",
                style="secondary",
                command=lambda o=opt: self._revert_single(o),
                width=130,
                height=32,
            ).pack(side="left")

        # Бейдж безопасности
        if opt.get("safe_for_anticheat"):
            safe_frame = ctk.CTkFrame(
                row3,
                fg_color=SUCCESS + "15",
                corner_radius=RADIUS_SMALL,
                border_width=1,
                border_color=SUCCESS + "50",
            )
            safe_frame.pack(side="left", padx=8)
            ctk.CTkLabel(
                safe_frame,
                text="🛡️ Безопасно для античита",
                font=FONT_TINY,
                text_color=SUCCESS,
            ).pack(padx=6, pady=2)

    def _apply_single(self, opt: dict):
        """Применить одну оптимизацию."""
        self._set_status(f"⏳ Применяю: {opt['title']}...")

        def run():
            result = apply_optimization(self.game["id"], opt)
            self.applied.add(opt["id"])
            fps = get_fps_estimate(opt, self.pc.tier)
            self.after(0, lambda: self._set_status(
                f"✅ {opt['title']} — готово! Ожидаемый прирост: {fps}"
            ))
            self.after(100, lambda: self._show_category(self._current_category))

        threading.Thread(target=run, daemon=True).start()

    def _revert_single(self, opt: dict):
        """Отменить оптимизацию (симуляция)."""
        from utils.settings import unmark_optimization
        unmark_optimization(self.game["id"], opt["id"])
        self.applied.discard(opt["id"])
        self._set_status(f"↩ {opt['title']} — отменено")
        self._show_category(self._current_category)

    def _optimize_all(self):
        """Применить все оптимизации."""
        all_opts = self.game.get("optimizations", [])

        progress_win = _ProgressWindow(self, self.game["name"], self.user_name, self.game_color)

        def on_progress(title, current, total):
            pct = current / total
            self.after(0, lambda: progress_win.update(title, pct, current, total))

        def on_complete(total_fps):
            for opt in all_opts:
                self.applied.add(opt["id"])
            self.after(0, lambda: progress_win.complete(total_fps))
            self.after(0, lambda: self._show_category(self._current_category))
            self.after(0, lambda: self._set_status(
                f"🎉 Все оптимизации применены! Ожидаемый суммарный прирост: +{total_fps} FPS"
            ))

        apply_all_optimizations(
            self.game["id"],
            all_opts,
            on_progress=on_progress,
            on_complete=on_complete,
        )

    def _cleanup_only(self):
        """Только очистка паразитных процессов."""
        cleanup_opts = [
            o for o in self.game.get("optimizations", [])
            if o.get("category") == "Очистка"
        ]
        if cleanup_opts:
            for opt in cleanup_opts:
                self._apply_single(opt)
        else:
            # Запускаем общую очистку
            from core.optimizer_engine import _cleanup_parasites
            threading.Thread(
                target=lambda: _cleanup_parasites(
                    lambda msg: self.after(0, lambda: self._set_status(f"🧹 {msg}"))
                ),
                daemon=True,
            ).start()
            self._set_status("🧹 Очищаю паразитные процессы...")

    def _launch_game(self):
        """Запустить игру через правильный лаунчер."""
        success, msg = launch_game(self.game)
        self._set_status(msg)

    def _set_status(self, text: str):
        self._status_bar.configure(text=text)


class _ProgressWindow(ctk.CTkToplevel):
    """Красивое окно прогресса оптимизации."""

    def __init__(self, parent, game_name: str, user_name: str, accent: str):
        super().__init__(parent)
        self.accent = accent
        self.user_name = user_name
        self.game_name = game_name
        self._done = False

        self.title("Оптимизация...")
        self.geometry("440x260")
        self.configure(fg_color=BG_MAIN)
        self.resizable(False, False)
        self.grab_set()

        self._build()

    def _build(self):
        ctk.CTkLabel(
            self,
            text="✨ Оптимизируем для тебя...",
            font=FONT_SUBTITLE,
            text_color=self.accent,
        ).pack(pady=(28, 4))

        self._game_label = ctk.CTkLabel(
            self,
            text=self.game_name,
            font=FONT_BODY,
            text_color=WHITE_DIM,
        )
        self._game_label.pack()

        self._progress = ctk.CTkProgressBar(
            self,
            progress_color=self.accent,
            fg_color=BORDER,
            corner_radius=RADIUS_ROUND,
            height=10,
        )
        self._progress.pack(fill="x", padx=40, pady=20)
        self._progress.set(0)

        self._step_label = ctk.CTkLabel(
            self,
            text="Начинаю...",
            font=FONT_SMALL,
            text_color=WHITE_FADED,
        )
        self._step_label.pack()

        self._counter = ctk.CTkLabel(
            self,
            text="0 / 0",
            font=FONT_TINY,
            text_color=WHITE_FADED,
        )
        self._counter.pack(pady=4)

    def update(self, step_title: str, pct: float, current: int, total: int):
        if self._done:
            return
        self._progress.set(pct)
        self._step_label.configure(text=step_title)
        self._counter.configure(text=f"{current} / {total}")

    def complete(self, total_fps: int):
        self._done = True
        self._progress.set(1.0)
        self._step_label.configure(
            text=f"🎉 Готово, {self.user_name}! +{total_fps} FPS!",
            text_color=SUCCESS,
        )
        self._counter.configure(text="Все оптимизации применены!")
        self.after(2500, self.destroy)
