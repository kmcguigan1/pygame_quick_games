import pygame

# game variables
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JUMP MAN!")
# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
# character vars
CHARACTER_WIDTH, CHARACTER_HEIGHT = 40, 65
RUNNING = 0
JUMPING = 1
DUCKING = 2
# frame limit
FPS = 30
# jumping variables
JUMP_VEL = 25
GRAVITY = 2
# ground variables
BASE_HEIGHT = 3*HEIGHT//4
GROUND = pygame.Rect(0, BASE_HEIGHT, WIDTH, HEIGHT//25)
# obstacle variables
BASE_INIT_VEL = 10
BASE_VEL_INCR = 2
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
# game events
ADD_OBS_EVENT = pygame.USEREVENT + 1
ACCELERATE_EVENT = ADD_OBS_EVENT + 1
COLLISION_EVENT = ACCELERATE_EVENT + 1

pygame.init()

class Character():
    def __init__(self):
        self.state = RUNNING
        self.velocity = 0
        center_x = (WIDTH//4) - (CHARACTER_WIDTH//2)
        center_y = BASE_HEIGHT - CHARACTER_HEIGHT
        super().__init__(center_x, center_y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    def jump(self):
        if(self.state == RUNNING or self.state == DUCKING):
            self.state = JUMPING
            self.velocity = JUMP_VEL
    def duck(self):
        if(self.state == RUNNING):
            self.state = DUCKING
    def move_character(self):
        if(self.state == RUNNING):
            pass
        elif(self.state == JUMPING):
            self.y -= self.velocity
            self.velocity -= GRAVITY
            if(self.y > BASE_HEIGHT - CHARACTER_HEIGHT): # consider gte to allow for a tick earlier to jump
                self.y = BASE_HEIGHT - CHARACTER_HEIGHT
                self.velocity = 0
                self.state = RUNNING
        else:
            raise Exception(f'character state was {self.state}, not a valid state')
    def show(self):
        print(f"STATE {self.state} VEL {self.velocity} POS ({self.x}, {self.y})")

class Obstacle(pygame.Rect):
    def __init__(self, width, height):
        start_x = WIDTH 
        start_y = BASE_HEIGHT - height
        self.width = width
        self.height = height
        super().__init__(start_x, start_y, width, height)
    def move(self, vel):
        self.x -= vel
        if(self.x + self.width <= 0):
            return False
        return True
    def show(self):
        print(f"POS ({self.x}, {self.y})")

class Base():
    def __init__(self):
        self.velocity = BASE_INIT_VEL
        self.obstacles = []
    def speedup(self):
        self.velocity += BASE_VEL_INCR
    def move_obstacles(self):
        for obs in self.obstacles:
            if(not obs.move(self.velocity)):
                del obs
    def add_obstacle(self):
        obstacle = Obstacle(OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        self.obstacles.append(obstacle)
    def show(self):
        print(f"VEL {self.velocity}")

def draw(character, base):
    WIN.fill(WHITE)
    for obs in base.obstacles:
        pygame.draw.rect(WIN, RED, obs)
    pygame.draw.rect(WIN, BLUE, character)
    pygame.draw.rect(WIN, BLACK, GROUND)
    pygame.display.update()

def handle_keys(keys_pressed, character):
    if(keys_pressed[pygame.K_DOWN]):
        character.duck()
    if(keys_pressed[pygame.K_UP]):
        character.jump()

def handle_character(character):
    character.move_character()

def handle_base(base):
    base.move_obstacles()

def handle_collisions(character, base):
    for obs in base.obstacles:
        if(character.colliderect(obs)):
            pygame.event.post(pygame.event.Event(COLLISION_EVENT))

def main():
    character = Character()
    base = Base()
    clock = pygame.time.Clock()
    pygame.time.set_timer(ADD_OBS_EVENT, 4_000)
    pygame.time.set_timer(ACCELERATE_EVENT, 8_000)
    run = True
    while(run):
        clock.tick(FPS)
        for event in pygame.event.get(): # handle all the events in the event queue
            if(event.type == pygame.QUIT):
                run = False
                pygame.quit()
            if(event.type == COLLISION_EVENT):
                run = False
                break
            if(event.type == ADD_OBS_EVENT):
                base.add_obstacle()
            if(event.type == ACCELERATE_EVENT):
                base.speedup()

        keys_pressed = pygame.key.get_pressed()
        handle_keys(keys_pressed, character)
        handle_character(character)
        handle_base(base)
        handle_collisions(character, base)
        draw(character, base)

if __name__ == '__main__':
    main()