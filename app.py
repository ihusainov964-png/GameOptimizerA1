# filepath: ui/game_window.py
"""
Окно оптимизации игры.
"""

import threading
import customtkinter as ctk
from ui.theme import *
from ui.widgets import PixarButton
from core.optimizer_engine import apply_optimization, apply_all_optimizations
from core.launcher import launch_game
from core.pc_detector import get_pc_info, get_fps_estimate
from utils.settings import get_applied_optimizations, mark_optimization_applied


class GameWindow(ctk.CTkToplevel):

    def __init__(self, parent, game: dict,
                 user_name: str = "", on_applied=None):
        super().__init__(parent)

        self.game       = game
        self.user_name  = user_name
        self.on_applied = on_applied
        self.pc         = get_pc_info()
        self.applied    = set(get_applied_optimizations(game["id"]))
        self._color     = game.get("color", TEAL)

        self.title(f"✨ {game['name']} — GameOptimizer AI")
        self.geometry("920x680")
        self.configure(fg_color=BG_MAIN)
        self.resizable(True, True)
        self.grab_set()

        self._build()

    # ── Build ────────────────────────────────────────

    def _build(self):
        self._build_header()

        # Основная область
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True)

        # Сайдбар категорий
        self._sidebar = ctk.CTkScrollableFrame(
            main, fg_color=BG_PANEL, width=185, corner_radius=0)
        self._sidebar.pack(side="left", fill="y")

        # Контент оптимизаций
        self._content = ctk.CTkScrollableFrame(
            main, fg_color=BG_MAIN, corner_radius=0)
        self._content.pack(side="left", fill="both", expand=True)

        # Статус-бар
        self._status = ctk.CTkLabel(
            self,
            text=f"💕 Выбери категорию слева, {self.user_name or 'друг'}!",
            font=FONT_SMALL,
            text_color=WHITE_FADED,
            fg_color=BG_PANEL,
            anchor="w")
        self._status.pack(fill="x", padx=14, pady=4)

        self._cats = self._get_categories()
        self._build_sidebar()
        if self._cats:
            self._show_category(self._cats[0])

    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color=BG_PANEL,
                           height=72, corner_radius=0)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        ctk.CTkFrame(hdr, fg_color=self._color,
                     height=3, corner_radius=0).pack(fill="x", side="top")

        row = ctk.CTkFrame(hdr, fg_color="transparent")
        row.pack(fill="both", expand=True, padx=16)

        ctk.CTkLabel(row,
                     text=self.game.get("emoji", "🎮"),
                     font=("Segoe UI Emoji", 30)).pack(side="left", pady=10)

        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(info, text=self.game["name"],
                     font=FONT_TITLE, text_color=WHITE).pack(anchor="w")
        ctk.CTkLabel(info,
                     text=f"CPU: {self.pc.cpu_name[:28]}  |  "
                          f"GPU: {self.pc.gpu_name[:22]}  |  "
                          f"RAM: {self.pc.ram_gb}GB",
                     font=FONT_TINY,
                     text_color=WHITE_FADED).pack(anchor="w")

        btns = ctk.CTkFrame(row, fg_color="transparent")
        btns.pack(side="right", pady=10)

        PixarButton(btns, text="🚀 Запустить",
                    style="orange",
                    command=self._launch,
                    width=130, height=34).pack(side="right", padx=4)

        PixarButton(btns, text="⚡ Всё сразу",
                    style="primary",
                    command=self._optimize_all,
                    width=130, height=34).pack(side="right", padx=4)

    def _build_sidebar(self):
        ctk.CTkLabel(self._sidebar, text="Категории",
                     font=FONT_SMALL,
                     text_color=WHITE_FADED).pack(anchor="w", padx=10,
                                                  pady=(14, 6))
        self._cat_btns = {}
        for cat in self._cats:
            icon  = CATEGORY_ICONS.get(cat, "•")
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
            btn.pack(fill="x", padx=6, pady=2)
            self._cat_btns[cat] = (btn, color)

        # Кнопка очистки
        ctk.CTkFrame(self._sidebar, fg_color=BORDER,
                     height=1).pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(
            self._sidebar,
            text="🧹  Очистить паразитов",
            fg_color=PINK + "20",
            hover_color=PINK + "40",
            text_color=PINK_SOFT,
            corner_radius=RADIUS_SMALL,
            font=FONT_SMALL,
            border_width=1,
            border_color=PINK_DIM,
            command=self._cleanup,
        ).pack(fill="x", padx=6, pady=2)

    # ── Categories ───────────────────────────────────

    def _get_categories(self):
        cats = []
        for o in self.game.get("optimizations", []):
            c = o.get("category", "Другое")
            if c not in cats:
                cats.append(c)
        return cats

    def _show_category(self, cat: str):
        self._current_cat = cat

        # Обновить подсветку в сайдбаре
        for c, (btn, color) in self._cat_btns.items():
            if c == cat:
                btn.configure(fg_color=color + "25",
                              text_color=color,
                              border_width=1, border_color=color)
            else:
                btn.configure(fg_color="transparent",
                              text_color=WHITE_DIM, border_width=0)

        # Очистить контент
        for w in self._content.winfo_children():
            w.destroy()

        icon  = CATEGORY_ICONS.get(cat, "•")
        color = CATEGORY_COLORS.get(cat, TEAL)
        opts  = [o for o in self.game.get("optimizations", [])
                 if o.get("category") == cat]
        done  = sum(1 for o in opts if o["id"] in self.applied)

        # Заголовок
        hrow = ctk.CTkFrame(self._content, fg_color="transparent")
        hrow.pack(fill="x", padx=18, pady=(14, 6))
        ctk.CTkLabel(hrow, text=f"{icon}  {cat}",
                     font=FONT_TITLE, text_color=color).pack(side="left")
        ctk.CTkLabel(hrow, text=f"{done}/{len(opts)} применено",
                     font=FONT_SMALL,
                     text_color=WHITE_FADED).pack(side="left", padx=14)

        ctk.CTkFrame(self._content, fg_color=BORDER_GLOW,
                     height=1).pack(fill="x", padx=18, pady=(0, 10))

        for opt in opts:
            self._build_opt_card(opt, color)

    def _build_opt_card(self, opt: dict, color: str):
        done = opt["id"] in self.applied
        fps  = get_fps_estimate(opt, self.pc.tier)

        frame = ctk.CTkFrame(
            self._content,
            fg_color=BG_CARD_HOV if done else BG_CARD,
            corner_radius=RADIUS_MEDIUM,
            border_width=1,
            border_color=(SUCCESS + "55") if done else BORDER,
        )
        frame.pack(fill="x", padx=18, pady=5)

        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=14, pady=10)

        # Строка 1: Название + статус + FPS
        r1 = ctk.CTkFrame(inner, fg_color="transparent")
        r1.pack(fill="x")

        ctk.CTkLabel(r1,
                     text=opt.get("title", ""),
                     font=FONT_BODY_BOLD,
                     text_color=SUCCESS if done else WHITE).pack(side="left")

        if done:
            ctk.CTkLabel(r1, text="✅ Применено",
                         font=FONT_SMALL,
                         text_color=SUCCESS).pack(side="left", padx=8)

        # FPS бейдж
        fps_f = ctk.CTkFrame(r1,
                             fg_color=ORANGE + "22",
                             corner_radius=RADIUS_SMALL,
                             border_width=1,
                             border_color=ORANGE_DIM)
        fps_f.pack(side="right")
        ctk.CTkLabel(fps_f, text=fps,
                     font=FONT_SMALL,
                     text_color=ORANGE_WARM).pack(padx=8, pady=2)

        # Описание
        ctk.CTkLabel(inner,
                     text=opt.get("description", ""),
                     font=FONT_SMALL,
                     text_color=WHITE_FADED,
                     wraplength=560,
                     justify="left",
                     anchor="w").pack(fill="x", pady=(5, 8))

        # Строка 3: кнопки
        r3 = ctk.CTkFrame(inner, fg_color="transparent")
        r3.pack(fill="x")

        if not done:
            PixarButton(r3, text="⚡ Применить",
                        style="primary",
                        command=lambda o=opt: self._apply_one(o),
                        width=120, height=30).pack(side="left")
        else:
            PixarButton(r3, text="↩ Отменить",
                        style="secondary",
                        command=lambda o=opt: self._revert_one(o),
                        width=120, height=30).pack(side="left")

        # Бейдж безопасности
        if opt.get("safe_for_anticheat"):
            sf = ctk.CTkFrame(r3,
                              fg_color=SUCCESS + "15",
                              corner_radius=RADIUS_SMALL,
                              border_width=1,
                              border_color=SUCCESS + "40")
            sf.pack(side="left", padx=8)
            ctk.CTkLabel(sf, text="🛡️ Безопасно",
                         font=FONT_TINY,
                         text_color=SUCCESS).pack(padx=6, pady=2)

    # ── Actions ──────────────────────────────────────

    def _apply_one(self, opt: dict):
        self._set_status(f"⏳ Применяю: {opt['title']}...")

        def run():
            apply_optimization(self.game["id"], opt)
            self.applied.add(opt["id"])
            fps = get_fps_estimate(opt, self.pc.tier)
            self.after(0, lambda: self._set_status(
                f"✅ {opt['title']} — готово! {fps}"))
            self.after(80, lambda: self._show_category(self._current_cat))
            if self.on_applied:
                self.after(120, lambda: self.on_applied(self.game["id"]))

        threading.Thread(target=run, daemon=True).start()

    def _revert_one(self, opt: dict):
        from utils.settings import unmark_optimization
        unmark_optimization(self.game["id"], opt["id"])
        self.applied.discard(opt["id"])
        self._set_status(f"↩ {opt['title']} — отменено")
        self._show_category(self._current_cat)

    def _optimize_all(self):
        opts = self.game.get("optimizations", [])
        prog = _ProgressWin(self, self.game["name"],
                            self.user_name, self._color)

        def on_prog(title, cur, total):
            self.after(0, lambda: prog.update(title, cur / total, cur, total))

        def on_done(fps):
            for o in opts:
                self.applied.add(o["id"])
            self.after(0, lambda: prog.complete(fps))
            self.after(0, lambda: self._show_category(self._current_cat))
            self.after(0, lambda: self._set_status(
                f"🎉 Всё готово! Ожидаемый прирост: +{fps} FPS"))
            if self.on_applied:
                self.after(100, lambda: self.on_applied(self.game["id"]))

        apply_all_optimizations(self.game["id"], opts,
                                on_progress=on_prog, on_complete=on_done)

    def _cleanup(self):
        from core.optimizer_engine import _cleanup_parasites
        self._set_status("🧹 Очищаю паразитные процессы...")
        threading.Thread(
            target=lambda: _cleanup_parasites(
                lambda m: self.after(0, lambda: self._set_status(f"🧹 {m}"))),
            daemon=True).start()

    def _launch(self):
        ok, msg = launch_game(self.game)
        self._set_status(msg)

    def _set_status(self, text: str):
        self._status.configure(text=text)


# ── Progress window ──────────────────────────────

class _ProgressWin(ctk.CTkToplevel):

    def __init__(self, parent, game: str, user: str, color: str):
        super().__init__(parent)
        self._done = False
        self._user = user
        self.title("Оптимизация...")
        self.geometry("420x230")
        self.configure(fg_color=BG_MAIN)
        self.resizable(False, False)
        self.grab_set()
        self._build(game, color)

    def _build(self, game: str, color: str):
        ctk.CTkLabel(self, text="✨ Оптимизируем...",
                     font=FONT_SUBTITLE,
                     text_color=color).pack(pady=(24, 4))
        ctk.CTkLabel(self, text=game,
                     font=FONT_BODY,
                     text_color=WHITE_DIM).pack()

        self._bar = ctk.CTkProgressBar(self,
                                       progress_color=color,
                                       fg_color=BORDER,
                                       height=8)
        self._bar.pack(fill="x", padx=40, pady=16)
        self._bar.set(0)

        self._lbl = ctk.CTkLabel(self, text="Начинаю...",
                                 font=FONT_SMALL,
                                 text_color=WHITE_FADED)
        self._lbl.pack()

        self._cnt = ctk.CTkLabel(self, text="0 / 0",
                                 font=FONT_TINY,
                                 text_color=WHITE_FADED)
        self._cnt.pack(pady=4)

    def update(self, title: str, pct: float, cur: int, total: int):
        if self._done:
            return
        self._bar.set(min(pct, 1.0))
        self._lbl.configure(text=title)
        self._cnt.configure(text=f"{cur} / {total}")

    def complete(self, fps: int):
        self._done = True
        self._bar.set(1.0)
        name = self._user or "друг"
        self._lbl.configure(
            text=f"🎉 Готово, {name}! +{fps} FPS!",
            text_color=SUCCESS)
        self._cnt.configure(text="Все оптимизации применены!")
        self.after(2500, self.destroy)
