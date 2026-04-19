# filepath: core/parasite_cleaner.py
"""
Безопасная очистка паразитных процессов.
Строго защищает античит и системные процессы от закрытия.
"""

from core.optimizer_engine import PROTECTED_PROCESSES, PARASITE_PROCESSES, _cleanup_parasites
from utils.logger import get_logger

log = get_logger("ParasiteCleaner")


def get_running_parasites() -> list[dict]:
    """
    Вернуть список паразитных процессов, которые сейчас запущены.
    Не закрывает — только возвращает список для отображения.
    """
    running = []
    try:
        import psutil
        for proc_name, display_name, auto in PARASITE_PROCESSES:
            for proc in psutil.process_iter(["name", "pid", "memory_info"]):
                try:
                    if proc.info["name"] and proc.info["name"].lower() == proc_name.lower():
                        mem_mb = round(proc.info["memory_info"].rss / (1024 * 1024), 1)
                        running.append({
                            "name": proc_name,
                            "display": display_name,
                            "pid": proc.info["pid"],
                            "memory_mb": mem_mb,
                            "auto": auto,
                            "protected": proc_name.lower() in PROTECTED_PROCESSES,
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
    except ImportError:
        log.warning("psutil не установлен")
    return running


def clean_all_safe(on_progress=None) -> tuple[int, int]:
    """
    Закрыть все безопасные паразитные процессы.
    Возвращает (закрыто, пропущено).
    """
    closed = 0
    skipped = 0

    try:
        import psutil
        for proc_name, display_name, auto_close in PARASITE_PROCESSES:
            if not auto_close:
                skipped += 1
                continue

            if proc_name.lower() in PROTECTED_PROCESSES:
                log.warning(f"🛡️ Защищён — пропущен: {proc_name}")
                skipped += 1
                continue

            for proc in psutil.process_iter(["name", "pid"]):
                try:
                    if proc.info["name"] and proc.info["name"].lower() == proc_name.lower():
                        proc.terminate()
                        closed += 1
                        log.info(f"🧹 Закрыт: {display_name}")
                        if on_progress:
                            on_progress(f"Закрыт: {display_name}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

    except ImportError:
        log.warning("psutil не доступен")

    return closed, skipped
