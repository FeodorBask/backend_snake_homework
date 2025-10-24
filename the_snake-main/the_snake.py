from random import randint
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
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов"""
    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = BOARD_BACKGROUND_COLOR
    
    def draw(self):
        """Абстрактный метод для отрисовки объекта"""
        pass


class Apple(GameObject):
    """Класс для яблока - еды для змейки"""
    def __init__(self):
        super().__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR
    
    def randomize_position(self):
        """Устанавливает случайную позицию для яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
    
    def draw(self):
        """Отрисовывает яблоко на экране"""
        # Убеждаемся, что position - это кортеж с двумя числами
        if (isinstance(self.position, (tuple, list)) and 
            len(self.position) == 2 and 
            all(isinstance(coord, (int, float)) for coord in self.position)):
            
            rect = pygame.Rect(
                (int(self.position[0]), int(self.position[1])), 
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        else:
            print(f"Ошибка: некорректная позиция яблока: {self.position}")


class Snake(GameObject):
    """Класс для змейки - главного игрового объекта"""
    def __init__(self):
        super().__init__()
        # ИНИЦИАЛИЗИРУЕМ ВСЕ АТРИБУТЫ НЕПОСРЕДСТВЕННО В init
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
    
    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
    
    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        """Обновляет позицию змейки - двигает её вперед"""
        # Сохраняем последнюю позицию для затирания
        self.last = self.positions[-1] if len(self.positions) > 1 else None
        
        # Получаем текущую позицию головы
        head_x, head_y = self.positions[0]
        
        # Вычисляем новую позицию головы
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        
        # Добавляем новую голову в начало списка
        self.positions.insert(0, new_head)
        
        # Если длина не увеличилась, удаляем хвост
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]
    
    def draw(self):
        """Отрисовывает змейку на экране"""
        # Отрисовываем все сегменты тела, кроме головы
        for position in self.positions[1:]:
            if (isinstance(position, (tuple, list)) and 
                len(position) == 2 and 
                all(isinstance(coord, (int, float)) for coord in position)):
                
                rect = pygame.Rect(
                    (int(position[0]), int(position[1])), 
                    (GRID_SIZE, GRID_SIZE)
                )
                pygame.draw.rect(screen, self.body_color, rect)
                pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        
        # Отрисовываем голову змейки
        head_position = self.positions[0]
        if (isinstance(head_position, (tuple, list)) and 
            len(head_position) == 2 and 
            all(isinstance(coord, (int, float)) for coord in head_position)):
            
            head_rect = pygame.Rect(
                (int(head_position[0]), int(head_position[1])), 
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        
        # Затираем последний сегмент (если он есть)
        if self.last:
            if (isinstance(self.last, (tuple, list)) and 
                len(self.last) == 2 and 
                all(isinstance(coord, (int, float)) for coord in self.last)):
                
                last_rect = pygame.Rect(
                    (int(self.last[0]), int(self.last[1])), 
                    (GRID_SIZE, GRID_SIZE)
                )
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Главная функция игры"""
    # Инициализация PyGame:
    pygame.init()
    
    # === СОЗДАНИЕ ЭКЗЕМПЛЯРОВ КЛАССОВ ДО ЦИКЛА ===
    snake = Snake()
    apple = Apple()
    
    # Проверяем начальные позиции
    print(f"Начальная позиция змейки: {snake.positions[0]}")
    print(f"Начальная позиция яблока: {apple.position}")
    
    # === ОСНОВНОЙ ИГРОВОЙ ЦИКЛ ===
    while True:
        # Ограничение FPS
        clock.tick(SPEED)
        
        # 1. ОБРАБОТКА СОБЫТИЙ КЛАВИШ
        handle_keys(snake)
        
        # 2. ОБНОВЛЕНИЕ НАПРАВЛЕНИЯ ДВИЖЕНИЯ ЗМЕЙКИ
        snake.update_direction()
        
        # 3. ДВИЖЕНИЕ ЗМЕЙКИ (МОДИФИКАЦИЯ СПИСКА POSITIONS)
        snake.move()
        
        # 4. ПРОВЕРКА, СЪЕЛА ЛИ ЗМЕЙКА ЯБЛОКО
        if snake.get_head_position() == apple.position:
            # УВЕЛИЧЕНИЕ ДЛИНЫ ЗМЕЙКИ
            snake.length += 1
            # ПЕРЕМЕЩЕНИЕ ЯБЛОКА
            apple.randomize_position()
            # Убеждаемся, что яблоко не появляется на теле змейки
            while apple.position in snake.positions:
                apple.randomize_position()
        
        # 5. ПРОВЕРКА СТОЛКНОВЕНИЙ ЗМЕЙКИ С САМОЙ СОБОЙ
        head_position = snake.get_head_position()
        if head_position in snake.positions[1:]:
            # СБРОС ИГРЫ ПРИ СТОЛКНОВЕНИИ
            print(f"Игра окончена! Счёт: {snake.length - 1}")
            snake.reset()
        
        # 6. ОТРИСОВКА ИГРОВЫХ ОБЪЕКТОВ
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана
        snake.draw()  # Отрисовка змейки
        apple.draw()  # Отрисовка яблока
        
        # 7. ОБНОВЛЕНИЕ ЭКРАНА
        pygame.display.update()


if __name__ == '__main__':
    main()