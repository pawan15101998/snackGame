import pygame
import time
import random
from pygame.locals import *


size = 40
background_color = (110, 110, 5)


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/block.jpeg").convert()
        self.image = pygame.transform.scale(self.image,(40,40))
        self.parent_screen = parent_screen
        self.x = size*3
        self.y = size*3
    
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    
    def move(self):
        self.x = random.randint(0, 24)*size
        self.y = random.randint(0, 19)*size



class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpeg").convert()
        self.block = pygame.transform.scale(self.block,(40,40))
        self.block_x = [size]*length
        self.block_y = [size]*length
        self.direction = 'down'

    def draw(self):
        # self.parent_screen.fill(background_color)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.block_x[i], self.block_y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length +=1
        self.block_x.append(-1)
        self.block_y.append(-1)
        
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]
        if self.direction == 'down':
            self.block_y[0] += size
        if self.direction == 'up':
            self.block_y[0] -= size
        if self.direction == 'left':
            self.block_x[0] -= size
        if self.direction == 'right':
            self.block_x[0] += size

        self.draw()



        
class Game:
    def __init__(self):
        pygame.init()
        self.play_background_music()
        pygame.display.set_caption("Snake and Apple game")
        pygame.mixer.init()
        self.surface  = pygame.display.set_mode((1000, 800))
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()


    def play_background_music(self):
        pygame.mixer.music.load("resources/bg.mp3")
        pygame.mixer.music.play()

    def playSound(self, sound):
        sound = pygame.mixer.Sound(sound)
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/images.jpeg")
        bg = pygame.transform.scale(bg,(1000,800))
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        # Snake colliding with apple
        if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.apple.x, self.apple.y):
            self.playSound("resources/ding.mp3")
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]) :
                self.playSound("resources/crash.mp3")
                raise "game over"

        
    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.render_background()
        # self.surface.fill(background_color)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 =font.render("To play again press enter. To exit press escape", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 7)
        self.apple = Apple(self.apple)


    def run(self):
            running = True
            pause = False
            while running:
                for event in pygame.event.get():
                  if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                                self.snake.move_up()
                        if event.key == K_DOWN:
                                self.snake.move_down()
                        if event.key == K_LEFT:
                                self.snake.move_left()
                        if event.key == K_RIGHT:
                                self.snake.move_right()
                    elif event.type ==  QUIT:
                        running = False
                try:   
                 if not pause:
                  self.play()
                except Exception as e:
                    self.show_game_over()
                    pause = True
                    self.reset()
                time.sleep(0.3)
    
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 +size:
                return True
        
        return False




if __name__ == '__main__':

    game = Game()
    game.run()

    # pygame.display.flip()

