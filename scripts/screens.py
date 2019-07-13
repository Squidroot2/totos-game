"""Contains the screens, each of which contains its own while loop

Functions:
    titleScreen(window, fps_clock)
    playerCreateScreen(window, fps_clock)
"""
import pygame

from scripts.utilities import checkForQuit
from pygame.constants import *


# GLOBAL VALUES
#                    R   G   B
COLORS = {'BLACK': (  0,  0,  0),
          'WHITE': (255,255,255)}

pygame.font.init()
FONTS = {'TITLE': pygame.font.Font('freesansbold.ttf', 70),
         'MAIN': pygame.font.Font('freesansbold.ttf', 28),
         'INFO': pygame.font.Font('freesansbold.ttf', 14)}
FONTS['TITLE'].set_underline(True)

FPS = 144

def titleScreen(window, fps_clock):
    """Displays the Title Screen. Runs its own while loop until the player hits enter to continue

    Parameters:
        window : pygame.Surface
            Where the content will get drawn to
        fps_clock : pygame.Clock
            Used to keep FPS Steady

    """

    # Fills the screen with WHITE
    window.fill(COLORS['WHITE'])

    # Stores a rect representing the entire window. This is used for relative placement of surfaces
    window_rect = window.get_rect()

    title = FONTS['TITLE'].render('Grim Ranger', True, COLORS['BLACK'])
    title_rect = title.get_rect()
    title_rect.center = (window_rect.centerx, window_rect.height/6)

    subtitle = FONTS['MAIN'].render("A Game By Hayden Foley", True, COLORS['BLACK'])
    subtitle_rect = subtitle.get_rect()
    subtitle_rect.midtop = (window_rect.centerx, title_rect.bottom + FONTS['MAIN'].get_linesize())

    continue_prompt = FONTS['MAIN'].render("Press Enter to Continue", True, COLORS['BLACK'])
    continue_prompt_rect = continue_prompt.get_rect()
    continue_prompt_rect.center = (window_rect.centerx, window_rect.height*(2/3))

    # Cover used to give the illusion of transparency to the Font surface
    continue_cover = pygame.Surface((continue_prompt_rect.width, continue_prompt_rect.height))
    continue_cover.fill(COLORS['WHITE'])

    # Sets variables for the alpha of the cover
    alpha_max = 200
    alpha_min = 25
    alpha_change_rate = 5

    # Sets the alpha, stores it in cover_alpha, and sets decrease_alpha to True
    continue_cover.set_alpha(alpha_max)
    cover_alpha = continue_cover.get_alpha()
    decrease_alpha = True

    # Blits each of the Font surfaces to the screen
    window.blit(title, title_rect)
    window.blit(subtitle, subtitle_rect)
    window.blit(continue_prompt, continue_prompt_rect)

    # Runs loop while show_title is True
    show_title = True
    while show_title:
        checkForQuit()
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_RETURN:
                show_title = False

        # Decreases or increases alpha of cover
        if decrease_alpha:
            continue_cover.set_alpha(cover_alpha - alpha_change_rate)
        else:
            continue_cover.set_alpha(cover_alpha + alpha_change_rate)

        # Checks if alpha has reached minimum or maximum
        cover_alpha = continue_cover.get_alpha()
        if cover_alpha == alpha_min:
            decrease_alpha = False
        elif cover_alpha == alpha_max:
            decrease_alpha = True

        # Blits continue_prompt, then cover over it
        window.blit(continue_prompt, continue_prompt_rect)
        window.blit(continue_cover, continue_prompt_rect)

        pygame.display.flip()
        fps_clock.tick(FPS)

def playerCreateScreen(window, fps_clock):
    """Displays the player creation window where the player can choose their name and class

    Parameters:
        window : pygame.Surface
            Where the content will get drawn to
        fps_clock : pygame.Clock
            Used to keep FPS Steady

    """

    window_rect = window.get_rect()


    name_prompt = FONTS['MAIN'].render("Name: ", True, COLORS['BLACK'])
    name_prompt_rect = name_prompt.get_rect()
    name_prompt_rect.midright = (window_rect.centerx, window_rect.height/6)

    name = ''

    # Clear the events to ensure no keys previously pressed show up in the name
    pygame.event.clear()

    name_chosen = False
    while not name_chosen:
        window.fill(COLORS['WHITE'])
        window.blit(name_prompt, name_prompt_rect)

        #drawClassSelect()

        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN and name != '':
                    name_chosen = True
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        name_text = FONTS['MAIN'].render(name, True, COLORS['BLACK'])
        input_rect = name_text.get_rect()
        input_rect.midleft = (name_prompt_rect.right, name_prompt_rect.centery)

        window.blit(name_text, input_rect)

        fps_clock.tick(FPS)
        pygame.display.flip()

    # todo have the player choose class in this function and return it
    return name

# todo finish drawClassSelect
def drawClassSelect(window):
    window.get_rect()


def mainGameScreen(window, fps_clock, player):
    '''runs the main game loop as long as the run_game boolean is true'''
    window_rect = window.get_rect()

    panes = getPanes(window_rect)

    drawStatPane(window, player, panes['side'])
    drawLogPane(window, player, panes['bottom'])


    #game loop
    run_game = True
    while run_game:
        checkForQuit()
        for event in pygame.event.get():


            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_KP8:
                    player.move(0, -1)
                elif event.key == K_DOWN or event.key == K_KP2:
                    player.move(0, 1)
                elif event.key == K_LEFT or event.key == K_KP4:
                    player.move(-1, 0)
                elif event.key == K_RIGHT or event.key == K_KP6:
                    player.move(1, 0)
                elif event.key == K_KP7:
                    player.move(-1, -1)
                elif event.key == K_KP9:
                    player.move(1, -1)
                elif event.key == K_KP1:
                    player.move(-1, 1)
                elif event.key == K_KP3:
                    player.move(1, 1)
                elif event.key == K_i:
                    # todo write open inventory screen
                    pass
                elif event.key == K_f:
                    # todo write ranged attack screen
                    pass

                for entity in player.location.entities:
                    if entity.ai:
                        entity.ai.takeTurn()
        # Draw the map
        player.location.draw(window)

        # Draw the entities in the map
        for entity in player.location.entities:
            if entity is player:
                continue
            entity.draw(window)
        player.draw(window)

        drawStatPane(window, player, panes['side'])
        drawLogPane(window, player, panes['bottom'])

        pygame.display.update()
        fps_clock.tick(FPS)

def getPanes(window_rect):
    """Takes a pygame.Rect object representing the window and returns a dictionary of Rect Objects for the three panes
    of the mainGameScreen"""

    # Explicit variables for the size of the panes
    bottom_pane_height = window_rect.height / 6
    side_pane_width = window_rect.width / 4

    # Calculate bottom pane dimensions
    bottom_pane_top = window_rect.bottom - bottom_pane_height
    bottom_pane_width = window_rect.width - side_pane_width

    # Calculate side pane dimension
    side_pane_left = window_rect.width - side_pane_width

    # Calculate main pane dimensions
    main_pane_width = window_rect.width - side_pane_width
    main_pane_height = window_rect.height - bottom_pane_height

    # Create Rect Objects
    bottom_pane = pygame.Rect(0, bottom_pane_top, bottom_pane_width, bottom_pane_height)
    side_pane = pygame.Rect(side_pane_left, 0, side_pane_width, window_rect.height)
    main_pane = pygame.Rect(0, 0, main_pane_width, main_pane_height)

    # Create dictionary
    panes = {'bottom': bottom_pane,
             'side': side_pane,
             'main': main_pane}

    # Return dictionary
    return panes


def drawStatPane(window, player, pane):
    """Draws the players statistics on the right side of the screen"""

    # Fills in the pane in black
    pygame.draw.rect(window, COLORS['BLACK'], pane, 0)

    X_MARGIN = pane.width/10
    Y_MARGIN = pane.height/25

    # Strings used
    full_name = player.name + " the " + player.background
    experience = "XL: %d" % player.level
    defense = "Defense: %d" % player.getDefense()
    life = "Life: %d" % player.life

    # Dictionary of text surfaces that will be blitted to the screen
    text_surfs = dict()

    text_surfs['name'] = FONTS['INFO'].render(full_name, True, COLORS['WHITE'], COLORS['BLACK'])
    text_surfs['xp'] = FONTS['INFO'].render(experience, True, COLORS['WHITE'], COLORS['BLACK'])
    text_surfs['defense'] = FONTS['INFO'].render(defense,  True, COLORS['WHITE'], COLORS['BLACK'])
    text_surfs['energy_key'] = FONTS['INFO'].render("Energy", True, COLORS['WHITE'], COLORS['BLACK'])

    # Create Dictionary of Rectangle objects for each rect
    text_rects = {surf: text_surfs[surf].get_rect() for surf in text_surfs}

    # Place rectangles
    text_rects['name'].midleft = (pane.left+X_MARGIN, Y_MARGIN)
    text_rects['xp'].topleft = (pane.left+X_MARGIN, text_rects['name'].bottom)
    text_rects['defense'].topleft = (pane.left+X_MARGIN, text_rects['xp'].bottom)

    for text in text_surfs:
        window.blit(text_surfs[text], text_rects[text])


def drawLogPane(window, player, pane):

    # Fills in the pane in black
    # 0 represents the width, if zero fills in rect
    pygame.draw.rect(window, COLORS['BLACK'], pane, 0)




