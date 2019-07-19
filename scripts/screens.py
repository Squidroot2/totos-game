"""Contains the screens, each of which contains its own while loop

Functions:
    titleScreen(window, fps_clock)
    playerCreateScreen(window, fps_clock)
    mainGameScreen(window, fps_clock, game)
    gameOverScreen(window, fps_clock)


"""
import pygame
from pygame.constants import *
from scripts.constants import COLORS, FONTS, FPS
from scripts.utilities import checkForQuit


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

    Returns:
        name : string
            Chosen name of the player character
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


def mainGameScreen(window, fps_clock, game):
    """runs the main game loop as long as the run_game boolean is true"""
    window_rect = window.get_rect()
    
    # Pulls the player from the game object
    player = game.player

    # Gets a dict of Rects
    panes = getPanes(window_rect)

    # Create a Rect with the same dimensions as the camera; center it in the main pane
    game_area = player.camera.getRect().copy()
    game_area.center = panes['main'].center

    #game loop
    run_game = True
    while run_game:
        checkForQuit()
        for event in pygame.event.get():

            # Determine what to do with Key Presses
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

        if player.is_dead:
            run_game = False

        window.fill(COLORS['BLACK'])
        # Draw the map
        player.location.draw(game.surface)

        # Draw the entities in the map
        for entity in player.location.entities:
            if entity is player:
                continue
            entity.draw(game.surface)
        player.draw(game.surface)

        # Draw the side and log panes
        drawStatPane(window, player, panes['side'])
        drawLogPane(window, game.log, panes['log'])

        pygame.draw.rect(window, COLORS['DARK GRAY'], panes['bottom'], 0)
        player.camera.update()

        # todo add the following line after camera and game.surface are finished
        window.blit(game.surface, game_area, player.camera.getRect())
            
        # Update the screen and wait for clock to tick; repeat the while loop
        pygame.display.update()
        fps_clock.tick(FPS)

def gameOverScreen(window, fps_clock):
    """Shown after the player dies

    Parameters:
        window : pygame.Surface
        fps_clock : pygame.Clock
    """

    window.fill(COLORS['BLACK'])

    window_rect = window.get_rect()

    text = FONTS['TITLE'].render('Game Over', True, COLORS['RED'])
    text_rect = text.get_rect()
    text_rect.center = (window_rect.center)

    window.blit(text, text_rect)
    show_game_over = True

    while show_game_over:
        checkForQuit()
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_RETURN:
                show_game_over = False

        pygame.display.flip()
        fps_clock.tick(FPS)

def getPanes(window_rect):
    """Takes a pygame.Rect object representing the window and returns a dictionary of Rect Objects for the four panes
    of the mainGameScreen"""

    # log pane margin from bottom
    log_y_margin = 10

    # Explicit variables for the size of the panes
    bottom_pane_height = window_rect.height / 25
    side_pane_width = window_rect.width / 4
    log_pane_width = window_rect.width / 5
    log_pane_height = window_rect.height / 6

    # Calculate bottom pane dimensions
    bottom_pane_top = window_rect.bottom - bottom_pane_height
    bottom_pane_width = window_rect.width - side_pane_width

    # Calculate side pane dimension
    side_pane_left = window_rect.width - side_pane_width

    # Calculate main pane dimensions
    main_pane_width = window_rect.width - side_pane_width
    main_pane_height = window_rect.height - bottom_pane_height

    # Calculate log pane dimension
    log_pane_bottom = window_rect.height - log_y_margin

    # Create Rect Objects
    bottom_pane = pygame.Rect(0, bottom_pane_top, bottom_pane_width, bottom_pane_height)
    side_pane = pygame.Rect(side_pane_left, 0, side_pane_width, window_rect.height)
    main_pane = pygame.Rect(0,0, main_pane_width, main_pane_height)
    log_pane = pygame.Rect(0,0, log_pane_width, log_pane_height)

    # Align log pane within the side pane
    log_pane.midbottom = (side_pane.centerx, log_pane_bottom)

    # Create dictionary
    panes = {'bottom': bottom_pane,
             'side': side_pane,
             'log': log_pane,
             'main': main_pane}

    # Return dictionary
    return panes


def drawStatPane(window, player, pane):
    """Draws the players statistics on the right side of the screen"""


    background_color = COLORS['DARK GRAY']
    font_color = COLORS['WHITE']

    # Fills in the pane in black
    pygame.draw.rect(window, background_color, pane, 0)

    X_MARGIN = pane.width/10
    Y_MARGIN = pane.height/25

    # Strings used
    full_name = player.name + " the " + player.background
    experience = "XL: %d" % player.level
    defense = "Defense: %d" % player.getDefense()
    life = "Life: %d" % player.life

    # Dictionary of text surfaces that will be blitted to the screen
    text_surfs = dict()

    text_surfs['name'] = FONTS['INFO'].render(full_name, True, font_color, background_color)
    text_surfs['xp'] = FONTS['INFO'].render(experience, True, font_color, background_color)
    text_surfs['defense'] = FONTS['INFO'].render(defense, True, font_color, background_color)
    text_surfs['life'] = FONTS['INFO'].render(life, True, font_color, background_color)
    text_surfs['energy_key'] = FONTS['INFO'].render("Energy", True, font_color, background_color)

    # Create Dictionary of Rectangle objects for each rect
    text_rects = {surf: text_surfs[surf].get_rect() for surf in text_surfs}

    # Place rectangles
    text_rects['name'].midleft = (pane.left+X_MARGIN, Y_MARGIN)
    text_rects['xp'].topleft = (pane.left + X_MARGIN, text_rects['name'].bottom + FONTS['INFO'].get_linesize())
    text_rects['defense'].topleft = (pane.left+X_MARGIN, text_rects['xp'].bottom)
    text_rects['life'].topleft = (pane.left + X_MARGIN, text_rects['defense'].bottom)

    for text in text_surfs:
        window.blit(text_surfs[text], text_rects[text])


def drawLogPane(window, log, pane):
    """Draws the messages on the bottom pane of the screen"""
    # Fills in the pane in black
    # 0 represents the width; if zero fills in rect
    pygame.draw.rect(window, COLORS['WHITE'], pane, 0)

    # Adds a Margin to the top and left side of the messages box
    X_MARGIN = 10
    Y_MARGIN = 5
    log_left = pane.left + X_MARGIN
    log_top = pane.top + Y_MARGIN

    # Get tha last messages from the log
    messages = log.getLastMessages(8)

    # Create lists to store surfaces and rects
    text_surfs = list()
    text_rects = list()

    for line, message in enumerate(messages):

        # Create a surface and rect for each line of messages
        surf = FONTS['LOG'].render(message, True, COLORS['BLACK'], COLORS['WHITE'])
        rect = surf.get_rect()

        # Place rect based on line number
        rect.topleft = (log_left, log_top + FONTS['LOG'].get_linesize() * line)

        # Append surf and rect to list
        text_surfs.append(surf)
        text_rects.append(rect)

    # Blits all text surfaces to the location of their Rect
    for i, surf in enumerate(text_surfs):
        window.blit(surf, text_rects[i])



