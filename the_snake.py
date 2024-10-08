from random import randrange

import pygame as pg

from sys import exit

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Стартовая позиция
DEFAULT_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 150, 255)

# Цвет границы ячейки
BORDER_COLOR = (50, 50, 50)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет ёжика
HEDGEHOG_COLOR = (255, 255, 100)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Snake')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс родитель с общими аргументами и методами."""

    def __init__(self, position=DEFAULT_POSITION, body_color=BOARD_BACKGROUND_COLOR) -> None:
        """"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заглушка, будет переопределен в дочерних классах"""
        raise NotImplementedError


class Apple(GameObject):
    """
    Дочерний класс Яблоко.

    Если голова Змейки попадет на ячейку с
    Яблоком,то ее длина вырастет на 1.
    randomize_position -- выбирает случайную ячейку для спавна
    draw -- переопределенный метод, отрисовывающий Яблоко
    """

    def __init__(self, occupied_positions=DEFAULT_POSITION, body_color=APPLE_COLOR):
        """"""
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=DEFAULT_POSITION):
        """Выбирает случайную ячейку для появления Яблока."""
        if occupied_positions is None:
            occupied_positions = []
        while True:
            position = (randrange(0, GRID_WIDTH) * GRID_SIZE), (
                randrange(0, GRID_HEIGHT) * GRID_SIZE)
            if position not in occupied_positions:
                self.position = position
                break

    def draw(self):
        """Метод отрисовывающий Яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Hedgehog(GameObject):
    """
    Дочерний класс Ёжик.

    Если голова Змейки попадет на ячейку с
    Ёжиком,то ее длина уменьшится на 1.
    randomize_position -- выбирает случайную ячейку для спавна
    draw -- переопределенный метод, отрисовывающий Ёжика
    """

    def __init__(self, occupied_positions=DEFAULT_POSITION, body_color=HEDGEHOG_COLOR):
        """"""
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=DEFAULT_POSITION):
        """Выбирает случайную ячейку для появления Ёжика."""
        if occupied_positions is None:
            occupied_positions = []
        while True:
            position = (randrange(0, GRID_WIDTH) * GRID_SIZE), (
                randrange(0, GRID_HEIGHT) * GRID_SIZE)
            if position not in occupied_positions:
                self.position = position
                break

    def draw(self):
        """Метод отрисовывающий Ёжика на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Дочерний класс Змейка, предвигается по игровому полю.

    update_direction -- метод обновления направления после нажатия на кнопку
    move -- метод, отвечающий за перемещение Змейки
    draw -- метод отрисовывающий Змейку на экране
    get_head_position -- позиция первого элемента (головы) Змейки
    reset -- функция отвечающая за начало новой партии
    """

    def __init__(self, body_color=SNAKE_COLOR):
        """"""
        super().__init__(body_color=body_color)
        self.reset()

    def update_direction(self, next_direction):
        """Метод обновления направления после нажатия на кнопку."""
        if next_direction:
            self.direction = next_direction
            self.next_direction = None

    def move(self):
        """Перемещение Змейки."""
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH, (
            head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT)
        # Добавляет новую голову
        self.positions.insert(0, new_head)
        # Убирает последний элемент, если не съедено яблоко
        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        """Позиция первого элемента (головы) Змейки."""
        return self.positions[0]

    def draw(self):
        """Метод отрисовывающий Змейку на экране."""
        for position in self.positions:
            head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, head_rect)
            pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """
        Метод, отвечающий за начало новой
        партии при окончании предыдущей.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                exit(0)


def main():
    """Логика игры."""
    pg.init()
    # Экземпляры классов
    snake = Snake()
    apple = Apple(snake.positions)
    hedgehog = Hedgehog(snake.positions)
    #  screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        # Увеличение скорости в зависимости от длины змеи
        speed = SPEED + len(snake.positions) // 5
        clock.tick(speed)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() == hedgehog.position:
            snake.length -= 1
            snake.positions.pop()
            if len(snake.positions) == 0:
                snake.reset()
                apple.randomize_position()
            hedgehog.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            hedgehog.randomize_position()
        snake.draw()
        apple.draw()
        hedgehog.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
