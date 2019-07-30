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
from source.constants import COLORS, FONTS, FPS, BACKGROUNDS
from source.utilities import checkForQuit
from source.entities import Target
from source.floors import Floor

# todo have titleScreen use a background
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

    # Shows the name prompt
    name_prompt = FONTS['MAIN'].render("Name: ", True, COLORS['BLACK'])
    name_prompt_rect = name_prompt.get_rect()
    name_prompt_rect.midright = (window_rect.centerx, window_rect.height/6)

    name = ''

    bg_chosen_index = 0

    # Clear the events to ensure no keys previously pressed show up in the name
    pygame.event.clear()

    name_chosen = False
    while not name_chosen:
        window.fill(COLORS['WHITE'])
        window.blit(name_prompt, name_prompt_rect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN and name != '':
                    name_chosen = True

                # If Backspace, remove character
                elif event.key == K_BACKSPACE:
                    name = name[:-1]

                # If left or right, change chosen background index
                elif event.key in (K_KP4, K_LEFT) and bg_chosen_index > 0:
                    bg_chosen_index -= 1
                elif event.key in (K_KP6, K_RIGHT) and bg_chosen_index < len(BACKGROUNDS)-1:
                    bg_chosen_index += 1
                else:
                    name += event.unicode

        name_text = FONTS['MAIN'].render(name, True, COLORS['BLACK'])
        input_rect = name_text.get_rect()
        input_rect.midleft = (name_prompt_rect.right, name_prompt_rect.centery)

        window.blit(name_text, input_rect)
        drawClassSelect(window, BACKGROUNDS[bg_chosen_index])

        fps_clock.tick(FPS)
        pygame.display.flip()

    return name, BACKGROUNDS[bg_chosen_index]


def drawClassSelect(window, selected_class):
    """Draw the Class Selection Buttons"""
    assert selected_class in BACKGROUNDS

    window_rect = window.get_rect()

    x_margin = window_rect.width / 25

    # Button Dimensions
    button_width = (window_rect.width-x_margin*2) / len(BACKGROUNDS)
    button_height = window_rect.height / 3
    button_top = window_rect.height / 3
    border_thickness = 1

    for i, background in enumerate(BACKGROUNDS):

        # Identify colors for buttons and text
        if background == selected_class:
            button_color = COLORS['BLACK']
            text_color = COLORS['WHITE']
        else:
            button_color = COLORS['WHITE']
            text_color = COLORS['BLACK']

        # Render text for background and get associated rect
        background_text = FONTS['MAIN'].render(background, True, text_color, button_color)
        background_text_rect = background_text.get_rect()

        # Determine horizontal location for rect and create inner and outer
        left = x_margin + button_width*i
        border_rect = pygame.Rect(left, button_top, button_width, button_height)
        inner_rect = pygame.Rect(left+border_thickness, button_top+border_thickness, button_width-border_thickness, button_height-border_thickness)

        # Inner and outer Rect
        pygame.draw.rect(window, button_color, inner_rect, 0)
        pygame.draw.rect(window, COLORS['BLACK'], border_rect, border_thickness)

        # Draw text in center of button
        background_text_rect.center = border_rect.center
        window.blit(background_text, background_text_rect)

    # The vertical margin for the text
    text_margin = FONTS['SUBMAIN'].get_linesize()
    
    choose_prompt = FONTS['SUBMAIN'].render('Choose Background with arrow keys', True, COLORS['BLACK'], COLORS['WHITE'])
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

                # Used for moving downwards
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

                # Used for moving upwards
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

                elif event.key == K_i:
                    # todo write open inventory screen
                    turn_taken = False
                elif event.key == K_f:
                    turn_taken = targetScreen(window, fps_clock, game, panes)
                elif event.key == K_x:
                    # todo write explore screen
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

            # Also do stuff to the log
            game.log.write()
            game.log.addEOTUnderscore()

        if player.is_dead:
            run_game = False

        # Fill in the background of the window with black
        window.fill(COLORS['BLACK'])

        # Draw the side and log panes
        drawStatPane(window, player, panes['side'])
        drawLogPane(window, game.log, panes['log'])
        drawGamePane(window, game, panes['main'])
        pygame.draw.rect(window, COLORS['DARK GRAY'], panes['bottom'], 0)

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
    """Used for targeting ranged attack"""

    # Create aliases for player and floor
    player = game.player
    floor = player.location

    # Create target
    target = Target(floor, player.x, player.y)
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
                    if target.on_top_of is not None:
                        player.rangedAttack(target.on_top_of)
                        target_mode = False
                        turn_taken = True
                    else:
                        game.log.addMessage("Not A Valid Target")

        # Fill in the background of the window with black
        window.fill(COLORS['BLACK'])

        # Draw the side and log panes
        drawStatPane(window, player, panes['side'])
        drawLogPane(window, game.log, panes['log'])
        drawGamePane(window, game, panes['main'])
        pygame.draw.rect(window, COLORS['DARK GRAY'], panes['bottom'], 0)

        # Update the screen and wait for clock to tick; repeat the while loop
        pygame.display.update()
        fps_clock.tick(FPS)

    # Clean up target after no longer used
    target.remove()

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

    x_margin = pane.width/10
    y_margin = pane.height/25

    # Strings used
    full_name = player.name + " the " + player.background
    floor_number = "Floor : %d" % player.location.number
    experience = "XL: %d" % player.level
    defense = "Defense: %d" % player.getDefense()
    life = "Life: %d" % player.life
    energy_value = "%.1f / %d" % (player.energy, player.max_energy)

    # Dictionary of text surfaces that will be blitted to the screen
    text_surfs = dict()

    text_surfs['name'] = FONTS['INFO'].render(full_name, True, font_color, background_color)
    text_surfs['floor'] = FONTS['INFO'].render(floor_number, True, font_color, background_color)
    text_surfs['xp'] = FONTS['INFO'].render(experience, True, font_color, background_color)
    text_surfs['defense'] = FONTS['INFO'].render(defense, True, font_color, background_color)
    text_surfs['life'] = FONTS['INFO'].render(life, True, font_color, background_color)
    text_surfs['energy_key'] = FONTS['INFO'].render("Energy:", True, font_color, background_color)
    text_surfs['energy_value'] = FONTS['INFO'].render(energy_value, True, energy_value_font_color)

    # Create Dictionary of Rectangle objects for each rect
    text_rects = {surf: text_surfs[surf].get_rect() for surf in text_surfs}

    # Place rectangles
    text_rects['name'].midleft = (pane.left+x_margin, y_margin)
    text_rects['floor'].topleft = (pane.left + x_margin, text_rects['name'].bottom + FONTS['INFO'].get_linesize())
    text_rects['xp'].topleft = (pane.left+x_margin, text_rects['floor'].bottom)
    text_rects['defense'].topleft = (pane.left+x_margin, text_rects['xp'].bottom)
    text_rects['life'].topleft = (pane.left + x_margin, text_rects['defense'].bottom)
    text_rects['energy_key'].topleft = (pane.left + x_margin, text_rects['life'].bottom)
    # Energy Value is placed after energy bar

    # Define Energy Bar Dimensions
    energy_bar_width = pane.width/4
    energy_bar_height = FONTS['INFO'].get_linesize()
    energy_bar_left = text_rects['energy_key'].right + 20
    energy_bar_top = text_rects['energy_key'].top

    energy_bar = pygame.Rect(energy_bar_left, energy_bar_top, energy_bar_width, energy_bar_height)

    # Place Energy Value over the Energy Bar
    text_rects['energy_value'].center = energy_bar.center

    # Draw to Screen
    pygame.draw.rect(window, COLORS['WHITE'], energy_bar, 1)

    # Define Energy Fill
    energy_fill = energy_bar.copy()
    energy_fill.y += 1
    energy_fill.x += 1
    energy_fill.height -= 2
    energy_fill.width = (energy_bar.width - 2) * (player.energy / player.max_energy)

    # Draw Energy Fill to Screen
    pygame.draw.rect(window, COLORS['LIGHT BLUE'], energy_fill, 0)



    # todo figure out printing items to pane
    # Get Images of equipped weapons
    # item_images = dict()
    #
    # for item in player.inventory.equipped:
    #     if player[item] is not None:
    #         item_images[item] = player.inventory.equipped[item]
    #     except AttributeError:
    #         item_images[item] = pygame.Surface((32, 32))
    #
    # # Create Dictionary of Rects for the images
    # item_image_rects = {item: item_images[item].get_rect() for item in item_images}
    #
    # # Define Location of Images of Items
    # item_image_rects['weapon'].midleft = (pane.left+x_margin, pane.centery)
    #
    # # Draw picture of images
    # for item in item_images:
    #     window.blit(item_images[item], item_image_rects[item])

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


def drawGamePane(window, game, pane):
    """Draws on the game surface then blits game surface to the window"""

    # Pulls the player and current floor from the game object
    player = game.player
    floor = player.location

    # Run the draw method on floor
    floor.draw(game.surface)

    # Draw the entities in the map
    for entity in floor.entities:
        # Skip the player until the end
        if entity is player:
            continue
        if player.getFOV()[entity.y][entity.x]:
            # If the entity is in fov, mark as discovered, update last known coordinates, and draw
            entity.discovered = True
            entity.last_known_x = entity.x
            entity.last_known_y = entity.y
            entity.draw(game.surface)
        elif entity.discovered and not player.getFOV()[entity.last_known_y][entity.last_known_x]:
            # If the entity is not in fov but is discovered, draw at last known coordinates...
            # unless the last known coordinates are in FOV
            entity.drawAtLastKnown(game.surface)

    # Draw the player after all other entities
    player.draw(game.surface)

    # Draw Fog over the map
    floor.drawFog(game.surface)

    # Update the camera's position
    player.camera.update()

    # Create a Rect with the same dimensions as the camera; center it in the main pane
    game_area = player.camera.getRect().copy()
    game_area.center = pane.center

    # Blit everything on the game surface to the window
    window.blit(game.surface, game_area, player.camera.getRect())
