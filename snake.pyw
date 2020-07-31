import pygame
from random import randint

pygame.init()

class Snake:

    def __init__(self, color: tuple, surface: pygame.Surface):
        
        self.color = color
        self.surface = surface
        self.delayCounter = 0

        self.elements = [
                            [SquareMapping.toCoords(3),SquareMapping.toCoords(4)],
                            [SquareMapping.toCoords(4),SquareMapping.toCoords(4)],
                            [SquareMapping.toCoords(5),SquareMapping.toCoords(4)],
                        ]

        self.see = 'down'
        
    def draw(self):
        
        for el in self.elements:

            pygame.draw.rect(self.surface, self.color, [el[0], el[1], 10, 10])

    
    def update(self):

        self.checkCollide()

        if self.delayCounter >= 3:

            self.goto()

            self.delayCounter = 0

        if self.elements[0][0] > 490:
            self.elements[0][0] = 0

        if self.elements[0][0] < 0:
            self.elements[0][0] = 490

        if self.elements[0][1] > 490:
            self.elements[0][1] = 0

        if self.elements[0][1] < 0:
            self.elements[0][1] = 490

        self.delayCounter += 1

    def checkCollide(self):

        for el in self.elements:
            
            if self.elements.count(el) >= 2 and self.elements[-1] != el:

                exit()

    def goto(self):

        if self.see == 'right':

            del self.elements[-1]
            self.elements.insert(0, [self.elements[0][0] + 10, self.elements[0][1]])

        elif self.see == 'left':

            del self.elements[-1]
            self.elements.insert(0, [self.elements[0][0] - 10, self.elements[0][1]])

        elif self.see == 'up':

            del self.elements[-1]
            self.elements.insert(0, [self.elements[0][0], self.elements[0][1] - 10])

        elif self.see == 'down':

            del self.elements[-1]
            self.elements.insert(0, [self.elements[0][0], self.elements[0][1] + 10])

class SquareMapping:

    @staticmethod
    def toSquare(pos: int):
        return round(pos // 10)

    @staticmethod
    def toCoords(square: int):
        return square * 10

class Apple:

    def __init__(self, color: tuple, snake: Snake, surface: pygame.Surface):

        self.color = color
        self.surface = surface
        self.snake = snake

        self.respawn()

    def respawn(self):

        self.coords = [SquareMapping.toCoords(randint(1, 49)), SquareMapping.toCoords(randint(1, 49))]

    def update(self):

        self.checkSnake()

    def checkSnake(self):
        
        if self.coords == self.snake.elements[0]:

            self.snake.elements.append([self.snake.elements[-1][0], self.snake.elements[-1][1]])
            self.respawn()

    def draw(self):
        
        pygame.draw.rect(self.surface, self.color, [self.coords[0], self.coords[1], 10, 10])

class Main:

    def __init__(self, FPS):
        
        self.screen = pygame.display.set_mode((500,500))
        pygame.display.set_caption('Snake!')

        self.Clock = pygame.time.Clock()
        self.FPS = FPS
        self.GAME = True

        self.snake = Snake((0,255,0), self.screen)
        
        self.apple = Apple((255, 0, 0), self.snake, self.screen)

        while self.GAME:

            # Место обновления
            self.snake.update()
            self.apple.update()
            # Место отрисовки
            self.screen.fill((0,0,0))
            self.snake.draw()
            self.apple.draw()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.GAME = False

                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_UP and self.snake.see != 'down':
                        self.snake.see = 'up'

                    elif event.key == pygame.K_DOWN and self.snake.see != 'up':
                        self.snake.see = 'down'

                    elif event.key == pygame.K_LEFT and self.snake.see != 'right':
                        self.snake.see = 'left'

                    elif event.key == pygame.K_RIGHT and self.snake.see != 'left':
                        self.snake.see = 'right'

            pygame.display.update()

            self.Clock.tick(self.FPS)

Main(30)