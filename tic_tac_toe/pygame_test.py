# Импортировать библиотеку Pygame.
import pygame

# Инициализировать библиотеку Pygame.
pygame.init()

# Создать окно размером 800x600 точек (или пикселей).
screen = pygame.display.set_mode((800, 600))
# Задать окну заголовок.
pygame.display.set_caption('Пример графического окна Pygame')


running = True

# Описание главного цикла игры.
# Этот цикл работает до тех пор, пока пользователь не закроет окно.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


# Деинициализирует все модули pygame, которые были инициализированы ранее.
pygame.quit()