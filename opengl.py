import pygame
from pygame.locals import *
from pygame import mixer_music, mixer

from gl import Renderer, Model
import shaders
import glm

deltaTime = 0.0

# Inicializacion de pygame
pygame.init()
clock = pygame.time.Clock()
screenSize = (960, 540)
screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)

# initialize in game music
mixer_music.load('sfx/lounge.wav')
mixer_music.play(-1)

blip = mixer.Sound('sfx/blip_1.wav')
next_meme = mixer.Sound('sfx/next_meme.wav')

# Inicializacion de nuestro Renderer en OpenGL
r = Renderer(screen)
r.camPosition.z = 3
r.pointLight.x = 30

r.setShaders(shaders.vertex_shader, shaders.fragment_shader)

r.modelList.append(Model('models/barrel.obj', 'textures/barrel.bmp', position=glm.vec3(0, -1, 0), scale=glm.vec3(1, 1, 1)))
r.modelList.append(Model('models/vase.obj', 'textures/vase.bmp', position=glm.vec3(0, -1.2, 0), scale=glm.vec3(1/2, 1/2, 1/2)))
r.modelList.append(Model('models/nature.obj', 'textures/vase.bmp', position=glm.vec3(0, -1, 0), scale=glm.vec3(1/8, 1/8, 1/8)))
r.modelList.append(Model('models/cup.obj', 'textures/vase.bmp', position=glm.vec3(0, -1, 0), scale=glm.vec3(1/2, 1/2, 1/2)))
r.modelList.append(Model('models/porcelain.obj', 'textures/porcelain.bmp', position=glm.vec3(0, -1, 0), scale=glm.vec3(1/2, 1/2, 1/2)))
r.modelList.append(Model('models/egg.obj', 'textures/porcelain.bmp', position=glm.vec3(0, -1, 0), scale=glm.vec3(1/5, 1/5, 1/5)))
r.active_model = 0

# variable for loop
isPlaying = True

# zoom value
zoom_in = 0

# movement with mouse
move_right = False
move_left = False
move_up = False
move_down = False

# mouse movement sensitivity
horizontal_intensity = 0
vertical_intensity = 0

# visualization mode
mode = 'INSPECT'

# loop for pygame
while isPlaying:

    # any key pressed
    keys = pygame.key.get_pressed()     

    if mode == 'SHOWCASE':
        if r.camPosition.z > 0:
            r.camPosition.x -= 1 * deltaTime
        else:
            r.camPosition.x += 1 * deltaTime

        if r.camPosition.x < 0:
            r.camPosition.z -= 1 * deltaTime
        else:
            r.camPosition.z += 1 * deltaTime
            
        r.camRotation.y -= deltaTime * 30
        r.camRotation.x = 0
    
    else:
        # move cam
        if keys[K_e]:
            if r.camPosition.z > 1.5:
                zoom_in -= 1 * deltaTime
                r.camPosition.z -= 1 * deltaTime
        if keys[K_q]:
            if r.camPosition.z < 5:
                zoom_in += 1
                r.camPosition.z += 1 * deltaTime
        if keys[K_w]:
            r.camPosition.y += 1 * deltaTime
            r.camRotation.x -= 15 * deltaTime
        if keys[K_s]:
            r.camPosition.y -= 1 * deltaTime
            r.camRotation.x += 15 * deltaTime
        if keys[K_a]:
            r.camPosition.x -= 1 * deltaTime
            r.camRotation.y -= 15 * deltaTime
        if keys[K_d]:
            r.camPosition.x += 1 * deltaTime
            r.camRotation.y += 15 * deltaTime

    for ev in pygame.event.get():
        position = pygame.mouse.get_pos()
        on_screen = pygame.mouse.get_focused()

        if ev.type == pygame.QUIT:
            isPlaying = False

        elif ev.type == pygame.MOUSEMOTION:
            if position[0] > 560:
                move_right = True
                move_left = False
                horizontal_intensity = 30 if position[0] > 760 else 15
            elif position[0] < 400:
                move_left = True
                move_right = False
                horizontal_intensity = 30 if position[0] < 200 else 15
            else:
                move_left = False
                move_right = False

            if position[1] > 340:
                move_down = True
                move_up = False
                vertical_intensity = 30 if position[1] > 440 else 15
            elif position[1] < 200:
                move_down = False
                move_up = True
                vertical_intensity = 30 if position[1] < 100 else 15
            else:
                move_down = False
                move_up = False

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_1:
                r.filledMode()
            elif ev.key == pygame.K_2:
                r.wireframeMode()
            elif ev.key == pygame.K_n:
                next_meme.play()
                r.active_model = (r.active_model + 1) % len(r.modelList)
            elif ev.key == pygame.K_m:
                blip.play()
                mode = 'SHOWCASE' if mode == 'INSPECT' else 'INSPECT'

                r.camPosition.x = 0
                r.camPosition.y = 0
                r.camPosition.z = 3
                
                r.camRotation.x = 0
                r.camRotation.y = 0
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False

    if on_screen == 1:
        if move_right:
            r.camRotation.y -= horizontal_intensity * deltaTime
        if move_left:
            r.camRotation.y += horizontal_intensity * deltaTime
        if move_down:
            r.camRotation.x -= vertical_intensity * deltaTime
        if move_up:
            r.camRotation.x += vertical_intensity * deltaTime

    # renderer loop
    r.render()

    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000

pygame.quit()
