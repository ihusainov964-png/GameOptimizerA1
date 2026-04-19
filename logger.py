# filepath: utils/settings.py
"""
Хранение настроек пользователя (имя, применённые оптимизации и т.д.)
"""

import json
import os

SETTINGS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "user_settings.json"
)


def load_settings() -> dict:
    """Загрузить настройки из файла."""
    if not os.path.exists(SETTINGS_FILE):
        return {}
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(data: dict) -> None:
    """Сохранить настройки в файл."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Settings] Не удалось сохранить: {e}")


def get(key: str, default=None):
    return load_settings().get(key, default)


def set_val(key: str, value) -> None:
    data = load_settings()
    data[key] = value
    save_settings(data)


def get_applied_optimizations(game_id: str) -> list:
    data = load_settings()
    return data.get("applied", {}).get(game_id, [])


def mark_optimization_applied(game_id: str, opt_id: str) -> None:
    data = load_settings()
    if "applied" not in data:
        data["applied"] = {}
    if game_id not in data["applied"]:
        data["applied"][game_id] = []
    if opt_id not in data["applied"][game_id]:
        data["applied"][game_id].append(opt_id)
    save_settings(data)


def unmark_optimization(game_id: str, opt_id: str) -> None:
    data = load_settings()
    applied = data.get("applied", {}).get(game_id, [])
    if opt_id in applied:
        applied.remove(opt_id)
    if "applied" in data and game_id in data["applied"]:
        data["applied"][game_id] = applied
    save_settings(data)
