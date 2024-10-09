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

    def __init__(
        self,
        position=DEFAULT_POSITION,
        body_color=BOARD_BACKGROUND_COLOR
    ) -> None:
        """Конструктор главного класса."""
        self.position = position
        self.body_color = body_color

    def draw_base(
        self,
        screen,
        position=None,
        body_color=None,
        border_color=BORDER_COLOR
    ):
        """Метод для отрисовки ячейки на экране."""
        if position is None:
            position = self.position
        if body_color is None:
            body_color = self.body_color
        rect = pg.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Заглушка, будет переопределен в дочерних классах."""
        raise NotImplementedError


class InteactiveObject(GameObject):
    """
    Базовый класс для интерактивных объектов: Яблоко и Ёжик.

    randomize_position -- выбирает случайную ячейку для спавна
    draw -- переопределенный метод, отрисовывающий объект
    """

    def __init__(
        self,
        occupied_positions_snake=DEFAULT_POSITION,
        body_color=BOARD_BACKGROUND_COLOR
    ):
        """Конструктор классов для взаимодействия."""
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions_snake)

    def randomize_position(self, occupied_positions_snake=DEFAULT_POSITION):
        """Задает случайную ячейку для появления объекта."""
        if not occupied_positions_snake:
            occupied_positions_snake = []
        while True:
            self.position = (randrange(0, GRID_WIDTH) * GRID_SIZE), (
                randrange(0, GRID_HEIGHT) * GRID_SIZE)
            if self.position not in occupied_positions_snake:
                break

    def draw(self, screen, position, body_color):
        """Отрисовка объекта."""
        self.draw_base(screen, position, body_color)


class Apple(InteactiveObject):
    """
    Дочерний класс Яблоко.

    Если голова Змейки попадет на ячейку с
    Яблоком,то ее длина вырастет на 1.
    """

    def __init__(self, occupied_positions_snake=DEFAULT_POSITION):
        """Конструтор класса Яблоко"""
        super().__init__(occupied_positions_snake, APPLE_COLOR)


class Hedgehog(InteactiveObject):
    """
    Дочерний класс Ёжик.

    Если голова Змейки попадет на ячейку с
    Ёжиком,то ее длина уменьшится на 1.
    randomize_position -- выбирает случайную ячейку
    """

    def __init__(
        self,
        occupied_positions_snake=DEFAULT_POSITION,
        occupied_positions_apple=None
    ):
        """Конструктор класса Ёжик"""
        super().__init__(occupied_positions_snake, HEDGEHOG_COLOR)
        self.randomize_position(
            occupied_positions_snake,
            occupied_positions_apple
        )

    def randomize_position(
        self,
        occupied_positions_snake=DEFAULT_POSITION,
        occupied_positions_apple=None
    ):
        """Метод, выбирающий свободную от Змейки и Яблока позицию ячейку"""
        if not occupied_positions_snake:
            occupied_positions_snake = []
        while True:
            self.position = (
                randrange(0, GRID_WIDTH) * GRID_SIZE,
                randrange(0, GRID_HEIGHT) * GRID_SIZE
            )
            if (self.position not in occupied_positions_snake
               and self.position != occupied_positions_apple):
                break


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
        """Конструктор класса Змейка."""
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

    def get_tail_position(self):
        """Позиция последнего элемента (хвоста) Змейки"""
        return self.positions[-1]

    def draw(self):
        """Метод отрисовывающий Змейку на экране."""
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        tail_rect = pg.Rect(self.get_tail_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, tail_rect)
        pg.draw.rect(screen, BORDER_COLOR, tail_rect, 1)

    def reset(self):
        """
        Метод, отвечающий за начало новой
        партии при окончании предыдущей.
        """
        screen.fill(BOARD_BACKGROUND_COLOR)
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
    hedgehog = Hedgehog(snake.positions, apple.position)
    # Создаем фон
    screen.fill(BOARD_BACKGROUND_COLOR)
    # Бесконечный цикл
    while True:
        # Увеличение скорости в зависимости от длины змеи
        speed = SPEED + len(snake.positions) // 5
        clock.tick(speed)
        handle_keys(snake)
        # Запоминаем последнее значение "хвоста"
        last_position = snake.positions[-1]
        snake.move()
        # Затираем ячейку в цвет фона после движения Змейки
        if last_position:
            pg.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                pg.Rect(last_position[0], last_position[1],
                        GRID_SIZE, GRID_SIZE)
            )
        # Проверка на столкновение с Яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        # Проверка на стокновение с Ёжиком
        if snake.get_head_position() == hedgehog.position:
            snake.length -= 1
            if snake.positions:
                last_position = snake.positions.pop()
                # Затирка ячейки, где находился Ёжик
                pg.draw.rect(
                    screen,
                    BOARD_BACKGROUND_COLOR,
                    pg.Rect(last_position[0], last_position[1],
                            GRID_SIZE, GRID_SIZE)
                )
            if len(snake.positions) == 0:
                snake.reset()
                apple.randomize_position(snake.positions)
            hedgehog.randomize_position(snake.positions, apple.position)
        # Проверка на стокновение самой с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            hedgehog.randomize_position(snake.positions, apple.position)
        snake.draw()
        apple.draw(screen, position=apple.position, body_color=APPLE_COLOR)
        hedgehog.draw(
            screen,
            position=hedgehog.position,
            body_color=HEDGEHOG_COLOR
        )
        pg.display.update()


if __name__ == '__main__':
    main()
