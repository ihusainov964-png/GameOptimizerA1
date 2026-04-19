# filepath: core/optimizer_engine.py
"""
Движок оптимизации — применяет оптимизации для каждой игры.
Все действия логируются и могут быть отменены.
"""

import os
import sys
import time
import threading
from typing import Callable
from utils.logger import get_logger
from utils.settings import mark_optimization_applied, unmark_optimization

log = get_logger("OptimizerEngine")

# Процессы, которые НИКОГДА нельзя трогать (защита от бана)
PROTECTED_PROCESSES = {
    "easyanticheat.exe",
    "easyanticheat_eos.exe",
    "beservice.exe",
    "be_launcher.exe",
    "vgc.exe",
    "vanguard.exe",
    "faceit.exe",
    "faceitclient.exe",
    "xigncode.exe",
    "gameguard.des",
    "nprotect.exe",
    "steam.exe",
    "epicgameslauncher.exe",
    "battlenet.exe",
    "wargaming.net game center.exe",
    "riotclientservices.exe",
    "leagueclient.exe",
}

# Безопасные паразитные процессы
PARASITE_PROCESSES = [
    ("discord.exe", "Discord", False),          # закрываем только overlay, сам Discord опционально
    ("discordoverlay.exe", "Discord Overlay", True),
    ("nvbackend.exe", "GeForce Experience", True),
    ("nvcontainer.exe", "NVIDIA Container", False),
    ("msiafterburner.exe", "MSI Afterburner", False),
    ("rtss.exe", "RivaTuner", False),
    ("icue.exe", "Corsair iCUE", True),
    ("lightingservice.exe", "ASUS Aura", True),
    ("lgfwupdater.exe", "Logitech FW Updater", True),
    ("lghub.exe", "Logitech G Hub", False),
    ("razer synapse.exe", "Razer Synapse", False),
    ("rgb fusion.exe", "GIGABYTE RGB Fusion", True),
    ("alienfx.exe", "Alienware FX", True),
    ("overwolf.exe", "Overwolf", True),
    ("playnite.exe", "Playnite", True),
]


class OptimizationResult:
    def __init__(self, success: bool, message: str, fps_gained: int = 0):
        self.success = success
        self.message = message
        self.fps_gained = fps_gained


def apply_optimization(
    game_id: str,
    opt: dict,
    on_progress: Callable[[str], None] | None = None,
) -> OptimizationResult:
    """
    Применить одну оптимизацию.
    В реальном проекте здесь были бы конкретные системные вызовы.
    Сейчас — безопасная симуляция с логированием.
    """
    opt_id = opt.get("id", "unknown")
    title = opt.get("title", "Оптимизация")

    if on_progress:
        on_progress(f"Применяю: {title}...")

    log.info(f"[{game_id}] Применяю оптимизацию: {opt_id} — {title}")

    try:
        # Специальная обработка для очистки паразитов
        if opt.get("category") == "Очистка":
            _cleanup_parasites(on_progress)

        # Симуляция применения (0.5–1.5 сек)
        time.sleep(0.3)

        mark_optimization_applied(game_id, opt_id)
        log.info(f"[{game_id}] ✅ Оптимизация применена: {opt_id}")

        return OptimizationResult(
            success=True,
            message=f"✅ {title} — применено!",
            fps_gained=_get_tier_gain(opt),
        )

    except Exception as e:
        log.error(f"[{game_id}] ❌ Ошибка оптимизации {opt_id}: {e}")
        return OptimizationResult(
            success=False,
            message=f"❌ Ошибка: {title} — {str(e)}",
        )


def apply_all_optimizations(
    game_id: str,
    optimizations: list,
    on_progress: Callable[[str, int, int], None] | None = None,
    on_complete: Callable[[int], None] | None = None,
) -> None:
    """Применить все оптимизации в фоновом потоке."""

    def worker():
        total = len(optimizations)
        total_fps = 0

        for i, opt in enumerate(optimizations):
            if on_progress:
                on_progress(opt.get("title", "..."), i + 1, total)

            result = apply_optimization(game_id, opt)
            if result.success:
                total_fps += result.fps_gained
            time.sleep(0.2)

        if on_complete:
            on_complete(total_fps)

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()


def _cleanup_parasites(on_progress: Callable | None = None) -> None:
    """Безопасно закрыть паразитные процессы."""
    try:
        import psutil
    except ImportError:
        log.warning("psutil не установлен — очистка пропущена")
        return

    for proc_name, display_name, auto_close in PARASITE_PROCESSES:
        if not auto_close:
            continue

        proc_lower = proc_name.lower()

        # Проверяем защиту
        if proc_lower in PROTECTED_PROCESSES:
            log.warning(f"🛡️ Защищён — пропускаем: {proc_name}")
            continue

        try:
            for proc in psutil.process_iter(["name", "pid"]):
                if proc.info["name"] and proc.info["name"].lower() == proc_lower:
                    proc.terminate()
                    log.info(f"🧹 Закрыт паразит: {display_name} (PID {proc.info['pid']})")
                    if on_progress:
                        on_progress(f"Закрываю {display_name}...")
        except Exception as e:
            log.error(f"Ошибка при закрытии {proc_name}: {e}")


def _get_tier_gain(opt: dict) -> int:
    """Получить прирост FPS для текущего тира ПК."""
    try:
        from core.pc_detector import get_pc_info
        tier = get_pc_info().tier
    except Exception:
        tier = "mid"

    gains = opt.get("fps_gain", {"low": 5, "mid": 8, "high": 4})
    return gains.get(tier, gains.get("mid", 5))
