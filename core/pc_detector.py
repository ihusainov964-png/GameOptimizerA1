# filepath: core/pc_detector.py
"""
Определение характеристик ПК пользователя.
Используется для персонализированных FPS-оценок.
"""

import platform
import psutil
from utils.logger import get_logger

log = get_logger("PCDetector")


class PCInfo:
    """Хранит информацию о железе пользователя."""

    def __init__(self):
        self.cpu_name: str = "Неизвестно"
        self.cpu_cores: int = 4
        self.ram_gb: float = 8.0
        self.gpu_name: str = "Неизвестно"
        self.gpu_vram_gb: float = 4.0
        self.os_name: str = platform.system()
        self.tier: str = "mid"  # low / mid / high
        self.is_nvidia: bool = False

    def __str__(self):
        return (
            f"CPU: {self.cpu_name} ({self.cpu_cores} ядер)\n"
            f"RAM: {self.ram_gb:.1f} GB\n"
            f"GPU: {self.gpu_name} ({self.gpu_vram_gb:.1f} GB VRAM)\n"
            f"Тир ПК: {self.tier}\n"
            f"ОС: {self.os_name}"
        )


def detect_pc() -> PCInfo:
    """Определить характеристики ПК. Безопасно обрабатывает ошибки."""
    info = PCInfo()

    # CPU
    try:
        import subprocess
        result = subprocess.run(
            ["wmic", "cpu", "get", "name"],
            capture_output=True, text=True, timeout=3
        )
        lines = [l.strip() for l in result.stdout.splitlines() if l.strip() and l.strip() != "Name"]
        if lines:
            info.cpu_name = lines[0]
    except Exception:
        try:
            info.cpu_name = platform.processor() or "Неизвестно"
        except Exception:
            pass

    try:
        info.cpu_cores = psutil.cpu_count(logical=False) or 4
    except Exception:
        pass

    # RAM
    try:
        mem = psutil.virtual_memory()
        info.ram_gb = round(mem.total / (1024 ** 3), 1)
    except Exception:
        pass

    # GPU (через wmic или GPUtil)
    try:
        import subprocess
        result = subprocess.run(
            ["wmic", "path", "win32_VideoController", "get", "name,AdapterRAM"],
            capture_output=True, text=True, timeout=3
        )
        lines = result.stdout.splitlines()
        for line in lines[1:]:
            if line.strip() and not line.strip().startswith("AdapterRAM"):
                parts = line.strip().split()
                if parts:
                    # Последнее поле — RAM в байтах, остальное — название
                    try:
                        ram_bytes = int(parts[-1])
                        info.gpu_vram_gb = round(ram_bytes / (1024 ** 3), 1)
                        info.gpu_name = " ".join(parts[:-1])
                    except ValueError:
                        info.gpu_name = " ".join(parts)
                    break
    except Exception:
        pass

    # Попытка через GPUtil
    if info.gpu_name == "Неизвестно":
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                g = gpus[0]
                info.gpu_name = g.name
                info.gpu_vram_gb = round(g.memoryTotal / 1024, 1)
        except Exception:
            pass

    # Определить NVIDIA
    info.is_nvidia = "nvidia" in info.gpu_name.lower() or "rtx" in info.gpu_name.lower() or "gtx" in info.gpu_name.lower()

    # Определить тир ПК
    info.tier = _calculate_tier(info)

    log.info(f"Определён ПК: {info}")
    return info


def _calculate_tier(info: PCInfo) -> str:
    """Определить тир ПК: low / mid / high."""
    score = 0

    # RAM
    if info.ram_gb >= 32:
        score += 3
    elif info.ram_gb >= 16:
        score += 2
    elif info.ram_gb >= 8:
        score += 1

    # VRAM
    if info.gpu_vram_gb >= 12:
        score += 3
    elif info.gpu_vram_gb >= 8:
        score += 2
    elif info.gpu_vram_gb >= 4:
        score += 1

    # CPU ядра
    if info.cpu_cores >= 12:
        score += 3
    elif info.cpu_cores >= 8:
        score += 2
    elif info.cpu_cores >= 6:
        score += 1

    # Проверка по названию GPU
    high_end = ["4090", "4080", "4070 ti", "3090", "3080", "rx 7900", "rx 6900"]
    low_end = ["1050", "1030", "750", "rx 580", "rx 570", "rx 560"]

    gpu_lower = info.gpu_name.lower()
    if any(h in gpu_lower for h in high_end):
        score += 3
    elif any(l in gpu_lower for l in low_end):
        score -= 2

    if score >= 7:
        return "high"
    elif score >= 3:
        return "mid"
    else:
        return "low"


def get_fps_estimate(opt: dict, tier: str) -> str:
    """Вернуть строку с оценкой FPS для данного тира."""
    gains = opt.get("fps_gain", {"low": 5, "mid": 8, "high": 4})
    val = gains.get(tier, gains.get("mid", 5))
    if val <= 0:
        return "стабильность ↑"
    return f"+{val} FPS"


# Синглтон — определяем один раз при запуске
_pc_info: PCInfo | None = None


def get_pc_info() -> PCInfo:
    global _pc_info
    if _pc_info is None:
        _pc_info = detect_pc()
    return _pc_info
