import pygame
import random
pygame.init()

# game variables
WIDTH, HEIGHT = 700, 1200
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RUN!")
# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
# frame limit
FPS = 30
# track information
LEFT, MID, RIGHT = 0, 1, 2
TRACK = (LEFT, MID, RIGHT)
LANES = (
    (WIDTH//3) - (WIDTH//3//2),
    (2*WIDTH//3) - (WIDTH//3//2),
    WIDTH - (WIDTH//3//2),
)
# Game play variables
INIT_VEL = 7
VEL_INCR = 2
# game events
ADD_OBS_EVENT = pygame.USEREVENT + 1
ACCELERATE_EVENT = ADD_OBS_EVENT + 1
COLLISION_EVENT = ACCELERATE_EVENT + 1

class Obstacle(pygame.Rect):
    OBS_WIDTH, OBS_HEIGHT = 120, 120
    def __init__(self, lane):
        super().__init__(LANES[lane] - (Obstacle.OBS_WIDTH//2), -Obstacle.OBS_HEIGHT, Obstacle.OBS_WIDTH, Obstacle.OBS_HEIGHT)
    def advance(self, y_dist):
        self.y += y_dist
        if(self.y >= HEIGHT):
            return False 
        return True

class ObstacleHandler:
    def __init__(self):
        self.obstacles = []
    def add_obstacle(self, level):
        n_obs = 1
        if(level > random.randint(1, 100)):
            n_obs = 2
        positions = random.sample(TRACK, n_obs)
        for pos in positions:
            self.obstacles.append(Obstacle(pos))
    def advance_obstacles(self, y_dist):
        for obs in self.obstacles:
            if(not obs.advance(y_dist)):
                del obs
    def check_collisions(self, player):
        for obs in self.obstacles:
            if(player.colliderect(obs)):
                pygame.event.post(pygame.event.Event(COLLISION_EVENT))
    def draw(self):
        for obs in self.obstacles:
            pygame.draw.rect(WIN, RED, obs)


class Player(pygame.Rect):
    PLAYER_WIDTH, PLAYER_HEIGHT = 90, 90
    def __init__(self, lane):
        self.lane = lane
        x_pos = LANES[self.lane] - (Player.PLAYER_WIDTH//2)
        super().__init__(x_pos, HEIGHT - Player.PLAYER_HEIGHT - (HEIGHT//10), Player.PLAYER_WIDTH, Player.PLAYER_HEIGHT)
    def go_left(self):
        if(self.lane != LEFT):
            self.lane -= 1
            self.x = LANES[self.lane] - (Player.PLAYER_WIDTH//2)
    def go_right(self):
        if(self.lane != RIGHT):
            self.lane += 1
            self.x = LANES[self.lane] - (Player.PLAYER_WIDTH//2)
    def draw(self):
        pygame.draw.rect(WIN, BLUE, self)

class Board:
    def __init__(self):
        self.track_dividers = (
            pygame.Rect((WIDTH//3)-(WIDTH//50//2), 0, WIDTH//50, HEIGHT),
            pygame.Rect((2*(WIDTH//3))-(WIDTH//50//2), 0, WIDTH//50, HEIGHT)
        )
    def draw(self):
        for div in self.track_dividers:
            pygame.draw.rect(WIN, BLACK, div)

class Game:
    def __init__(self):
        self.velocity = INIT_VEL
        self.level = 1
    def speedup(self):
        self.velocity += VEL_INCR
        if(self.level < 99):
            self.level += 1

def draw(board, obs_handler, player):
    WIN.fill(WHITE)
    board.draw()
    obs_handler.draw()
    player.draw()
    pygame.display.update()

def main():
    game = Game()
    board = Board()
    player = Player(MID)
    obs_handler = ObstacleHandler()
    clock = pygame.time.Clock()
    pygame.time.set_timer(ADD_OBS_EVENT, 3_000)
    pygame.time.set_timer(ACCELERATE_EVENT, 6_000)
    run = True
    while(run):
        clock.tick(FPS)
        for event in pygame.event.get(): # handle all the events in the event queue
            if(event.type == pygame.QUIT):
                run = False
                pygame.quit()
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LEFT):
                    player.go_left()
                if(event.key == pygame.K_RIGHT):
                    player.go_right()
            if(event.type == COLLISION_EVENT):
                run = False
            if(event.type == ADD_OBS_EVENT):
                obs_handler.add_obstacle(game.level)
            if(event.type == ACCELERATE_EVENT):
                game.speedup()

        obs_handler.advance_obstacles(game.velocity)
        obs_handler.check_collisions(player)
        draw(board, obs_handler, player)

if __name__ == '__main__':
    main()