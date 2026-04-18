<div align="center">

# 🎮 GameOptimizer AI ✨
### *Твой тёплый Pixar-друг для максимального FPS*

[![Build](https://github.com/YOUR_USERNAME/GameOptimizerAI/actions/workflows/build.yml/badge.svg)](https://github.com/YOUR_USERNAME/GameOptimizerAI/actions/workflows/build.yml)
[![Release](https://img.shields.io/github/v/release/YOUR_USERNAME/GameOptimizerAI?style=flat-square&color=00D4C8)](https://github.com/YOUR_USERNAME/GameOptimizerAI/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**«Я краснею от умилства» — вот что чувствуешь, запуская GameOptimizer AI** 🌸

</div>

---

## ⚡ Быстрая установка

### 🪟 Windows — просто скачай и запусти
> Ничего устанавливать не нужно!

**[⬇️ Скачать GameOptimizerAI.exe](https://github.com/YOUR_USERNAME/GameOptimizerAI/releases/latest)**

1. Скачай `.zip` из [Releases](https://github.com/YOUR_USERNAME/GameOptimizerAI/releases/latest)
2. Распакуй
3. Запусти `GameOptimizerAI.exe` — готово! ✨

### 🐍 Из исходников (любая ОС)
```bash
git clone https://github.com/YOUR_USERNAME/GameOptimizerAI.git
cd GameOptimizerAI
pip install -r requirements.txt
python main.py
```

---

## 💫 О проекте

**GameOptimizer AI** — это не просто оптимизатор игр. Это твой личный Pixar-друг, который:
- 🤗 Знает тебя по имени и заботится о тебе
- 🎯 Подбирает оптимизации **персонально под твоё железо**
- 🛡️ Никогда не трогает античит — аккаунты в безопасности
- 🚀 Реально поднимает FPS на 15–60%
- 💬 Болтает как настоящий Pixar-персонаж

Дизайн вдохновлён **Pixar 2026** (Soul, Inside Out 2, Elemental) — мягкое тёплое свечение, округлые формы, нежные цвета.

---

## 🎮 Поддерживаемые игры

| Игра | Оптимизаций | Категории |
|------|------------|-----------|
| 🔴 Cyberpunk 2077 | 13 | Графика, FPS, Стабильность, NVIDIA |
| 🟡 GTA V | 10 | Графика, FPS, Память |
| 🔵 Fortnite | 9 | Конкурентный FPS, Задержка |
| 🟣 Valorant | 8 | Про-настройки, Античит |
| ⚔️ Elden Ring | 7 | Стабильность, Фризы |
| 🟤 Rust | 7 | Серверная оптимизация |
| 🩸 Dead by Daylight | 6 | FPS, Анти-фриз |
| 🪖 World of Tanks | 6 | Графика, Пинг |
| 🟠 PUBG | 6 | Конкурентные настройки |
| ✈️ War Thunder | 6 | FPS, Онлайн |
| 🟢 Counter-Strike 2 | 10 | Про-FPS, NVIDIA, Инпут-лаг |

**Итого: 88 оптимизаций** персонально подобранных под твоё железо

---

## 🤖 AI-друг Лuma

При первом запуске Лuma познакомится с тобой:
> *"Привет! Я Лuma — твой личный игровой друг 💕 Как тебя зовут?"*

Лuma знает твоё имя, поддерживает в трудных матчах, радуется победам и рассказывает анекдоты про игры.

---

## 🛡️ Безопасность (античит)

**НИКОГДА не трогаем:**
`EasyAntiCheat` · `BattlEye` · `Vanguard` · `Steam` · `EpicGamesLauncher` · `FaceIT`

**Безопасно закрываем:**
`Discord Overlay` · `GeForce Experience` · `RGB-программы` · `iCUE` · `Aura Sync`

---

## 🏗️ Для разработчиков

### Структура проекта
```
GameOptimizerAI/
├── main.py                    # Точка входа
├── requirements.txt
├── GameOptimizerAI.spec       # PyInstaller конфиг
├── .github/workflows/
│   └── build.yml              # Auto-build → .exe на GitHub
├── core/
│   ├── pc_detector.py         # CPU/GPU/RAM → тир ПК
│   ├── optimizer_engine.py    # Движок оптимизации
│   ├── launcher.py            # Steam/Epic/Riot/Wargaming
│   ├── ai_friend.py           # Pixar AI-характер
│   └── parasite_cleaner.py    # Безопасная очистка
├── ui/
│   ├── app.py                 # Главное окно + SplashScreen
│   ├── game_card.py           # Карточки игр
│   ├── game_window.py         # Окно оптимизации
│   ├── ai_friend.py           # Панель чата
│   ├── widgets.py             # Кастомные виджеты
│   └── theme.py               # Pixar-тема и цвета
├── data/
│   └── games_data.py          # База игр и оптимизаций
└── utils/
    ├── settings.py            # Сохранение настроек
    └── logger.py              # Логирование
```

### Добавить новую игру
Открой `data/games_data.py` и добавь словарь:
```python
{
    "id": "my_game",
    "name": "Название",
    "emoji": "🎮",
    "launcher": "steam",
    "steam_id": 123456,
    "color": "#FF6B6B",
    "description": "Слоган",
    "optimizations": [
        {
            "id": "opt_1",
            "title": "Название оптимизации",
            "description": "Что делает и почему помогает",
            "category": "Графика",  # или Производительность / Стабильность / Очистка / NVIDIA
            "fps_gain": {"low": 10, "mid": 6, "high": 2},
            "safe_for_anticheat": True,
        }
    ]
}
```

### Собрать .exe локально
```bash
pip install pyinstaller
pyinstaller GameOptimizerAI.spec --clean
# Результат: dist/GameOptimizerAI.exe
```

### Выпустить новый релиз
```bash
git tag v1.1
git push origin v1.1
# GitHub Actions автоматически соберёт .exe и создаст Release!
```

---

## 📜 Лицензия

MIT — используй, модифицируй, делись! 💕

---

<div align="center">

*Сделано с любовью и щепоткой Pixar-магии* ✨  
**Приятной игры!** 🎮💕

</div>
