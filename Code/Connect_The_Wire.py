import pygame, sys, levels, module

def creating_wire_list(level):
    global score, right, right_amount, wire

    right_amount = len(levels.right_list[level])
    score = levels.list_of_sums[level]
    right = levels.right_list[level]
    for index in range(len(levels.list_of_levels[level])):
        if levels.types[level][index] == 0:
            wire = module.Wire(index, 0, level)
            wires.append(wire)
        elif levels.types[level][index] == 1:
            wire = module.Wire(index, 1, level)
            wires.append(wire)
        elif levels.types[level][index] == 2:
            wire = module.Wire(index, 2, level)
            wires.append(wire)
        elif levels.types[level][index] == 3:
            wire = module.Wire(index, 3, level)
            wires.append(wire)
        elif levels.types[level][index] == 4:
            wire = module.Wire(index, 4, level)
            wires.append(wire)


# variables
level = module.level
cooldown = 20
countdown = 20
wires = []
level_finished = False
next_level = False
bright = False
language_choice = 0

# setup
pygame.init()
pygame.display.set_caption('Connect The Wire')
icon = pygame.image.load('Graphics/title_image.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
music = pygame.mixer.Sound('Audio/music.wav')
music.play(loops=-1)

battery = pygame.image.load('Graphics/battery.png').convert_alpha()
battery = pygame.transform.scale_by(battery, .15)
battery_rect = battery.get_rect(bottomleft=(30, 569))

bulb = module.Bulb()

cursor_img = pygame.transform.scale_by(pygame.image.load('Graphics/Cursor/cursor_1.png').convert_alpha(), 0.15)
cursor_rect = cursor_img.get_rect()
cursor_img1 = pygame.transform.scale_by(pygame.image.load('Graphics/Cursor/cursor_2.png').convert_alpha(), 0.15)
cursor_rect1 = cursor_img1.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.mouse.set_visible(False)

    try:
        if pygame.mouse.get_pressed()[0] and level_finished and cooldown == 20:
            next_level = True
        if pygame.mouse.get_pressed()[0] and next_level:
            level += 1
            wires = []
            bright = bulb.turn_off()
            next_level = False
            level_finished = False

        if wires == []:
            creating_wire_list(level)

        if bright:
            module.screen.fill(module.lavender)
        else:
            module.screen.fill(module.purple)
        module.show_level(level, language_choice)
        module.instruction(language_choice)
        cooldown, language_choice = module.language(language_choice, cooldown)

        for item in range(len(levels.list_of_levels[level])):
            if wires[item].tapping_on_wire() and countdown == 20:
                # check if straight wires are correctly oriented
                if levels.types[level][item] == 0:
                    for i in range(right_amount):
                        if right[i][item] is False:
                            score[i] += 1
                            right[i][item] = True
                        elif right[i][item] is True:
                            score[i] -= 1
                            right[i][item] = False
                # check if |_ wire(L-shape) is correctly oriented
                elif levels.types[level][item] == 1 or levels.types[level][item] == 3 or levels.types[level][item] == 4:
                    for i in range(right_amount):
                        if right[i][item] == 0:
                            score[i] -= 1
                            right[i][item] = 3
                        elif right[i][item] == 1:
                            score[i] += 1
                            right[i][item] = 0
                        else:
                            right[i][item] -= 1
                # main action - turning the wires and keeping score
                wires[item].turn()
                for i in range(right_amount):
                    if score[i] == 13:
                        bright = bulb.light_up_bulb()
                        level_finished = True
                countdown -= 1

        if cooldown < 20:
            cooldown -= 1
            if cooldown <= 0:
                cooldown = 20

        if countdown < 20:
            countdown -= 1
            if countdown <= 0:
                countdown = 20

        bulb.draw()
        for item in range(len(levels.list_of_levels[level])):
            wires[item].draw()
        module.screen.blit(battery, battery_rect)

        if not pygame.mouse.get_pressed()[0]:
            cursor_rect = pygame.mouse.get_pos()
            module.screen.blit(cursor_img, cursor_rect)
        elif pygame.mouse.get_pressed()[0]:
            cursor_rect1 = pygame.mouse.get_pos()
            module.screen.blit(cursor_img1, cursor_rect1)

    except IndexError:
        module.finish_of_game(language_choice)
        cursor_rect = pygame.mouse.get_pos()
        module.screen.blit(cursor_img, cursor_rect)
        music.fadeout(1000)

    pygame.display.update()
    clock.tick(60)
