import pygame
from random import choice

pygame.init()

class Map:

    def __init__(self, fill_color: tuple, stripes_color: tuple, surface: pygame.Surface):
 
        self.fill_color = fill_color
        self.stripes_color = stripes_color

        self.surface = surface
        self.surface_width = self.surface.get_width()
        self.surface_height = self.surface.get_height()
        self.surface_center = self.surface.get_width() // 2
    
    def draw(self):

        self.fill()
        self.draw_strips()

    def draw_strips(self):

        temp = 0
        section_length = 30

        for section in range(self.surface_height // section_length + 1):

            if temp % 2 == 0:

                pygame.draw.line(self.surface, self.stripes_color, [self.surface_center, section * section_length], [self.surface_center, section * section_length + section_length], 5)

            temp += 1

    def fill(self):

        self.surface.fill(self.fill_color)

class Rocket:

    def __init__(self, color: tuple, right: bool, surface: pygame.Surface, size: dict):

        self.color = color
        self.right = right
        
        self.surface = surface
        self.surface_width = self.surface.get_width()
        self.surface_height = self.surface.get_height()

        self.height = size['height']
        self.width = size['width']

        self.speed = 5

        if not self.right:
            self.x = 0
        else:
            self.x = self.surface_width - self.width

        self.y = None

        self.respawn()

    def respawn(self):
        
        self.y = self.surface_height // 2 - self.height // 2

    def check_pressed(self):

        keys = pygame.key.get_pressed()

        if not self.right:

            if keys[pygame.K_w]:
                self.go_to_up()

            if keys[pygame.K_s]:
                self.go_to_down()

        elif self.right:

            if keys[pygame.K_UP]:
                self.go_to_up()

            if keys[pygame.K_DOWN]:
                self.go_to_down()

    def update(self):
        self.check_pressed()

    def draw(self):

        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))

    def go_to_down(self):
        
        if self.y + self.height < self.surface_height:

            self.y += self.speed

    def go_to_up(self):
    
        if self.y > 0:

            self.y -= self.speed

class Ball:

    def __init__(self, color: tuple, radius: int, surface: pygame.Surface, left_rocket: Rocket, right_rocket: Rocket, right_scoreboard, left_scoreboard):

        self.color = color
        self.radius = radius

        self.SPEED_NUMS = [-6, -5, -4, -3, 3, 4, 5, 6]
        
        self.surface = surface

        self.left_rocket = left_rocket
        self.right_rocket = right_rocket

        self.right_scoreboard = right_scoreboard
        self.left_scoreboard = left_scoreboard

        self.surface_width = self.surface.get_width()
        self.surface_height = self.surface.get_height()

        self.respawn()
    
    def respawn(self):

        self.x = self.surface_width // 2
        self.y = self.surface_height // 2

        self.speedX = choice(self.SPEED_NUMS)
        self.speedY = choice(self.SPEED_NUMS)

    def update(self):

        self.check_borders_and_rockets()

        self.x += self.speedX
        self.y += self.speedY

    def draw(self):
        pygame.draw.circle(self.surface, self.color, [self.x, self.y], self.radius)

    def check_left_border(self):
        
        if self.x < 0 + self.radius:
            
            self.right_rocket.respawn()
            self.left_rocket.respawn()
            self.respawn()
            self.right_scoreboard.plus()
    
    def check_right_border(self):
        
        if self.x > self.surface_width - self.radius:

            self.right_rocket.respawn()
            self.left_rocket.respawn()
            self.respawn()
            self.left_scoreboard.plus()
    
    def check_up_border(self):
        
        if self.y < 0 + self.radius:
            
            self.speedY = -self.speedY

    def check_down_border(self):
              
        if self.y > self.surface_height - self.radius:
            
            self.speedY = -self.speedY

    def check_left_rocket(self):
        
        if self.y + self.radius // 2 in range(self.left_rocket.y, self.left_rocket.y + self.left_rocket.height) and self.x - self.radius < self.left_rocket.x + self.left_rocket.width:

            self.speedX = -self.speedX

    def check_right_rocket(self):

        if self.y + self.radius // 2 in range(self.right_rocket.y, self.right_rocket.y + self.right_rocket.height) and self.x + self.radius > self.right_rocket.x:
           
            self.speedX = -self.speedX

    def check_borders_and_rockets(self):

        self.check_left_rocket()
        self.check_right_rocket()

        self.check_down_border()
        self.check_left_border()
        self.check_up_border()
        self.check_right_border()

class Scoreboard:

    def __init__(self, color: tuple, position: dict, size: int, surface: pygame.Surface):

        self.color = color

        self.x = position['x']
        self.y = position['y']

        self.value = 0

        self.size = size
        self.font = pygame.font.Font(None, self.size)

        self.surface = surface

    def plus(self):
        self.value += 1

    def draw(self):
        
        to_blit = self.font.render(str(self.value), 1, self.color)

        self.surface.blit(to_blit, (self.x, self.y))

class Main:

    def __init__(self):

        self.screen = pygame.display.set_mode((1001, 501))
        pygame.display.set_caption('Ping pong!')

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.GAME = True

        self.left_scoreboard = Scoreboard((255, 255, 255), {'x': 400, 'y' : 10}, 100, self.screen)
        self.right_scoreboard = Scoreboard((255, 255, 255), {'x': 560, 'y' : 10}, 100, self.screen)
        
        self.map = Map((0, 128, 128), (255, 255, 255), self.screen)
        
        self.left_rocket = Rocket((184, 134, 11), False, self.screen, {'width' : 20, 'height' : 120})
        self.right_rocket = Rocket((184, 134, 11), True, self.screen, {'width' : 20, 'height' : 120})

        self.ball = Ball((240, 230, 140), 15, self.screen, self.left_rocket, self.right_rocket, self.right_scoreboard, self.left_scoreboard)

        while self.GAME:

            # # # Изменение объeктов # # # 
            self.ball.update()
            self.right_rocket.update()
            self.left_rocket.update()
            # # # Отрисовка объектов # # #
            self.map.draw()
            self.ball.draw()
            self.left_rocket.draw()
            self.right_rocket.draw()
            self.right_scoreboard.draw()
            self.left_scoreboard.draw()
            # # # # # # # ## # # # # # # #

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.GAME = False

            pygame.display.update()

            self.clock.tick(self.FPS)

Main()