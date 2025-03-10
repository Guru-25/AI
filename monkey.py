import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Monkey-Banana Problem Simulation')

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

# Load images
def load_image(name, size):
    try:
        img = pygame.image.load(f"{name}.png")
        return pygame.transform.scale(img, size)
    except pygame.error:
        # If image not found, create a placeholder
        surface = pygame.Surface(size)
        surface.fill((255, 0, 255))
        font = pygame.font.SysFont(None, 24)
        text = font.render(name, True, BLACK)
        surface.blit(text, (size[0]//2 - text.get_width()//2, size[1]//2 - text.get_height()//2))
        return surface

# Images
monkey_img = load_image("monkey", (80, 80))
banana_img = load_image("banana", (60, 60))
box_img = load_image("box", (100, 100))

# Initial positions
monkey_pos = [100, HEIGHT - 120]
box_pos = [500, HEIGHT - 100]
banana_pos = [400, 100]

# States
IDLE = 0
MOVING_TO_BOX = 1
PUSHING_BOX = 2
CLIMBING_BOX = 3
GRABBING_BANANA = 4
CELEBRATING = 5

state = IDLE
step_counter = 0
font = pygame.font.SysFont(None, 36)

# State descriptions
state_descriptions = [
    "Initial State: Monkey sees banana and box",
    "Moving to box",
    "Pushing box under banana",
    "Climbing on the box",
    "Grabbing the banana",
    "Goal achieved! Monkey has the banana"
]

def draw_scene():
    screen.fill(WHITE)
    
    # Draw floor
    pygame.draw.line(screen, BLACK, (0, HEIGHT - 40), (WIDTH, HEIGHT - 40), 2)
    
    # Draw ceiling
    pygame.draw.line(screen, BLACK, (0, 20), (WIDTH, 20), 2)
    
    # Draw banana (if not grabbed)
    if state < GRABBING_BANANA:
        screen.blit(banana_img, (banana_pos[0], banana_pos[1]))
        # Draw string
        pygame.draw.line(screen, BLACK, (banana_pos[0] + 30, 20), (banana_pos[0] + 30, banana_pos[1]), 2)
    
    # Draw box
    screen.blit(box_img, (box_pos[0], box_pos[1]))
    
    # Draw monkey
    if state == CLIMBING_BOX or state == GRABBING_BANANA or state == CELEBRATING:
        # Monkey is on the box
        screen.blit(monkey_img, (monkey_pos[0], box_pos[1] - monkey_img.get_height()))
    else:
        screen.blit(monkey_img, (monkey_pos[0], monkey_pos[1]))
    
    # If monkey has the banana
    if state >= GRABBING_BANANA:
        screen.blit(banana_img, (monkey_pos[0] + 40, monkey_pos[1] - 30))
    
    # Display current state and step
    text = font.render(state_descriptions[state], True, BLACK)
    screen.blit(text, (20, 30))
    step_text = font.render(f"Step: {step_counter}", True, BLACK)
    screen.blit(step_text, (WIDTH - 150, 30))

def update_state():
    global state, step_counter, monkey_pos, box_pos
    
    step_counter += 1
    
    if state == IDLE and step_counter > 30:
        state = MOVING_TO_BOX
        step_counter = 0
    
    elif state == MOVING_TO_BOX:
        # Move monkey towards box
        if monkey_pos[0] < box_pos[0] - 50:
            monkey_pos[0] += 5
        else:
            state = PUSHING_BOX
            step_counter = 0
    
    elif state == PUSHING_BOX:
        # Push box under banana
        if box_pos[0] > banana_pos[0] - 20:
            box_pos[0] -= 3
            monkey_pos[0] -= 3
        else:
            state = CLIMBING_BOX
            step_counter = 0
    
    elif state == CLIMBING_BOX:
        if step_counter > 20:
            state = GRABBING_BANANA
            step_counter = 0
    
    elif state == GRABBING_BANANA:
        if step_counter > 20:
            state = CELEBRATING
            step_counter = 0

def main():
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset simulation
                    global state, step_counter, monkey_pos, box_pos
                    state = IDLE
                    step_counter = 0
                    monkey_pos = [100, HEIGHT - 120]
                    box_pos = [500, HEIGHT - 100]
        
        update_state()
        draw_scene()
        
        # Explanation box
        # pygame.draw.rect(screen, (240, 240, 240), (20, HEIGHT - 180, WIDTH - 40, 130))
        # pygame.draw.rect(screen, BLACK, (20, HEIGHT - 180, WIDTH - 40, 130), 2)
        
        # info_text = [
        #     # "Monkey-Banana Problem: AI Planning Problem Simulation",
        #     # "The monkey must plan a sequence of actions to reach the banana:",
        #     # "1. Move to the box  2. Push box under banana  3. Climb box  4. Grab banana",
        #     # "Press R to reset the simulation"
        # ]
        
        # for i, line in enumerate(info_text):
        #     info = font.render(line, True, BLACK)
        #     screen.blit(info, (30, HEIGHT - 170 + i * 30))
            
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()