import pygame
import time
import random

# initialize
pygame.init()

# constants
WIDTH =   800
HEIGHT =   600
FPS =   10  #slow snake

# colors
WHITE = (255,   255,   255)
GREEN = (0,   255,   0)
RED = (255,   0,   0)
BLACK = (0,   0,   0) 

# game window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# set up the clock
clock = pygame.time.Clock()

# font setup
SCORE_FONT = pygame.font.SysFont('times new roman',  20)

class Snake:
    def __init__(self):
        self.size =   3
        self.elements = [[100,   50], [90,   50], [80,   50]]
        self.direction = 'RIGHT'

    def change_direction(self, new_direction):
        if (new_direction == 'UP' and self.direction != 'DOWN') or \
           (new_direction == 'DOWN' and self.direction != 'UP') or \
           (new_direction == 'LEFT' and self.direction != 'RIGHT') or \
           (new_direction == 'RIGHT' and self.direction != 'LEFT'):
            self.direction = new_direction

    def move(self):
        if self.direction == 'UP':
            new_head = [self.elements[-1][0], self.elements[-1][1] -   20]
        elif self.direction == 'DOWN':
            new_head = [self.elements[-1][0], self.elements[-1][1] +   20]
        elif self.direction == 'LEFT':
            new_head = [self.elements[-1][0] -   20, self.elements[-1][1]]
        elif self.direction == 'RIGHT':
            new_head = [self.elements[-1][0] +   20, self.elements[-1][1]]

        if new_head[0] <  0:
            new_head[0] = WIDTH
        elif new_head[0] >= WIDTH:
            new_head[0] =  0
        if new_head[1] <  0:
            new_head[1] = HEIGHT
        elif new_head[1] >= HEIGHT:
            new_head[1] =  0

        self.elements.append(new_head)
        if len(self.elements) > self.size:
            del self.elements[0]

    def grow(self):
        self.size +=   1

    def collides_with_itself(self):
        return self.elements[0] in self.elements[1:]

    def collides_with_apple(self, apple):
        return self.elements[0] == apple.position

class Apple:
    def __init__(self):
        self.position = [random.randrange(1, WIDTH//20) *   20, random.randrange(1, HEIGHT//20) *   20]

    def randomize_position(self):
        self.position = [random.randrange(1, WIDTH//20) *   20, random.randrange(1, HEIGHT//20) *   20]

def game_over():
    font = pygame.font.SysFont('times new roman',   50)
    game_over_surface = font.render('GAME OVER', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (WIDTH /   2, HEIGHT /   4)
    WINDOW.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

def main():
    snake1 = Snake()
    snake2 = Snake()
    apple = Apple()
    score1 = score2 =  0

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # input for both players
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            snake1.change_direction('UP')
        if keys[pygame.K_s]:
            snake1.change_direction('DOWN')
        if keys[pygame.K_a]:
            snake1.change_direction('LEFT')
        if keys[pygame.K_d]:
            snake1.change_direction('RIGHT')

        # assuming the second player uses the arrow keys for movement
        if keys[pygame.K_UP]:
            snake2.change_direction('UP')
        if keys[pygame.K_DOWN]:
            snake2.change_direction('DOWN')
        if keys[pygame.K_LEFT]:
            snake2.change_direction('LEFT')
        if keys[pygame.K_RIGHT]:
            snake2.change_direction('RIGHT')

        # move both snakes
        snake1.move()
        snake2.move()

        # collisions with apples for both players
        if snake1.collides_with_apple(apple):
            snake1.grow()
            apple.randomize_position()
            score1 +=  1
        if snake2.collides_with_apple(apple):
            snake2.grow()
            apple.randomize_position()
            score2 +=  1

        # collisions with itself for both players
        if snake1.collides_with_itself() or snake2.collides_with_itself():
            game_over()

        # render both players' views on screen
        WINDOW.fill(WHITE)
        draw_player_view(snake1, score1)
        draw_player_view(snake2, score2)

        # draw apple in the center of the screen for both players to see
        pygame.draw.rect(WINDOW, RED, pygame.Rect(apple.position[0], apple.position[1],  20,  20))

        pygame.display.update()

def draw_player_view(snake, score):
    # snake's segments
    for segment in snake.elements:
        pygame.draw.rect(WINDOW, GREEN, pygame.Rect(segment[0], segment[1],   20,   20))

    # render score
    score_text = SCORE_FONT.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect()
    score_rect.topleft = (10,  10)
    WINDOW.blit(score_text, score_rect)

if __name__ == '__main__':
    main()
