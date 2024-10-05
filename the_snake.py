from random import randrange

import pygame

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 150, 255)

# Цвет границы ячейки
BORDER_COLOR = (50, 50, 50)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвета ёжика
HEDGEHOG_COLOR = (255, 255, 100)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Snake')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс родитель с общими аргументами и методами."""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Заглушка."""
        pass


class Apple(GameObject):
    """
    Дочерний класс Яблоко, съев которое,
    длина Змейки вырастет на 1 ячейку.
    """

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Выбирает случайную ячейку для появления Яблока."""
        self.position = (randrange(0, GRID_WIDTH) * GRID_SIZE), (
            randrange(0, GRID_HEIGHT) * GRID_SIZE)

    def draw(self):
        """Метод отрисовывающий Яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Hedgehog(GameObject):
    """
    Дочерний класс Ёжик, попав на которого
    длина Змейки уменьшится на 1 ячейку.
    """

    def __init__(self):
        super().__init__()
        self.body_color = HEDGEHOG_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Выбирает случайную ячейку для появления Ёжика."""
        self.position = (randrange(0, GRID_WIDTH) * GRID_SIZE), (
            randrange(0, GRID_HEIGHT) * GRID_SIZE)

    def draw(self):
        """Метод отрисовывающий Ёжика на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс Змейка, предвигается по игровому полю."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещение Змейки."""
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH, (
            head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT)
        # Добавляет новую голову
        self.positions.insert(0, new_head)
        # Убирает последний элемент, если не съедено яблоко"""
        if len(self.positions) > self.length:
            self.positions.pop()

    def check_eat_apple(self, apple):
        """Провека на съеденное Яблоко."""
        if self.positions[0] == apple.position:
            self.length += 1
            apple.position = (randrange(0, GRID_WIDTH) * GRID_SIZE), (
                randrange(0, GRID_HEIGHT) * GRID_SIZE)

    def check_meet_hedgehog(self, hedgehog):
        """Провека на встреченного Ёжика."""
        if self.positions[0] == hedgehog.position:
            self.length -= 1
            self.positions.pop()
            if len(self.positions) == 0:
                self.reset()
            hedgehog.position = (randrange(0, GRID_WIDTH) * GRID_SIZE), (
                randrange(0, GRID_HEIGHT) * GRID_SIZE)

    def check_eaten_by_herself(self):
        """Проверка на столкновение Змейки с самой собой."""
        return self.positions[0] in self.positions[1:]

    def draw(self):
        """Метод отрисовывающий Змейку на экране."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Позиция первого элемента (головы) Змейки."""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def reset(self):
        """
        Функция отвечающая за начало новой
        партии при окончании предыдущей.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Логика игры."""
    pygame.init()
    # Экземпляры классов
    apple = Apple()
    snake = Snake()
    hedgehog = Hedgehog()
    while True:
        # Увеличение скорости в зависимости от длины змеи
        speed = SPEED + len(snake.positions) // 5
        clock.tick(speed)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.check_eat_apple(apple)
        snake.check_meet_hedgehog(hedgehog)
        if snake.check_eaten_by_herself():
            snake.reset()
        apple.draw()
        hedgehog.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
