# 🎮 GameOptimizer AI ✨
### *Твой тёплый Pixar-друг для максимального FPS*

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Style](https://img.shields.io/badge/Style-Pixar%202026-pink?style=for-the-badge)

**«Я краснею от умилства» — вот что чувствуешь, запуская GameOptimizer AI** 🌸

</div>

---

## 💫 О проекте

**GameOptimizer AI** — это не просто оптимизатор игр. Это твой личный Pixar-друг, который:
- 🤗 Знает тебя по имени и заботится о тебе
- 🎯 Подбирает оптимизации **персонально под твоё железо**
- 🛡️ Никогда не трогает античит и не банит аккаунты
- 🚀 Реально поднимает FPS на 15–60%
- 💬 Болтает с тобой как настоящий Pixar-персонаж

Дизайн вдохновлён фильмами **Pixar 2026** (Soul, Inside Out 2, Elemental) — мягкий тёплый свет, округлые формы, нежные цвета и ощущение заботы и радости.

---

## 🎮 Поддерживаемые игры

| Игра | Категории оптимизации |
|------|----------------------|
| 🔴 Cyberpunk 2077 | Графика, Производительность, RTX, Стабильность |
| 🟡 GTA V | FPS, Память, Онлайн-стабильность |
| 🔵 Fortnite | Конкурентный FPS, Задержка, Визуал |
| 🟣 Valorant | Про-настройки, Минимальный пинг |
| ⚔️ Elden Ring | Стабильность, Устранение фризов |
| 🟤 Rust | Серверная оптимизация, Память |
| 🩸 Dead by Daylight | FPS, Анти-фриз |
| 🪖 World of Tanks | Графика, Пинг |
| 🟠 PUBG | Конкурентные настройки |
| ✈️ War Thunder | FPS, Стабильность |
| 🟢 Counter-Strike 2 | Про-FPS, Минимальный инпут-лаг |

---

## 🚀 Быстрый старт

### Требования
- Python 3.11+
- Windows 10/11 (рекомендуется)
- NVIDIA GPU (опционально, для NVIDIA-функций)

### Установка

```bash
# 1. Клонируй репозиторий
git clone https://github.com/yourusername/GameOptimizerAI.git
cd GameOptimizerAI

# 2. Создай виртуальное окружение (рекомендуется)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Установи зависимости
pip install -r requirements.txt

# 4. Запусти!
python main.py
```

### Первый запуск
При первом запуске появится тёплое приветствие от AI-друга:
> *"Привет! Я так рада тебя видеть! 💕 Давай познакомимся — как тебя зовут?"*

Введи своё имя и начни путешествие! ✨

---

## 🧠 Умный запуск игр

GameOptimizer AI автоматически определяет, через какой лаунчер нужно запустить игру:

| Лаунчер | Поддержка |
|---------|-----------|
| Steam | ✅ `steam://rungameid/{appid}` |
| Epic Games | ✅ `com.epicgames.launcher://` |
| Battle.net | ✅ `battlenet://` |
| Прямой EXE | ✅ Обнаружение пути |

**Почему это важно:** Запуск через правильный лаунчер гарантирует корректную работу античита (EAC, BattlEye, Vanguard и т.д.) и предотвращает блокировки аккаунта.

---

## 🧹 Безопасная очистка паразитов

Оптимизатор закрывает **только безопасные** фоновые процессы:

### ✅ Безопасно закрываем:
- Discord Overlay
- GeForce Experience
- MSI Afterburner (оверлей)
- RGB-программы (iCUE, Aura Sync, etc.)
- Неиспользуемые браузеры
- Torrent-клиенты

### 🛡️ НИКОГДА не трогаем (защищённый список):
- `EasyAntiCheat.exe`
- `BEService.exe` (BattlEye)
- `vgc.exe` (Vanguard)
- `Steam.exe`
- `EpicGamesLauncher.exe`
- Системные процессы Windows

---

## 🎨 Pixar-стиль дизайна

Приложение создано в стиле **«я краснею»** — тёплый уютный Pixar 2026:

- 🌙 **Тёмная основа** — комфортно для ночного гейминга
- ✨ **Мягкие светящиеся акценты** — бирюзовый, тёплый оранжевый, нежный розовый
- 🎭 **Анимации с душой** — плавные, живые, как в Pixar-фильме
- 💬 **AI-друг с характером** — заботливый, игривый, поддерживающий

---

## 🤖 AI-друг (Pixar Personality)

AI-друг обладает настоящим характером:
- Знает твоё имя и всегда обращается к тебе лично
- Поддерживает в трудных игровых моментах
- Радуется твоим успехам
- Рассказывает анекдоты про игры
- Мотивирует и вдохновляет

> Система построена на правилах (rule-based), но архитектура готова к подключению реального LLM (OpenAI / Anthropic API).

---

## 🔧 Как добавить новую игру

1. Открой `data/games_data.py`
2. Добавь новый словарь в список `GAMES_DATA`:

```python
{
    "id": "my_new_game",
    "name": "Название игры",
    "emoji": "🎮",
    "launcher": "steam",  # steam / epic / battlenet / exe
    "steam_id": 123456,   # если Steam
    "color": "#FF6B6B",
    "optimizations": [
        {
            "id": "opt_1",
            "title": "Название оптимизации",
            "description": "Описание что делает и почему помогает",
            "category": "Графика",  # Графика / Производительность / Стабильность / Очистка / NVIDIA
            "fps_gain": {"low": 5, "mid": 12, "high": 8},  # по тиру ПК
            "safe_for_anticheat": True,
            "image_before": "assets/images/before_default.png",
            "image_after": "assets/images/after_default.png",
        }
    ]
}
```

3. Перезапусти приложение — игра появится автоматически! 🎉

---

## 📁 Структура проекта

```
GameOptimizerAI/
├── main.py                    # Точка входа
├── requirements.txt
├── README.md
├── assets/
│   └── images/               # Иконки и изображения
├── core/
│   ├── pc_detector.py         # Определение железа
│   ├── optimizer_engine.py    # Движок оптимизации
│   ├── launcher.py            # Умный запуск игр
│   └── parasite_cleaner.py    # Безопасная очистка
├── ui/
│   ├── app.py                 # Главное окно
│   ├── game_card.py           # Карточка игры
│   ├── game_window.py         # Окно оптимизации игры
│   ├── ai_friend.py           # AI-чат друг
│   ├── widgets.py             # Кастомные виджеты
│   └── theme.py               # Pixar-тема и стили
├── data/
│   └── games_data.py          # База данных игр и оптимизаций
└── utils/
    ├── settings.py            # Настройки и сохранение
    └── logger.py              # Логирование
```

---

## ⚠️ Важные предупреждения

- **NVIDIA-функции** работают только с официальными драйверами NVIDIA
- **Реестр Windows**: некоторые оптимизации изменяют реестр — создаётся резервная копия
- **Администратор**: для некоторых оптимизаций требуются права администратора
- **Античит**: мы никогда не трогаем процессы античита — аккаунт в безопасности

---

## 📜 Лицензия

MIT License — используй, модифицируй, делись! 💕

---

<div align="center">

*Сделано с любовью и щепоткой Pixar-магии* ✨

**Приятной игры!** 🎮💕

</div>
