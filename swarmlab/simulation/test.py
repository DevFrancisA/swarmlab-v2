# init
import pygame

pygame.init()

# assets and resources - load sprites, images, fonts, etc and scaling
screen = pygame.display.set_mode((640, 640))

player = pygame.image.load('swarmlab/simulation/black_dot.png').convert_alpha()
player = pygame.transform.scale(player,
                                (player.get_width() / 30,
                                 player.get_height() / 30))


font = pygame.font.Font(None, size=30)

# game objects and initial states - positioning, hitboxes, goals, obstacles
running = True

# position
player_x = 0
player_y = 0
box_x = 150
box_y = 150

player_hitbox = pygame.Rect(player_x, player_y, player.get_width(), player.get_height())
box = pygame.Rect(box_x, box_y, 75, 75)
goal = pygame.Rect(450, 450, 200, 200)

W = False
A = False
S = False
D = False

obstacles = []

# game control and timing
clock = pygame.time.Clock()
delta_time = 0.1

# game loop
while running:

    # input - get keyboard inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # update - calculate position, sync collision rects, detect and resolve collisions, finalize positions
    first_pos = pygame.math.Vector2(player_x, player_y)

    if W:
        player_y -= 150 * delta_time
    if A:
        player_x -= 150 * delta_time
    if S:
        player_y += 150 * delta_time
    if D:
        player_x += 150 * delta_time      

    second_pos = pygame.math.Vector2(player_x, player_y)
    displacement = second_pos - first_pos
    dx = displacement[0]
    dy = displacement[1]
    print(displacement)

    player_hitbox.x = player_x
    player_hitbox.y = player_y

    if player_hitbox.colliderect(box):
        if dy < 0:
            box.y = player_hitbox.top - box.height
        elif dy > 0:
            box.y = player_hitbox.bottom

    if player_hitbox.colliderect(box):
        if dx < 0:
            box.x = player_hitbox.left - box.width
        elif dx > 0:
            box.x = player_hitbox.right

    box_x = box.x
    box_y = box.y

    # render - clear screen, draw surfaces, call flip to display new frame
    screen.fill((255, 255, 255))

    text = font.render('push the black box into the green area', True, (0, 0, 0))
    screen.blit(text, (250, 0))

    pygame.draw.rect(screen, (0, 0, 0), box)
    pygame.draw.rect(screen, (80, 200, 120), goal)

    screen.blit(player, (player_x, player_y))

    pygame.display.flip()

    # time related
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))



pygame.quit()
