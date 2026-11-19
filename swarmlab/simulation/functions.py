
# init
import pygame
from swarmlab.neural_network import neuralnetwork
import numpy as np

pygame.init()

screen = pygame.display.set_mode((640, 640))
screen_rect = screen.get_rect()

player = pygame.image.load('swarmlab/simulation/black_dot.png').convert_alpha()
player = pygame.transform.scale(player,
                                (player.get_width() / 30,
                                player.get_height() / 30))
font = pygame.font.Font(None, size=30)

# game objects and initial states - positioning, hitboxes, goals, obstacle
box_x = 150
box_y = 150
player_x = 0
player_y = 0
player_hitbox = pygame.Rect(player_x, player_y, player.get_width(), player.get_height())
box = pygame.Rect(box_x, box_y, 75, 75)
goal = pygame.Rect(450, 450, 200, 200)
player_distance = 150

# game control and timing
clock = pygame.time.Clock()
delta_time = 0.1

def simulation(action):
    global player_x
    global player_y
    global delta_time
    global box_x
    global box_y
    global player_distance

    # update - calculate position, sync collision rects, detect and resolve collisions, finalize positions
    first_player = pygame.math.Vector2(player_x, player_y)

    # decide movement
    if action[0] > 0:
        player_x += min(action[0] * player_distance * delta_time + player_distance, screen.width - player.width)
    elif action[0] < 0:
        player_x += max(action[0] * player_distance * delta_time - player_distance, 0)

    if action[1] > 0:
        player_y += min(action[1] * player_distance * delta_time + player_distance, screen.height - player.height)
    elif action[1] < 0:
        player_y += max(action[1] * player_distance * delta_time - player_distance, 0)
        
    second_player = pygame.math.Vector2(player_x, player_y)
    dx, dy = second_player - first_player

    player_x = first_player.x + dx
    player_hitbox.x = round(player_x)

    if player_hitbox.colliderect(box):
        if dx > 0:
            box.left = player_hitbox.right
        elif dx < 0:
            box.right = player_hitbox.left

    player_y = first_player.y + dy
    player_hitbox.y = round(player_y)

    if player_hitbox.colliderect(box):
        if dy > 0:
            box.top = player_hitbox.bottom
        elif dy < 0:
            box.bottom = player_hitbox.top

    box_x = box.x
    box_y = box.y

    if goal.contains(box):
        pygame.quit()

    # render - clear screen, draw surfaces, call flip to display new frame
    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (80, 200, 120), goal)
    pygame.draw.rect(screen, (0, 0, 0), box)
    screen.blit(player, (player_x, player_y))

    pygame.display.flip()

    # time related
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

    return player_x, player_y, box_x, box_y

def win_screen(screen):
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill("black")
        font = pygame.font.Font(None, size=100)
        text = font.render('you win!', True, (255, 255, 255))
        screen.blit(text, (200, 250))
        pygame.display.flip()

def agent_controller(observations: list[float | int], neural_network):
    np_array = np.array(observations)
    X = np.reshape(np_array, (-1, 1))
    _, activ_layer = neural_network.forward_propogation(X)
    action = activ_layer[-1]
    return (action[0][0], action[1][0])

def play_game_manually():
    running = True
    W = False
    A = False
    S = False
    D = False

    while running:
        # input - get keyboard inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    W = True
                if event.key == pygame.K_a:
                    A = True
                if event.key == pygame.K_s:
                    S = True
                if event.key == pygame.K_d:
                    D = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    W = False
                if event.key == pygame.K_a:
                    A = False
                if event.key == pygame.K_s:
                    S = False
                if event.key == pygame.K_d:
                    D = False

        direction_y = 0
        direction_x = 0

        # decide key
        if W == True and S == False:
            direction_y = -1
        if S == True and W == False:
            direction_y = 1

        if D == True and A == False:
            direction_x = 1
        if A == True and D == False:
            direction_x = -1

        action = (direction_x, direction_y)
        
        simulation(action)

def run_simulation(max_iterations):

    # Initialize
    counter = 0
    neural_network = neuralnetwork.NeuralNetwork([4, 16, 32, 2])
    action = (0, 0)
    player_x = 0
    player_y = 0
    box_x = 150
    box_y = 150

    while True:
        if counter > max_iterations:
            return "max iterations reached"

        # use observations to get new action
        action = agent_controller([player_x, player_y, box_x, box_y], neural_network)

        # do action then get observations
        player_x, player_y, box_x, box_y = simulation(action)

        counter += 1

run_simulation(500)

pygame.quit()
