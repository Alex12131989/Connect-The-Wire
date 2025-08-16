import pygame, levels, sys, tkinter


class Bulb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.dead_bulb = pygame.image.load('Graphics/Bulb/bulb_dead.png').convert_alpha()
        self.dead_bulb = pygame.transform.scale_by(self.dead_bulb, 0.086)
        self.alive_bulb = pygame.image.load('Graphics/Bulb/bulb_alive.png').convert_alpha()
        self.alive_bulb = pygame.transform.scale_by(self.alive_bulb, 0.086)
        self.states = [self.dead_bulb, self.alive_bulb]
        self.image = self.states[self.index]
        self.rect = self.image.get_rect(midbottom=(523, 317))

    def light_up_bulb(self):
        if self.index == 0:
            self.index = 1
        self.image = self.states[self.index]
        return True

    def turn_off(self):
        if self.index == 1:
            self.index = 0
        self.image = self.states[self.index]
        return False

    def draw(self):
        screen.blit(self.image, self.rect)


class Wire(pygame.sprite.Sprite):
    def __init__(self, index, img, lvl):
        super().__init__()
        self.coordinates_level = levels.list_of_levels[lvl]
        self.right_button = False

        self.wire1 = pygame.image.load('Graphics/Wire/wire1.png').convert_alpha()
        self.wire1 = pygame.transform.scale_by(self.wire1, .3)
        self.wire2 = pygame.image.load('Graphics/Wire/wire2.png').convert_alpha()
        self.wire2 = pygame.transform.scale_by(self.wire2, .3)
        self.cross_wire = pygame.image.load('Graphics/Wire/cross_wire.png').convert_alpha()
        self.cross_wire = pygame.transform.scale_by(self.cross_wire, .3)
        self.finished = pygame.image.load('Graphics/Wire/finished.png').convert_alpha()
        self.finished = pygame.transform.scale_by(self.finished, .3)
        self.t_wire = pygame.image.load('Graphics/Wire/T_wire.png')
        self.t_wire = pygame.transform.scale_by(self.t_wire, .3)
        self.list = [self.wire1, self.wire2, self.cross_wire, self.t_wire, self.finished]
        self.image = self.list[img]
        self.rect = self.image.get_rect(center=self.coordinates_level[index])
        screen.blit(self.image, self.rect)

    def tapping_on_wire(self):
        self.right_button = pygame.mouse.get_pressed()[0]
        if self.right_button:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                return True
        else:
            return False

    def turn(self):
        self.image = pygame.transform.rotate(self.image, 90)
        screen.blit(self.image, self.rect)

    def draw(self):
        screen.blit(self.image, self.rect)


pygame.font.init()
pygame.font.get_init()

screen = pygame.display.set_mode((600, 600))
level = 0
new_window = False
font = pygame.font.SysFont('comic sans cm', 100)
level_font = pygame.font.SysFont('comic sans cm', 40)
level_font1 = pygame.font.SysFont('comic sans cm', 35)

lavender = (201, 148, 227)
burning_red = (153, 35, 5)
purple = (106, 13, 173)


def finish_of_game(language):
    global level
    screen.fill(lavender)
    if language == 0:
        label = font.render('You have finished', True, (0, 200, 0))
        label1 = font.render('all levels', True, (0, 200, 0))
    else:
        label = font.render('#$@@@@@%@%#', True, (0, 200, 0))
        label1 = font.render('$^!###*!@P#', True, (0, 200, 0))
    label_rect = label.get_rect(center=(300, 250))
    label_rect1 = label1.get_rect(center=(300, 350))
    screen.blit(label, label_rect)
    screen.blit(label1, label_rect1)


def show_level(lvl, language):
    rectangle = pygame.rect.Rect(0, 0, 150, 50)
    if language == 0:
        level_label = level_font.render(f'Level: {lvl+1}', True, (240, 50, 36))
    else:
        level_label = level_font1.render(f'%#$@@^%*:', True, (240, 50, 36))
    level_rect = level_label.get_rect(center=(75, 25))
    pygame.draw.rect(screen, burning_red, rectangle)
    screen.blit(level_label, level_rect)


def instruction_window(language):
    window = tkinter.Tk()

    if language == 0:
        window.title('Instruction')
    else:
        window.title('&^$@@#$&^')
    window.iconphoto(True, tkinter.PhotoImage(file='Graphics/file.png'))

    x = int(window.winfo_screenwidth() / 2 - 308)
    y = int(window.winfo_screenheight() / 2 - 332)
    window.geometry(f'600x600+{x}+{y}')
    window.resizable(False, False)
    text = tkinter.Text(window, font=('comic sans mc', 20))
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    text.grid(sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)

    if language == 0:
        text_file = open('Instructions/instructions.txt', 'r')
    else:
        text_file = open('Instructions/instructions - Copy.txt', 'r', encoding="utf8")
    text.insert(tkinter.END, text_file.read())
    text_file.close()

    scroll_bar = tkinter.Scrollbar(window, orient='vertical', command=text.yview)
    scroll_bar.grid(row=0, column=1, sticky=tkinter.N + tkinter.E + tkinter.S)
    text.config(yscrollcommand=scroll_bar.set, bg='#c994e3')

    window.mainloop()


def instruction(language):
    file_rect1 = pygame.rect.Rect(151, 0, 50, 50)
    pygame.draw.rect(screen, burning_red, file_rect1)
    if pygame.mouse.get_pressed()[0]:
        if file_rect1.collidepoint(pygame.mouse.get_pos()):
            instruction_window(language)
    file = pygame.transform.scale_by(pygame.image.load('Graphics/file.png').convert_alpha(), 0.1)
    file_rect = file.get_rect(topleft=(151, 0))
    screen.blit(file, file_rect)


def language(language_choice, countdown):
    rectangle_language = pygame.rect.Rect(202, 0, 130, 50)
    pygame.draw.rect(screen, burning_red, rectangle_language)
    if pygame.mouse.get_pressed()[0] and countdown == 20:
        countdown = 19
        if rectangle_language.collidepoint(pygame.mouse.get_pos()):
            if language_choice == 0:
                language_choice = 1
            else:
                language_choice = 0
    if language_choice == 0:
        lang_label = level_font.render('English', True, (240, 50, 36))
    else:
        lang_label = level_font.render('##%#@!!#', True, (240, 50, 36))
    lang_rect = lang_label.get_rect(center=(267, 25))
    screen.blit(lang_label, lang_rect)

    return countdown, language_choice

