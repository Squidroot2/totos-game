"""Contains the screen functions which update the display to show different things to the player

Functions:
    titleScreen(window, fps_clock)
    playerCreateScreen(window, fps_clock)
    mainGameScreen(window, fps_clock, game)
    gameOverScreen(window, fps_clock)
    targetScreen(window, fps_clock, game, panes)
    inventoryScreen(window, fps_clock, game, panes)
"""

# Standard Library
import os.path

# Third Party
import pygame
from pygame.constants import *

# My Modules
from source.constants import COLORS, FONTS, FPS, BACKGROUNDS
from source.draw import drawClassSelect, getPanes, drawMapPane, drawGamePane, drawFPS, drawInventory, \
                        drawAllPanes, drawItemInfo, drawMainMenu
from source.quit import checkForQuit, SAVE_LOCATION
from source.entities import Target
from source.floors import Floor
from source.assets import Images, Fonts


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
    continue_prompt = Fonts.presets['main'].render("Press Enter to Continue", True, COLORS['YELLOW'])
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
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN:
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


def mainMenuScreen(window, fps_clock):
    """Shows the main menu"""

    choices = ("New Game", "Load Game", "How To Play", "Quit")
    selected_index = 0

    # GRAY OUT
    grey_out = {'How To Play'}
    if not os.path.exists(SAVE_LOCATION):
        grey_out.add("Load Game")

    option_chosen = False
    while not option_chosen:
        drawMainMenu(window, selected_index, choices, grey_out)
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in (K_KP2, K_DOWN) and selected_index < (len(choices)-1):
                    selected_index += 1
                    continue
                elif event.key in (K_KP8, K_UP) and selected_index > 0:
                    selected_index -= 1
                    continue
                elif event.key == K_RETURN:
                    if choices[selected_index] in grey_out:
                        continue
                    option_chosen = True

        pygame.display.flip()
        fps_clock.tick(FPS)

    return choices[selected_index]


def playerCreateScreen(window, fps_clock):
    """Displays the player creation window where the player can choose their name and class

    Parameters:
        window : pygame.Surface
            Where the content will get drawn to
        fps_clock : pygame.Clock
            Used to keep FPS Steady

    Returns: string, string : Chosen name of the player character and chosen background
    """

    bg_image = Images.getImage('Backgrounds', 'starry')

    window_rect = window.get_rect()

    main_font = Fonts.presets['main']

    # Shows the name prompt
    name_prompt = main_font.render("Name: ", True, COLORS['WHITE'])
    name_prompt_rect = name_prompt.get_rect()
    name_prompt_rect.center = (window_rect.centerx, window_rect.height/7)

    # Flashing prompt shown near bottom of screen
    continue_prompt = main_font.render("Press Enter to Continue", True, COLORS['YELLOW'])
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
    input_font = main_font
    char_width = input_font.size("W")[0]

    # Initialize the name as an empty string
    name = ''
    max_name_length = 15

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
                # If Return, and valid name, keep name
                if event.key == K_RETURN:
                    if name != '':
                        name_chosen = True
                        break
                    continue

                # If Backspace, remove character
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                    continue

                # Move chosen background index to the left
                elif event.key in (K_KP4, K_LEFT):
                    if bg_chosen_index > 0:
                        bg_chosen_index -= 1
                    continue
                # Move chosen background index to the right
                elif event.key in (K_KP6, K_RIGHT):
                    if bg_chosen_index < len(BACKGROUNDS)-1:
                        bg_chosen_index += 1
                    continue

                # Escape to Cancel the player creation
                elif event.key == K_ESCAPE:
                    return None, None

                # Add characters as long as less than max_name length
                elif len(name) < max_name_length:
                    if event.key != K_TAB:
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

    # Initial draw to screen
    drawAllPanes(window, game, panes)

    # game loop
    run_game = True
    while run_game:

        # Event Handler
        checkForQuit(game)
        for event in pygame.event.get():

            # Determine what to do with Key Presses
            if event.type == KEYDOWN:
                # A Key press assumes turn taken until decided otherwise
                turn_taken = True

                # Clears the message
                message = None

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

                # Rest Key
                elif event.key == K_KP0:
                    while not player.getEnemiesinFOV() and player.energy < player.max_energy:
                        for entity in player.location.entities:
                            #  every entity with an AI takes a turn
                            if entity.ai:
                                entity.ai.takeTurn()
                            # Recharge all equipped reactors
                            if entity.inventory and entity.inventory.equipped['reactor']:
                                entity.inventory.equipped['reactor'].recharge()
                                entity.inventory.equipped['reactor'].hit_this_turn = False

                        drawAllPanes(window, game, panes, message=message)
                        pygame.display.update()
                        fps_clock.tick(FPS)

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

                    # If the player does not move, turn is not taken
                    else:
                        turn_taken = False

                # Inventory Key
                elif event.key == K_i:
                    turn_taken = inventoryScreen(window, fps_clock, game, panes)

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
                    if len(player.inventory.contents) < player.inventory.capacity:
                        items = player.getItemsAtFeet()
                        if len(items) > 0:
                            items[0].pickUp(player.inventory)
                            game.log.addMessage("%s picked up a %s" % (player.name, items[0].name))
                        else:
                            game.log.addMessage("Nothing to pick up here")
                    else:
                        game.log.addMessage("Inventory is Full")
                        turn_taken = False

                # Explore Key
                elif event.key == K_x:
                    # todo write explore screen
                    turn_taken = False
                
                # Look Key
                elif event.key == K_l:
                    if message:
                        message = None
                    else:
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
                        # Recharge all equipped reactors
                        if entity.inventory and entity.inventory.equipped['reactor']:
                            entity.inventory.equipped['reactor'].recharge()
                            entity.inventory.equipped['reactor'].hit_this_turn = False

                    # See what the player can see
                    player.calculateFOV()
                    player.discoverTiles()

                    # Write whats in the log's buffer and add an underscore
                    game.log.write()
                    game.log.addEOTUnderscore()

                    if player.is_dead:
                        run_game = False
                        message = "You Died!"
                        game.log.addMessage("Press Enter to Continue...")

                # END IF TURN TAKEN

                drawAllPanes(window, game, panes, message=message)

            # END FOR KEYDOWN EVENT LOOP
        # END FOR EVENT LOOP

        # If there are projectiles, draw their animation until there there are no projectiles
        if player.location.projectiles:
            while player.location.projectiles:
                pygame.draw.rect(window, COLORS['BLACK'], panes['main'])
                drawGamePane(window, game, panes['main'])
                drawMapPane(window, player, player.location, panes['map'])
                pygame.display.update()
                fps_clock.tick(FPS)
            # Draw one more time to clear the projectile
            pygame.draw.rect(window, COLORS['BLACK'], panes['main'])
            drawGamePane(window, game, panes['main'])
            drawMapPane(window, player, player.location, panes['map'])
        
        # Update the screen and wait for clock to tick; repeat the while loop
        pygame.display.update()
        fps_clock.tick()

    # END WHILE RUN GAME
    # Stop until player hit enter key
    show_screen = True
    while show_screen:
        checkForQuit()
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_RETURN:
                show_screen = False

    gameOverScreen(window, fps_clock)


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
        checkForQuit(game)
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

            drawAllPanes(window, game, panes, target=target)

        # drawFPS(window, fps_clock)
        # Update the screen and wait for clock to tick; repeat the while loop
        pygame.display.update()
        fps_clock.tick()

    # Clean up target after no longer used
    target.remove()

    # Return bool determining if turn was taken
    return turn_taken


def inventoryScreen(window, fps_clock, game, panes):
    """Used for drawing the inventory

    Returns : bool : whether or not a turn was taken"""
    player = game.player

    drawAllPanes(window, game, panes)

    # drawInventory and get the item order
    selected_item = None
    item_order = drawInventory(window, panes['main'], player.inventory, selected_item)

    turn_taken = False

    show_inventory = True
    while show_inventory:

        # Event Handler
        checkForQuit(game)
        for event in pygame.event.get():

            # Determine what to do with Key Presses
            if event.type == KEYDOWN:

                if event.key in (K_ESCAPE, K_i):
                    show_inventory = False

                # If a Number key was pressed
                elif event.key in range(K_0, K_9+1):
                    # Converts the key pressed to an index 0-9
                    if event.key == K_0:
                        index = 9
                    else:
                        index = event.key - K_1

                    # If the number pressed is valid
                    if index < len(item_order):
                        # If the key corresponds to the item selected, deselect it
                        if selected_item is item_order[index]:
                            selected_item = None
                        else:
                            selected_item = item_order[index]

                        # Redraw Screen
                        drawAllPanes(window, game, panes)
                        drawInventory(window, panes['main'], player.inventory, selected_item)

                    # END IF INDEX LESS THAN LENGTH OF ITEM ORDER

                # Item Actions:
                if selected_item is not None:
                    if event.key == K_u:
                        if selected_item in player.inventory.equipped.values():
                            selected_item.unequip()
                            show_inventory = False
                            turn_taken = False
                            break

                    elif event.key == K_e:
                        if selected_item.item_class != "battery" and \
                                selected_item not in player.inventory.equipped.values():
                            selected_item.equip()
                            show_inventory = False
                            if selected_item.item_class == 'weapon' and selected_item.is_quick_draw:
                                turn_taken = False
                            else:
                                turn_taken = True
                            break

                    elif event.key == K_s:
                        if selected_item.item_class == "battery":
                            selected_item.use()
                            show_inventory = False
                            turn_taken = True
                            break

                    elif event.key == K_d:
                        selected_item.drop()
                        show_inventory = False
                        break

                # If Item selected, draw its info
                if selected_item:
                    drawItemInfo(window, panes['main'], selected_item)

            # END IF KEYDOWN EVENT

        # END FOR EVENT LOOP
        pygame.display.update()
        fps_clock.tick()

    # END WHILE SHOW INVENTORY
    return turn_taken
