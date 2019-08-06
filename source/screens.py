"""Contains the screen functions and the draw functions that the screen function use

Functions:
    titleScreen(window, fps_clock)
    playerCreateScreen(window, fps_clock)
    drawClassSelect(window)
    mainGameScreen(window, fps_clock, game)
    gameOverScreen(window, fps_clock) 
    getPanes(window_rect) : Takes a pygame.Rect object representing the window and returns a dictionary of Rect Objects
    drawStatPane(window, player, pane) : Draws the player's statistic on the right side of the screen
    drawLogPane(window, log, pane) : Draws the messages in the log pane

"""


# Third Party
import pygame
from pygame.constants import *

# My Modules
from source.constants import COLORS, FONTS, FPS, BACKGROUNDS, CELL_SIZE
from source.utilities import checkForQuit
from source.entities import Target
from source.floors import Floor
from source.assets import Images
from source.formulas import getRangedHitChance, getMeleeHitChance


def titleScreen(window, fps_clock):
    """Displays the Title Screen. Runs its own while loop until the player hits enter to continue

    Parameters:
        window : pygame.Surface
            Where the content will get drawn to
        fps_clock : pygame.Clock
            Used to keep FPS Steady

    """

    # Gets background image
    bg_image = Images.getImage('Backgrounds', 'title')

    # Stores a rect representing the entire window. This is used for relative placement of surfaces
    window_rect = window.get_rect()

    # Flashing prompt shown near bottom of screen
    continue_prompt = FONTS['MAIN'].render("Press Enter to Continue", True, COLORS['YELLOW'])
    continue_prompt_rect = continue_prompt.get_rect()
    continue_prompt_rect.center = (window_rect.centerx, window_rect.height*(3/4))

    # Cover used to give the illusion of transparency to the Font surface
    continue_cover = pygame.Surface((continue_prompt_rect.width, continue_prompt_rect.height))
    continue_cover.fill(COLORS['BLACK'])

    # Sets variables for the alpha of the cover
    alpha_max = 245
    alpha_min = 25
    alpha_change_rate = 3

    # Sets the alpha, stores it in cover_alpha, and sets decrease_alpha to True
    continue_cover.set_alpha(alpha_max)
    cover_alpha = continue_cover.get_alpha()
    decrease_alpha = True

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
        if cover_alpha <= alpha_min:
            decrease_alpha = False
        elif cover_alpha >= alpha_max:
            decrease_alpha = True

        window.blit(bg_image, window_rect)

        # Blits continue_prompt, then cover over it
        window.blit(continue_prompt, continue_prompt_rect)
        window.blit(continue_cover, continue_prompt_rect)

        drawFPS(window, fps_clock)
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

    bg_image = Images.getImage('Backgrounds', 'starry')

    window_rect = window.get_rect()

    # Shows the name prompt
    name_prompt = FONTS['MAIN'].render("Name: ", True, COLORS['WHITE'])
    name_prompt_rect = name_prompt.get_rect()
    name_prompt_rect.center = (window_rect.centerx, window_rect.height/7)

    # Flashing prompt shown near bottom of screen
    continue_prompt = FONTS['MAIN'].render("Press Enter to Continue", True, COLORS['YELLOW'])
    continue_prompt_rect = continue_prompt.get_rect()
    continue_prompt_rect.center = (window_rect.centerx, window_rect.height*(6/7))

    # Cover used to give the illusion of transparency to the Font surface
    continue_cover = pygame.Surface((continue_prompt_rect.width, continue_prompt_rect.height))
    continue_cover.fill(COLORS['BLACK'])

    # Sets variables for the alpha of the cover
    alpha_max = 245
    alpha_min = 25
    alpha_change_rate = 3
    decrease_alpha = True

    continue_cover.set_alpha(alpha_max)
    cover_alpha = continue_cover.get_alpha()


    # Identify the input font
    # Since W seems to be the biggest character, we want to calculate the char_width based on that
    input_font = FONTS['MAIN']
    char_width = input_font.size("W")[0]

    # Initialize the name as an empty string
    name = ''
    max_name_length = 10

    # Input Area; The White Space Where Text is typed
    input_area = pygame.rect.Rect(0,
                                  name_prompt_rect.bottom + input_font.get_linesize() / 2,
                                  max_name_length * char_width,
                                  input_font.get_linesize())

    input_area.centerx = window_rect.centerx

    input_border = pygame.rect.Rect(input_area.left - 1,
                                    input_area.top - 1,
                                    input_area.width + 1,
                                    input_area.height + 1)

    # The index of the chosen background
    bg_chosen_index = 0

    # Clear the events to ensure no keys previously pressed show up in the name
    pygame.event.clear()

    name_chosen = False
    while not name_chosen:

        # Blit background image
        window.blit(bg_image, window_rect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN and name != '':
                    name_chosen = True
                    break

                # If Backspace, remove character
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                    continue

                # If left or right, change chosen background index
                elif event.key in (K_KP4, K_LEFT):
                    if bg_chosen_index > 0:
                        bg_chosen_index -= 1
                    continue

                elif event.key in (K_KP6, K_RIGHT):
                    if bg_chosen_index < len(BACKGROUNDS)-1:
                        bg_chosen_index += 1
                    continue

                elif len(name) < max_name_length:
                    name += event.unicode

        # Decreases or increases alpha of cover
        if decrease_alpha:
            continue_cover.set_alpha(cover_alpha - alpha_change_rate)
        else:
            continue_cover.set_alpha(cover_alpha + alpha_change_rate)

        # Checks if alpha has reached minimum or maximum
        cover_alpha = continue_cover.get_alpha()
        if cover_alpha <= alpha_min:
            decrease_alpha = False
        elif cover_alpha >= alpha_max:
            decrease_alpha = True

        # If there is at least 1 character in the name, show Continue Prompt
        if len(name) > 0:
            window.blit(continue_prompt, continue_prompt_rect)
            window.blit(continue_cover, continue_prompt_rect)

        # Render the name that the player has typed and place it in the center of the Input Area
        input_text = input_font.render(name, True, COLORS['BLACK'])
        input_rect = input_text.get_rect()
        input_rect.center = input_area.center

        # Draw input area and border
        pygame.draw.rect(window, COLORS['WHITE'], input_area)
        pygame.draw.rect(window, COLORS['RED'], input_border, 1)

        # Blit name prompt and typed name
        window.blit(name_prompt, name_prompt_rect)
        window.blit(input_text, input_rect)

        # Draw Class Selections
        drawClassSelect(window, BACKGROUNDS[bg_chosen_index])

        fps_clock.tick(FPS)
        drawFPS(window, fps_clock)
        pygame.display.flip()

    return name, BACKGROUNDS[bg_chosen_index]


def drawClassSelect(window, selected_class):
    """Draw the Class Selection Buttons"""
    assert selected_class in BACKGROUNDS

    window_rect = window.get_rect()

    left_margin = window_rect.width / 25

    # Button Dimensions
    button_width = (window_rect.width-left_margin*2) / len(BACKGROUNDS)
    button_height = window_rect.height / 3
    button_top = window_rect.height / 3
    border_thickness = 1

    for i, background in enumerate(BACKGROUNDS):

        # Identify colors for buttons and text
        if background == selected_class:
            button_color = COLORS['WHITE']
            text_color = COLORS['BLACK']
        else:
            button_color = COLORS['BLACK']
            text_color = COLORS['WHITE']

        # Render text for background and get associated rect
        background_text = FONTS['MAIN'].render(background, True, text_color, button_color)
        background_text_rect = background_text.get_rect()

        # Determine horizontal location for rect and create inner and outer
        left = left_margin + button_width*i
        border_rect = pygame.Rect(left, button_top, button_width, button_height)
        inner_rect = pygame.Rect(left+border_thickness, button_top+border_thickness, button_width-border_thickness, button_height-border_thickness)

        # Inner and outer Rect
        if background == selected_class:
            pygame.draw.rect(window, button_color, inner_rect, 0)
        pygame.draw.rect(window, COLORS['RED'], border_rect, border_thickness)

        # Draw text in center of button
        background_text_rect.center = border_rect.center
        window.blit(background_text, background_text_rect)

    # The vertical margin for the text
    text_margin = FONTS['SUBMAIN'].get_linesize()
    
    choose_prompt = FONTS['SUBMAIN'].render('Choose Background with arrow keys', True, COLORS['WHITE'], COLORS['BLACK'])
    choose_rect = choose_prompt.get_rect()
    choose_rect.midtop = (window_rect.centerx, border_rect.bottom + text_margin)

    window.blit(choose_prompt, choose_rect)


def generateDungeonScreen(window):
    """A loading screen for generating the dungeon. Returns the dungeon"""
    window_rect = window.get_rect()

    # Text and Background colors
    text_color = COLORS['WHITE']
    bg_color = COLORS['BLACK']

    # Prompt
    window.fill(bg_color)
    prompt = FONTS['MAIN'].render("Generating Dungeon...",  True, text_color, bg_color)
    prompt_rect = prompt.get_rect()
    prompt_rect.center = window_rect.center

    window.blit(prompt, prompt_rect)

    pygame.display.flip()

    # Generate a dungeon with a specified number of floors
    dungeon = Floor.generateDungeon(num_of_floors=100)

    return dungeon


def mainGameScreen(window, fps_clock, game):
    """runs the main game loop as long as the run_game boolean is true"""
    window_rect = window.get_rect()
    
    # Pulls the player from the game object
    player = game.player

    # Gets a dict of Rects
    panes = getPanes(window_rect)

    # game loop
    run_game = True
    while run_game:

        # Turns true if player does an action that uses up their turn
        turn_taken = False

        # Event Handler
        checkForQuit()
        for event in pygame.event.get():

            # Determine what to do with Key Presses
            if event.type == KEYDOWN:
                # A Key press assumes turn taken until decided otherwise
                turn_taken = True

                # Movement Keys
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

                # Wait Key
                elif event.key == K_KP5:
                    pass

                # Down Portal Key
                elif event.unicode == ">":
                    # Check if player is on down portal
                    if player.x == player.location.portals['down'].x and player.y == player.location.portals['down'].y:

                        # If the player is on the last floor, game won
                        if player.location.number == len(game.dungeon):
                            # todo make Game won screen
                            pass
                        else:
                            new_floor = game.dungeon[player.location.number]
                            player.changeFloors(new_floor, "down")
                            game.surface.fill(COLORS['BLACK'])

                    # If the player does not move, turn is not taken
                    else:
                        turn_taken = False

                # Up Portal Key
                elif event.unicode == "<":
                    # Check if player is on up portal
                    if player.x == player.location.portals['up'].x and player.y == player.location.portals['up'].y:

                        # If the player is on the first floor, game over
                        if player.location.number == 1:
                            run_game = False

                        # Otherwise, move the player to the previous floor
                        else:
                            new_floor = game.dungeon[player.location.number-2]

                            player.changeFloors(new_floor, "up")
                            game.surface.fill(COLORS['BLACK'])

                    # If the player does not move, turn is not taken
                    else:
                        turn_taken = False

                # Inventory Key
                elif event.key == K_i:
                    # todo write open inventory screen
                    turn_taken = False

                # Fire Key
                elif event.key == K_f:
                    if not player.getEnergyPerShot() > player.energy:
                        turn_taken = targetScreen(window, fps_clock, game, panes)
                    else:
                        game.log.addMessage("Not enough energy")
                        turn_taken = False

                # Pick Up Key
                # todo be able to choose from a list of items to pick up
                elif event.key == K_g:
                    items = player.getItemsAtFeet()
                    if len(items) > 0:
                        items[0].pickUp(player.inventory)
                        game.log.addMessage("%s picked up a %s" % (player.name, items[0].name))
                    else:
                        game.log.addMessage("Nothing to pick up here")

                # Explore Key
                elif event.key == K_x:
                    # todo write explore screen
                    turn_taken = False
                
                # Look Key
                elif event.key == K_l:
                    # todo write look functionality
                    message = player.lookAround()
                    turn_taken = False

                else:
                    turn_taken = False

        # If turn was taken...
        if turn_taken:
            # iterate through all entities in the entities list
            for entity in player.location.entities:
                #  every entity with an AI takes a turn
                if entity.ai:
                    entity.ai.takeTurn()
                # Recharge all equipped generators
                if entity.inventory and entity.inventory.equipped['generator']:
                    entity.inventory.equipped['generator'].recharge()
                    entity.inventory.equipped['generator'].hit_this_turn = False

            # See what the player can see
            player.calculateFOV()
            player.discoverTiles()

            # Write whats in the log's buffer and add an underscore
            game.log.write()
            game.log.addEOTUnderscore()

        if player.is_dead:
            run_game = False
            game.log.addMessage("You Died!")
            game.log.addMessage("Press Enter to Continue...")

        # Fill in the background of the window with black
        window.fill(COLORS['BLACK'])

        # Draw the side and log panes
        drawStatPane(window, player, panes['side'])
        drawLogPane(window, game.log, panes['log'])
        drawGamePane(window, game, panes['main'])
        drawFPS(window, fps_clock)
        pygame.draw.rect(window, COLORS['DARK GRAY'], panes['bottom'], 0)

        # Update the screen and wait for clock to tick; repeat the while loop
        pygame.display.update()
        fps_clock.tick()

    # Stop until player hit enter key
    show_screen = True
    while show_screen:
        checkForQuit()
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_RETURN:
                show_screen = False



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
    text_rect.center = window_rect.center

    window.blit(text, text_rect)
    show_game_over = True

    while show_game_over:
        checkForQuit()
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_RETURN:
                show_game_over = False

        pygame.display.flip()
        fps_clock.tick(FPS)


def targetScreen(window, fps_clock, game, panes):
    """Used for targeting ranged attack

    Returns : bool : Whether ot not a turn was taken"""

    # Create aliases for player and floor
    player = game.player
    floor = player.location

    # Create target
    target = Target(floor, player.x, player.y, player)
    
    # Turn taken turns to True if player takes a shot
    turn_taken = False
    
    target_mode = True
    while target_mode:

        # Event Handler
        checkForQuit()
        for event in pygame.event.get():

            # Determine what to do with Key Presses
            if event.type == KEYDOWN:

                # Movement Keys
                if event.key == K_UP or event.key == K_KP8:
                    target.move(0, -1)
                elif event.key == K_DOWN or event.key == K_KP2:
                    target.move(0, 1)
                elif event.key == K_LEFT or event.key == K_KP4:
                    target.move(-1, 0)
                elif event.key == K_RIGHT or event.key == K_KP6:
                    target.move(1, 0)
                elif event.key == K_KP7:
                    target.move(-1, -1)
                elif event.key == K_KP9:
                    target.move(1, -1)
                elif event.key == K_KP1:
                    target.move(-1, 1)
                elif event.key == K_KP3:
                    target.move(1, 1)

                # Exit targeting
                elif event.key == K_ESCAPE:
                    target_mode = False

                # Shoot
                elif event.key in (K_f, K_RETURN):
                    if target.getFirstInPath() is not None:
                        player.attack(target.getFirstInPath(), is_ranged=True)
                        target_mode = False
                        turn_taken = True
                    else:
                        game.log.addMessage("Not A Valid Target")

        # Fill in the background of the window with black
        window.fill(COLORS['BLACK'])

        # Draw the side, log and game panes
        drawStatPane(window, player, panes['side'])
        drawLogPane(window, game.log, panes['log'])
        drawGamePane(window, game, panes['main'], target)
        drawFPS(window, fps_clock)
        pygame.draw.rect(window, COLORS['DARK GRAY'], panes['bottom'], 0)

        # Update the screen and wait for clock to tick; repeat the while loop
        pygame.display.update()
        fps_clock.tick()

    # Clean up target after no longer used
    target.remove()

    # Return bool determining if turn was taken
    return turn_taken


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
    main_pane = pygame.Rect(0, 0, main_pane_width, main_pane_height)
    log_pane = pygame.Rect(0, 0, log_pane_width, log_pane_height)

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
    """Draws the players statistics on the right side of the screen

    Parameters:
        window : pygame.Surface
        player : Player
        pane : pygame.Rect
    """

    # Define the colors used
    background_color = COLORS['DARK GRAY']
    font_color = COLORS['WHITE']
    energy_value_font_color = COLORS['GOLDENROD']

    # Fills in the pane in black
    pygame.draw.rect(window, background_color, pane, 0)
    
    #todo use linesizes throughout function
    # Get linesizes
    header_size = FONTS['INFO_HEADER'].get_linesize()
    line_size = FONTS['INFO'].get_linesize()

    half_line_size = line_size/2

    x_margin = pane.width/10
    y_margin = pane.height/25
    
    # todo use indent_left to reduce repeated arithmetic
    indent_left = pane.left + x_margin

    # Stats used multiple times
    eps = player.getEnergyPerShot()
    enc = player.getEncumbrance()

    # Strings used
    full_name = player.name + " the " + player.background
    floor_number = "Floor : %d" % player.location.number
    experience = "XL: %d" % player.level
    defense = "Defense: %d" % player.getDefense()
    life = "Life: %d" % player.life
    energy_value = "%.1f / %d" % (player.energy, player.max_energy)
    # Ranged Stats
    str_eps = "EPS: %.1f (%.1f)" % (eps, eps - player.getRecoilCharge())
    r_dmg = "DMG: %.1f" % player.getRangedDamage()
    r_ar = "AR:  %d" % player.getAttackRate(is_ranged=True)
    r_acc = "ACC: %d%%" % (100 * getRangedHitChance(enc, 0, 0))
    rng = "RNG: %d" % player.getRange()
    # Melee Stats
    m_dmg = "DMG: %.1f" % player.getMeleeDamage()
    m_ar = "AR:  %d" % player.getAttackRate(is_ranged=False)
    m_acc = "ACC: %d%%" % (100 * getMeleeHitChance(enc, 0))

    # Dictionary of text surfaces that will be blitted to the screen
    text_surfs = dict()

    text_surfs['name'] = FONTS['INFO'].render(full_name, True, font_color, background_color)
    text_surfs['floor'] = FONTS['INFO'].render(floor_number, True, font_color, background_color)
    text_surfs['xp'] = FONTS['INFO'].render(experience, True, font_color, background_color)
    text_surfs['defense'] = FONTS['INFO'].render(defense, True, font_color, background_color)
    text_surfs['life'] = FONTS['INFO'].render(life, True, font_color, background_color)
    text_surfs['energy_key'] = FONTS['INFO'].render("Energy:", True, font_color, background_color)
    
    text_surfs['energy_value'] = FONTS['INFO'].render(energy_value, True, energy_value_font_color)
    
    text_surfs['ranged'] = FONTS['INFO_HEADER'].render("Ranged", True, font_color, background_color)
    text_surfs['r_dmg'] = FONTS['INFO'].render(r_dmg, True, font_color, background_color)
    text_surfs['r_ar'] = FONTS['INFO'].render(r_ar, True, font_color, background_color)
    text_surfs['r_acc'] = FONTS['INFO'].render(r_acc, True, font_color, background_color)
    text_surfs['r_rng'] = FONTS['INFO'].render(rng, True, font_color, background_color)
    text_surfs['r_eps'] = FONTS['INFO'].render(str_eps, True, font_color, background_color)
    
    text_surfs['melee'] = FONTS['INFO_HEADER'].render("Melee", True, font_color, background_color)
    text_surfs['m_dmg'] = FONTS['INFO'].render(m_dmg, True, font_color, background_color)
    text_surfs['m_ar'] = FONTS['INFO'].render(m_ar, True, font_color, background_color)
    text_surfs['m_acc'] = FONTS['INFO'].render(m_acc, True, font_color, background_color)   

    # Create Dictionary of Rectangle objects for each rect
    text_rects = {surf: text_surfs[surf].get_rect() for surf in text_surfs}

    # Place rectangles
    text_rects['name'].midleft = (indent_left, y_margin)
    text_rects['floor'].topleft = (indent_left, text_rects['name'].bottom + line_size)
    text_rects['xp'].topleft = (indent_left, text_rects['floor'].bottom + half_line_size)
    text_rects['energy_key'].topleft = (indent_left, text_rects['xp'].bottom + half_line_size)
    text_rects['life'].topleft = (indent_left, text_rects['energy_key'].bottom + half_line_size)
    text_rects['defense'].topleft = (pane.centerx, text_rects['life'].top)
    # Energy Value is placed after energy bar
    
    # Draw Line Separating top stats from damage stats
    line_y = text_rects['life'].bottom + header_size
    line_start = indent_left
    line_end = pane.right-x_margin
    line_width = 1
    pygame.draw.line(window, COLORS['BLACK'], (line_start, line_y), (line_end, line_y), line_width)
    
    # Place Ranged Stats
    text_rects['ranged'].topleft = (indent_left, line_y + header_size)
    text_rects['r_dmg'].topleft = (indent_left, text_rects['ranged'].bottom + half_line_size)
    text_rects['r_ar'].topleft = (indent_left, text_rects['r_dmg'].bottom + half_line_size)
    text_rects['r_acc'].topleft = (indent_left, text_rects['r_ar'].bottom + half_line_size)
    text_rects['r_rng'].topleft = (indent_left, text_rects['r_acc'].bottom + half_line_size)
    text_rects['r_eps'].topleft = (indent_left, text_rects['r_rng'].bottom + half_line_size)
    
    # Place Melee Stats
    text_rects['melee'].topleft = (pane.centerx, text_rects['ranged'].top)
    text_rects['m_dmg'].topleft = (pane.centerx, text_rects['r_dmg'].top)
    text_rects['m_ar'].topleft = (pane.centerx, text_rects['r_ar'].top)
    text_rects['m_acc'].topleft = (pane.centerx, text_rects['r_acc'].top)

    # Define Energy Bar Dimensions
    energy_bar_width = pane.width/4
    energy_bar_height = line_size
    energy_bar_left = text_rects['energy_key'].right + 20
    energy_bar_top = text_rects['energy_key'].top

    energy_bar = pygame.Rect(energy_bar_left, energy_bar_top, energy_bar_width, energy_bar_height)

    # Place Energy Value over the Energy Bar
    text_rects['energy_value'].center = energy_bar.center

    # Draw to Screen
    pygame.draw.rect(window, COLORS['WHITE'], energy_bar, 1)

    # Define Energy Fill, A bar that is proportionate to the amount of energy remaining
    energy_fill = energy_bar.copy()
    energy_fill.y += 1
    energy_fill.x += 1
    energy_fill.height -= 2
    try:
        energy_fill.width = (energy_bar.width - 2) * (player.energy / player.max_energy)
    except ZeroDivisionError:
        energy_fill.width = 0

    # Draw Energy Fill to Screen
    pygame.draw.rect(window, COLORS['LIGHT BLUE'], energy_fill, 0)

    # Get the equipment and creates two dictionaries: one for images, one for names
    equipment = player.inventory.equipped
    item_images = dict()
    item_names = dict()
    for slot in equipment:
        if equipment[slot] is not None:
            item_images[slot] = equipment[slot].image
            item_names[slot] = equipment[slot].name
        else:
            item_images[slot] = pygame.Surface((CELL_SIZE, CELL_SIZE))
            item_names[slot] = "None"

    # Create dict for rects of the item images
    item_image_rects = {item: item_images[item].get_rect() for item in item_images}

    # The distance between the images
    image_dist = CELL_SIZE*3

    item_text_surfs = dict()
    item_text_rects = dict()

    # Place the rects for the images, amd render text associated with them
    for i, slot in enumerate(item_image_rects):
        item_image_rects[slot].midright = (pane.centerx, pane.centery + (i*image_dist))
        line_y = item_image_rects[slot].top - CELL_SIZE*3/2
        line_start = pane.left+x_margin
        line_end = pane.right-x_margin
        pygame.draw.line(window, COLORS['BLACK'], (line_start, line_y), (line_end, line_y), 1)

        # Title text
        title_top = line_y + CELL_SIZE/2
        item_text_surfs[slot+'_title'] = FONTS['INFO'].render(slot.capitalize(), True, font_color, background_color)
        item_text_rects[slot+'_title'] = item_text_surfs[slot+'_title'].get_rect()
        item_text_rects[slot+'_title'].midtop = (pane.centerx, title_top)

        # Name text
        item_text_surfs[slot+'_name'] = FONTS['LOG'].render(item_names[slot], True, font_color, background_color)
        item_text_rects[slot+'_name'] = item_text_surfs[slot+'_name'].get_rect()
        item_text_rects[slot+'_name'].midleft = (pane.centerx, item_image_rects[slot].centery)

    # Draw picture of images and the associated text
    for item in item_images:
        window.blit(item_images[item], item_image_rects[item])
        window.blit(item_text_surfs[item+'_title'], item_text_rects[item+'_title'])
        window.blit(item_text_surfs[item+'_name'], item_text_rects[item+'_name'])

    # Print Text
    for text in text_surfs:
        window.blit(text_surfs[text], text_rects[text])


def drawLogPane(window, log, pane):
    """Draws the messages in the log pane"""
    # Fills in the pane in black
    # 0 represents the width; if zero fills in rect
    pygame.draw.rect(window, COLORS['WHITE'], pane, 0)

    # Adds a Margin to the top and left side of the messages box
    x_margin = 10
    y_margin = 5
    log_left = pane.left + x_margin
    log_top = pane.top + y_margin

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


def drawGamePane(window, game, pane, target=None):
    """Draws on the game surface then blits game surface to the window"""

    # Pulls the player and current floor from the game object
    player = game.player
    floor = player.location

    # Run the draw method on floor
    floor.draw(game.surface, player.camera)

    # Update the camera's position
    player.camera.update()

    # Create a Rect with the same dimensions as the camera; center it in the main pane
    game_area = player.camera.getRect().copy()
    game_area.center = pane.center

    if target:
        target.drawPath(game.surface)

    # Blit everything on the game surface to the window
    window.blit(game.surface, game_area, player.camera.getRect())


def drawFPS(window, fps_clock):
    window_rect = window.get_rect()

    fps = int(fps_clock.get_fps())

    x_margin = 19
    y_margin = 10

    fps_surf = FONTS['SUBMAIN'].render(str(fps), True, COLORS['GRAY'])
    fps_rect = fps_surf.get_rect()
    fps_rect.topleft = (window_rect.left + x_margin, window_rect.top + y_margin)

    window.blit(fps_surf, fps_rect)
