# filepath: core/launcher.py
"""
Умный лаунчер игр.
Определяет правильный способ запуска каждой игры через её лаунчер.
"""

import os
import subprocess
import sys
from utils.logger import get_logger

log = get_logger("Launcher")


def launch_game(game: dict) -> tuple[bool, str]:
    """
    Запустить игру через правильный лаунчер.
    Возвращает (успех, сообщение).
    """
    launcher_type = game.get("launcher", "")
    game_name = game.get("name", "Игра")

    log.info(f"Запускаю {game_name} через лаунчер: {launcher_type}")

    try:
        if launcher_type == "steam":
            return _launch_steam(game)
        elif launcher_type == "epic":
            return _launch_epic(game)
        elif launcher_type == "battlenet":
            return _launch_battlenet(game)
        elif launcher_type == "riot":
            return _launch_riot(game)
        elif launcher_type == "wargaming":
            return _launch_wargaming(game)
        elif launcher_type == "exe":
            return _launch_exe(game)
        else:
            return False, f"Неизвестный лаунчер: {launcher_type}"

    except Exception as e:
        log.error(f"Ошибка запуска {game_name}: {e}")
        return False, f"Ошибка запуска: {str(e)}"


def _launch_steam(game: dict) -> tuple[bool, str]:
    """Запустить через Steam."""
    steam_id = game.get("steam_id")
    if not steam_id:
        return False, "Steam App ID не указан"

    url = f"steam://rungameid/{steam_id}"
    log.info(f"Steam URL: {url}")

    if sys.platform == "win32":
        os.startfile(url)
    else:
        subprocess.Popen(["xdg-open", url])

    return True, f"🚀 Запускаю через Steam..."


def _launch_epic(game: dict) -> tuple[bool, str]:
    """Запустить через Epic Games Launcher."""
    epic_id = game.get("epic_id", "")

    if epic_id:
        url = f"com.epicgames.launcher://apps/{epic_id}?action=launch"
    else:
        url = "com.epicgames.launcher://"

    log.info(f"Epic URL: {url}")

    if sys.platform == "win32":
        os.startfile(url)
    else:
        subprocess.Popen(["xdg-open", url])

    return True, f"🚀 Запускаю через Epic Games..."


def _launch_battlenet(game: dict) -> tuple[bool, str]:
    """Запустить через Battle.net."""
    product = game.get("battlenet_product", "")
    url = f"battlenet://{product}" if product else "battlenet://"

    if sys.platform == "win32":
        os.startfile(url)
    else:
        subprocess.Popen(["xdg-open", url])

    return True, f"🚀 Запускаю через Battle.net..."


def _launch_riot(game: dict) -> tuple[bool, str]:
    """Запустить через Riot Client."""
    # Riot Games требует запуска через RiotClientServices
    riot_paths = [
        r"C:\Riot Games\Riot Client\RiotClientServices.exe",
        os.path.expandvars(r"%PROGRAMFILES%\Riot Games\Riot Client\RiotClientServices.exe"),
    ]

    product = game.get("riot_product", "valorant")

    for path in riot_paths:
        if os.path.exists(path):
            subprocess.Popen([path, f"--launch-product={product}", "--launch-patchline=live"])
            return True, f"🚀 Запускаю через Riot Client..."

    return False, "Riot Client не найден. Установи его с официального сайта."


def _launch_wargaming(game: dict) -> tuple[bool, str]:
    """Запустить через Wargaming Game Center."""
    wgc_paths = [
        r"C:\Games\World_of_Tanks\WoTLauncher.exe",
        os.path.expandvars(r"%PROGRAMFILES(X86)%\World_of_Tanks\WoTLauncher.exe"),
    ]

    for path in wgc_paths:
        if os.path.exists(path):
            subprocess.Popen([path])
            return True, f"🚀 Запускаю через Wargaming Game Center..."

    # Запасной вариант — через URL
    try:
        os.startfile("wotgameclient://")
        return True, f"🚀 Запускаю через Wargaming Game Center..."
    except Exception:
        return False, "Wargaming Game Center не найден."


def _launch_exe(game: dict) -> tuple[bool, str]:
    """Запустить напрямую через EXE."""
    exe_path = game.get("exe_path", "")
    if not exe_path or not os.path.exists(exe_path):
        return False, f"Исполняемый файл не найден: {exe_path}"

    subprocess.Popen([exe_path], cwd=os.path.dirname(exe_path))
    return True, f"🚀 Запускаю напрямую..."
