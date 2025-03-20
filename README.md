# Игра "Змейка" с яблоками и ёжиками

Классическая игра "Змейка" с дополнительными механиками. Собирайте яблоки, избегайте ёжиков и не врезайтесь в себя!

<img src="https://raw.githubusercontent.com/Frenky19/the_snake/main/screenshot.png" width="400" alt="Скриншот игры">

## Особенности

- Управление стрелками на клавиатуре
- Случайное появление яблок (увеличивают длину) и ёжиков (уменьшают длину)
- Динамическая скорость: чем длиннее змейка, тем быстрее игра
- Автоматический перезапуск при столкновении
- Система подсчёта очков (длина змейки = счёт)
- Экран паузы перед стартом

## Технологии

- **Язык**: Python 3.7+
- **Библиотеки**: 
  - `pygame` — рендеринг графики и обработка ввода
- **Архитектура**: ООП с наследованием классов

## Установка

1. Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/frenky19/the_snake.git
```
```bash
cd the_snake
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv env
```
```bash
source env/bin/activate  # Linux
source env/scripts/activate  # Windows
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Запустить игру:

```bash
pip python the_snake.py
```

## Управление

| Клавиша         | Действие               |
|-----------------|------------------------|
| Стрелка Вверх   | Движение вверх         |
| Стрелка Вниз    | Движение вниз          |
| Стрелка Влево   | Движение влево         |
| Стрелка Вправо  | Движение вправо        |
| ESC             | Выход из игры          |

## Правила игры

- 🟢 **Змейка**  
  Автоматически движется в выбранном направлении

- 🍎 **Яблоко**:
  - Увеличивает длину на 1
  - Появляется в случайной позиции

- 🟡 **Ёжик**:
  - Уменьшает длину на 1
  - При длине 1 — игра перезапускается
  - Появляется в случайной позиции

- ☠️ **Проигрыш**:
  - Столкновение с собой
  - Длина уменьшена до 0

## Разработка

### Ключевые классы

- **`GameObject`** — базовый класс для всех объектов:
  - Отрисовка элементов
  - Управление позицией

- **`Snake`** — логика змейки:
  - Движение
  - Обработка столкновений
  - Управление длиной

- **`Apple`/`Hedgehog`** — интерактивные объекты:
  - Случайный спавн
  - Взаимодействие со змейкой

### Основные функции

- `handle_keys()` — обработка пользовательского ввода
- `waiting()` — экран паузы перед стартом
- `main()` — игровой цикл

## Возможные улучшения

- [ ] Добавить меню с настройками
- [ ] Реализовать систему рекордов
- [ ] Добавить звуковые эффекты
- [ ] Создать уровни сложности
- [ ] Реализовать мультиплеер

## Автор  
[Андрей Головушкин / Andrey Golovushkin](https://github.com/Frenky19)
