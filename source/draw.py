"""Contains functions that draw or assist in drawing things to the window

Functions:
    drawClassSelect(window, selected_class) : Draws the class selection buttons
    getPanes(window_rect) : Takes a pygame.Rect object representing the window and returns a dictionary of Rect Objects
    drawStatPane(window, player, pane) : Draws the player's statistic on the right side of the screen
    drawLogPane(window, log, pane) : Draws the messages in the log pane
    drawGamePane(window, game, pane, target=None, message=None) : Draws on the game surface then blits game surface to the window
    drawFPS(window, fps_clock) : Draws the FPS in the top right of the screen
    drawFillBar(window, pane, y_axis, height, fill_percent, fill_color, outline_color=COLORS['WHITE']) : Draws a bar filled to a specified percentage
    drawMessageBox(window, pane, message) : Draw a message box containing a specified message onto the game pane
 """

import pygame

from source.assets import Fonts, Images
from source.constants import BACKGROUNDS, COLORS, FONTS, CELL_SIZE, FLOOR_HEIGHT, FLOOR_WIDTH
from source.formulas import getRangedHitChance, getMeleeHitChance
from source.utilities import formatFloat


def drawMainMenu(window, selected_index, choices):
    window_rect = window.get_rect()

    font_color = COLORS['WHITE']

    bg_image = Images.getImage('Backgrounds', 'title')

    main_font = Fonts.presets['main']
    line_size = main_font.get_linesize()

    choice_top = window_rect.centery + 50

    text_dist = line_size * 2

    # Selector triangle dimensions
    triangle_length = 20
    triangle_x_margin = 10

    window.blit(bg_image, window_rect)

    for i, choice in enumerate(choices):
        choice_text = Fonts.presets['main'].render(choice, True, font_color)
        choice_rect = choice_text.get_rect()
        choice_rect.midtop = (window_rect.centerx, choice_top + (i * text_dist))

        window.blit(choice_text, choice_rect)

        if i == selected_index:
            # Triangle points
            tip = (choice_rect.left - triangle_x_margin, choice_rect.centery)
            base_top = (tip[0] - triangle_length, choice_rect.top)
            base_bottom = (tip[0] - triangle_length, choice_rect.bottom)

            # draw Selector triangle
            pygame.draw.polygon(window, COLORS['YELLOW'], (tip, base_top, base_bottom), 0)


def drawClassSelect(window, selected_class):
    """Draw the Class Selection Buttons
    
    Parameters: 
        window : pygame.Surface
        selected_class : string
    """
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
        inner_rect = pygame.Rect(left+border_thickness, button_top+border_thickness,
                                 button_width-border_thickness, button_height-border_thickness)

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


def getPanes(window_rect):
    """Takes a pygame.Rect object representing the window and returns a dictionary of Rect Objects for the four panes
    of the mainGameScreen
    
    Parameters:
        window_rect : pygame.Rect
    
    Returns : dict{string : pygame.Rect}
    """

    # log pane margin from bottom
    log_y_margin = 10

    # Map pane margins
    map_y_margin = 20
    map_x_margin = 20

    # Map scale
    map_scale = 3

    # Explicit variables for the size of the panes
    bottom_pane_height = window_rect.height / 25
    side_pane_width = window_rect.width / 4
    log_pane_width = window_rect.width / 4.4
    log_pane_height = window_rect.height / 4

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

    # Calculate map pane dimension
    map_pane_left = side_pane_left - FLOOR_WIDTH*map_scale - map_x_margin

    # Create Rect Objects
    bottom_pane = pygame.Rect(0, bottom_pane_top, bottom_pane_width, bottom_pane_height)
    side_pane = pygame.Rect(side_pane_left, 0, side_pane_width, window_rect.height)
    main_pane = pygame.Rect(0, 0, main_pane_width, main_pane_height)
    log_pane = pygame.Rect(0, 0, log_pane_width, log_pane_height)
    map_pane = pygame.Rect(map_pane_left, map_y_margin, FLOOR_WIDTH*map_scale, FLOOR_HEIGHT*map_scale)

    # Align log pane within the side pane
    log_pane.midbottom = (side_pane.centerx, log_pane_bottom)

    # Create dictionary
    panes = {'bottom': bottom_pane,
             'side': side_pane,
             'log': log_pane,
             'map': map_pane,
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
    xp_percent_font_color = COLORS['WHITE']

    # Fills in the pane in black
    pygame.draw.rect(window, background_color, pane, 0)

    # Get linesizes
    header_size = FONTS['INFO_HEADER'].get_linesize()
    line_size = FONTS['INFO'].get_linesize()

    half_line_size = line_size/2

    x_margin = pane.width/10
    y_margin = pane.height/25

    indent_left = pane.left + x_margin

    # Stats used multiple times
    eps = player.getEnergyPerShot()
    enc = player.getEncumbrance()
    percent_to_next_level = player.getPercentToNextLevel()
    if player.getRecoveryTime():
        recovery_left = "(%d)" % player.getRecoveryTime()
    else:
        recovery_left = ""

    # Strings used
    full_name = player.name + " the " + player.background
    floor_number = "Floor : %d" % player.location.number
    experience = "XL: %d" % player.level
    xp_percent = "%.1f%%" % (100*percent_to_next_level)
    defense = "Defense: %d" % player.getDefense()
    life = "Life: %d" % player.life
    energy_value = "%.1f / %d" % (player.energy, player.max_energy)
    recharge = "Recharge: %s %s" % (formatFloat("%.2f", player.getChargeThisTurn()), recovery_left)
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
    text_surfs['recharge'] = FONTS['INFO'].render(recharge, True, font_color, background_color)

    text_surfs['xp_percent'] = FONTS['INFO_S'].render(xp_percent, True, xp_percent_font_color)
    text_surfs['energy_value'] = FONTS['INFO_S'].render(energy_value, True, energy_value_font_color)

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
    text_rects['xp_percent'].center = (pane.centerx, text_rects['xp'].centery)
    text_rects['energy_key'].topleft = (indent_left, text_rects['xp'].bottom + half_line_size)
    text_rects['energy_value'].center = (pane.centerx, text_rects['energy_key'].centery)
    text_rects['recharge'].topleft = (indent_left, text_rects['energy_key'].bottom + half_line_size)
    text_rects['life'].topleft = (indent_left, text_rects['recharge'].bottom + half_line_size)
    text_rects['defense'].topleft = (pane.centerx, text_rects['life'].top)

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

    try:
        energy_fill_percent = player.energy / player.max_energy
    except ZeroDivisionError:
        energy_fill_percent = 0

    drawFillBar(window, pane, y_axis=text_rects['energy_key'].centery, height=line_size,
                fill_percent=energy_fill_percent, fill_color=COLORS['LIGHT BLUE'])
    drawFillBar(window, pane, y_axis=text_rects['xp'].centery, height=line_size,
                fill_percent=percent_to_next_level, fill_color=COLORS['ORANGE'])

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

    # The interval used to space out item images
    image_interval = pane.width / 6   # Images are centered at 1/6, 3/6, and 5/6

    # Dicts for item text and rects
    item_text_surfs = dict()
    item_text_rects = dict()

    # Draw a line above the items
    line_y = text_rects['r_eps'].bottom + line_size
    line_end = pane.right - x_margin
    pygame.draw.line(window, COLORS['BLACK'], (indent_left, line_y), (line_end, line_y), 1)

    # Vertical lines separating the items
    vert_line_start = line_y + half_line_size
    vert_line_end = (line_y + line_size*4 + CELL_SIZE)
    line_dist = pane.width / len(equipment)

    # Place the rects for the images, amd render text associated with them
    for i, slot in enumerate(item_image_rects):

        # Title text
        # title_top = line_y + CELL_SIZE/2
        item_text_surfs[slot+'_title'] = FONTS['INFO'].render(slot.capitalize(), True, font_color, background_color)
        item_text_rects[slot+'_title'] = item_text_surfs[slot+'_title'].get_rect()
        item_text_rects[slot+'_title'].midtop = (pane.left + image_interval + (i*2*image_interval),
                                                 line_y + line_size)

        # Item Image
        item_image_rects[slot].midtop = (item_text_rects[slot+'_title'].centerx,
                                         item_text_rects[slot+'_title'].bottom + half_line_size)

        # Name text
        item_text_surfs[slot+'_name'] = FONTS['INFO_S'].render(item_names[slot], True, font_color, background_color)
        item_text_rects[slot+'_name'] = item_text_surfs[slot+'_name'].get_rect()
        item_text_rects[slot+'_name'].midtop = (item_image_rects[slot].centerx,
                                                item_image_rects[slot].bottom + half_line_size)

        # Line in between. Not drawn first time around
        if i > 0:
            vert_line_x = pane.left + line_dist * i
            pygame.draw.line(window, COLORS['BLACK'], (vert_line_x, vert_line_start),
                            (vert_line_x, vert_line_end), 2)

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
    pygame.draw.rect(window, COLORS['BLACK'], pane, 1)

    # Identity Font
    log_font = Fonts.presets['log']

    # Adds a Margin to the top and left side of the messages box
    x_margin = 10
    y_margin = 5
    log_left = pane.left + x_margin
    log_top = pane.top + y_margin

    # Get tha last messages from the log
    messages = log.getLastLines(12, 40)

    # Create lists to store surfaces and rects
    text_surfs = list()
    text_rects = list()

    for line, message in enumerate(messages):

        # Create a surface and rect for each line of messages
        surf = log_font.render(message, True, COLORS['BLACK'], COLORS['WHITE'])
        rect = surf.get_rect()

        # Place rect based on line number
        rect.topleft = (log_left, log_top + log_font.get_linesize() * line)

        # Append surf and rect to list
        text_surfs.append(surf)
        text_rects.append(rect)

    # Blits all text surfaces to the location of their Rect
    for i, surf in enumerate(text_surfs):
        window.blit(surf, text_rects[i])


def drawGamePane(window, game, pane, target=None, message=None):
    """Draws on the game surface then blits game surface to the window
    
    Parameters:
        window: pygame.Surface
        game: source.game.Game
        pane: pygame.Rect
        target: source.entities.Target or None
        message: string or None
    """

    # Pulls the player and current floor from the game object
    player = game.player
    floor = player.location

    # Black out the Game Surface
    game.surface.fill(COLORS['BLACK'])

    # Update the camera's position, must be updated before running floor.draw
    player.camera.update()

    # Run the draw method on floor
    floor.draw(game.surface, player.camera)

    # Create a Rect with the same dimensions as the camera; center it in the main pane
    game_area = player.camera.getRect().copy()
    game_area.center = pane.center

    if target:
        target.drawPath(game.surface)

    # Blit everything on the game surface to the window
    window.blit(game.surface, game_area, player.camera.getRect())

    # If there's a message, draw it
    if message:
        drawMessageBox(window, pane, message)


def drawAllPanes(window, game, panes, target=None, message=None):
    """Redraws all of the panes found in the standard game screen"""
    # Fill in the background of the window with black
    window.fill(COLORS['BLACK'])

    # Draw the side, log and game panes
    drawGamePane(window, game, panes['main'], target, message)
    drawStatPane(window, game.player, panes['side'])
    drawLogPane(window, game.log, panes['log'])
    drawMapPane(window, game.player, game.player.location, panes['map'])
    pygame.draw.rect(window, COLORS['DARK GRAY'], panes['bottom'], 0)


def drawMapPane(window, player, floor, pane):
    """Draws the translucent map into the map pane"""
    scale = 3
    map_surface = pygame.Surface((pane.width, pane.height))
    map_surface.fill(COLORS['BLACK'])

    # Draw Border
    border = (pane.left-1, pane.top-1, pane.width+2, pane.height+2)
    pygame.draw.rect(window, COLORS['YELLOW'], border, 1)

    for x in range(FLOOR_WIDTH):
        for y in range(FLOOR_HEIGHT):
            if x == player.x and y == player.y:
                pygame.draw.rect(map_surface, COLORS['YELLOW'], (x*scale, y*scale, scale, scale), 0)
                continue

            if floor.tile_map[x][y].discovered:
                if x == floor.portals['up'].x and y == floor.portals['up'].y:
                    pygame.draw.rect(map_surface, COLORS['RED'], (x*scale, y*scale, scale, scale), 0)
                    continue

                if x == floor.portals['down'].x and y == floor.portals['down'].y:
                    pygame.draw.rect(map_surface, COLORS['MILD BLUE'], (x*scale, y*scale, scale, scale), 0)
                    continue

                if floor.map.walkable[y][x]:
                    pygame.draw.rect(map_surface, COLORS['GRAY'], (x*scale, y*scale, scale, scale), 0)
                else:
                    pygame.draw.rect(map_surface, COLORS['WHITE'], (x*scale, y*scale, scale, scale), 0)

    map_surface.set_alpha(160)
    window.blit(map_surface, pane)


def drawFPS(window, fps_clock):
    """Draws the FPS in the top right of the screen
    
    Parameters:
        window : pygame.Surface
        fps_clock : pygame.clock.Clock
    """
    window_rect = window.get_rect()

    fps = int(fps_clock.get_fps())

    x_margin = 19
    y_margin = 10

    fps_surf = FONTS['SUBMAIN'].render(str(fps), True, COLORS['GRAY'], COLORS['BLACK'])
    fps_rect = fps_surf.get_rect()
    fps_rect.topleft = (window_rect.left + x_margin, window_rect.top + y_margin)

    pygame.draw.rect(window, COLORS['BLACK'], fps_rect, 0)
    window.blit(fps_surf, fps_rect)


def drawFillBar(window, pane, y_axis, height, fill_percent, fill_color, outline_color=COLORS['WHITE']):
    """Draws a bar filled to a specified percentage
    
    Parameters:
        window : pygame.Surface 
        pane : pygame.Rect 
        y_axis : int : the centery of the bar
        height : int
        fill_percent : float : should be between 0 and 1
        fill_color : tuple(int,int,int)
        outline_color : tuple(int,int,int)
    """
    bar_width = pane.width / 4

    bar = pygame.Rect(0, 0, bar_width, height)
    bar.center = (pane.centerx, y_axis)

    pygame.draw.rect(window, outline_color, bar, 1)

    fill = bar.copy()
    fill.y += 1
    fill.x += 1
    fill.height -= 2
    fill.width = (bar.width - 2) * fill_percent

    pygame.draw.rect(window, fill_color, fill, 0)


def drawMessageBox(window, pane, message):
    """Draws a message box containing a specified message onto the game pane
    
    Parameters:
        window : pygame.Surface
        pane : pygame.Rect
        message : string
    """
    # todo be able to handle longer messages
    y_offset = pane.height / 5

    message_height = pane.height / 5
    message_width = pane.width / 2

    message_box = pygame.Rect(0, 0, message_width, message_height)

    message_box.center = (pane.centerx, pane.centery - y_offset)

    pygame.draw.rect(window, COLORS['BLACK'], message_box,  0)

    text = FONTS['SUBMAIN'].render(message, True, COLORS['WHITE'], COLORS['BLACK'])
    text_rect = text.get_rect()
    text_rect.center = message_box.center

    window.blit(text, text_rect)


def drawInventory(surface, pane, inventory, selected_item):
    """Draws all of the items of the inventory

    Returns: List(Item)
    """
    # Identify colors
    standard_bg_color = COLORS['DARK GRAY']
    selected_bg_color = COLORS['LIGHT GRAY']
    font_color = COLORS['WHITE']
    border_color = COLORS['YELLOW']

    bg_color = standard_bg_color

    # Identify Fonts
    header_font = Fonts.presets['inv_header']
    main_font = Fonts.presets['inv_listing']

    # Inventory Area dimensions
    inventory_width = pane.width / 4
    inventory_height = pane.height * (1/2)
    inventory_area = pygame.Rect(0, 0, inventory_width, inventory_height)
    inventory_area.center = (pane.centerx / 2, pane.centery)
    border_width = 3

    # Draw Inventory Area
    pygame.draw.rect(surface, bg_color, inventory_area, 0)
    pygame.draw.rect(surface, border_color, inventory_area, border_width)
    
    # Distance from the the top of the pane to the top of the word "Inventory"
    title_y_margin = inventory_area.height / 15

    # Draw the word "Inventory" at the top of the Inventory area
    title = header_font.render("Inventory", True, font_color, bg_color)
    title_rect = title.get_rect()
    title_rect.midtop = (inventory_area.centerx, inventory_area.top + title_y_margin)
    surface.blit(title, title_rect)

    # Get the margin on the left side
    x_margin = pane.width/25
    indent_left = inventory_area.left + x_margin

    # The amount that the line top is moved for each item printed
    line_height = main_font.get_linesize()

    # Start the line after the bottom of the Title
    line_top = title_rect.bottom + line_height

    # Start index
    index = 1
    item_order = []

    item_types = inventory.getItemsByType()

    for type in item_types:
        # Draw Header
        header = header_font.render(type.capitalize(), True, font_color, standard_bg_color)
        header_rect = header.get_rect()
        header_rect.topleft = (indent_left, line_top)
        surface.blit(header, header_rect)

        # Recalculate Line Top
        line_top = header_rect.bottom

        # Draw Items
        for item in item_types[type]:

            # Draw Gray Rect around selected item
            if item is selected_item:
                selected_area = pygame.Rect(inventory_area.left+border_width, line_top,
                                            inventory_area.width-border_width*2, line_height)
                pygame.draw.rect(surface, COLORS['LIGHT GRAY'], selected_area, 0)
                bg_color = selected_bg_color
            else:
                bg_color = standard_bg_color

            # Draw Index
            index_surf = main_font.render(str(index)[-1]+".", True, font_color, bg_color)
            index_rect = index_surf.get_rect()
            index_rect.topleft = (indent_left, line_top)
            surface.blit(index_surf, index_rect)

            # Draw Item
            drawItemListing(surface, item, main_font, font_color, bg_color, (index_rect.right, line_top))

            # Move Line
            line_top += line_height

            # Add item to list and increment index
            item_order.append(item)
            index += 1

        # END FOR ITEM LOOP

        # Add an extra line after item category
        line_top += line_height

    # END FOR TYPE LOOP

    return item_order


def drawItemListing(surface, item, font,  font_color, bg_color, top_left):
    """Draws the specified item as a line in the inventory"""
    # Space inbetween left side of image and left side of text

    icon_size = int(CELL_SIZE/2)

    gap = icon_size * (3 / 2)
    item_icon = pygame.transform.scale(item.image, (icon_size, icon_size))

    # Draw the image of the item
    surface.blit(item_icon, top_left)

    item_name = font.render(item.name, True, font_color, bg_color)
    item_name_rect = item_name.get_rect()
    item_name_rect.midleft = (top_left[0]+gap, top_left[1] + icon_size/2)
    surface.blit(item_name, item_name_rect)


def drawItemInfo(surface, pane, item):
    """Draws info about the specified item"""

    # Identify colors
    bg_color = COLORS['DARK GRAY']
    font_color = COLORS['WHITE']
    border_color = COLORS['YELLOW']

    # Identify Fonts
    header_font = Fonts.presets['inv_header']
    main_font = Fonts.presets['inv_listing']
    action_font = Fonts.presets['inv_detail']

    # Identify Linesize
    line_size = main_font.get_linesize()
    half_line_size = line_size / 2

    stats = []

    # Determine height of area description, and stats from item class
    if item.item_class == 'weapon':
        item_type, num = item.id.rsplit("_")
        description = "LVL %d %s" % (item.difficulty, item_type.capitalize())

        # Weapon Stats
        if item.is_ranged:
            area_height = pane.height / 2.25
            stats.append("Ranged Damaged: %.1f" % item.ranged_damage)
            stats.append("Energy Per Shot: %.1f" % item.energy_per_shot)
            stats.append("Fire Rate: %d" % item.fire_rate)
            stats.append("Range: %d" % item.range)

        else:
            area_height = pane.height / 3
            stats.append("Melee Only")

        stats.append("Melee Damage: %.1f" % item.melee_damage)
        stats.append("Melee Speed: %d" % item.melee_speed)

    elif item.item_class == 'armor':
        area_height = pane.height / 4

        description = "LVL %d %s" % (item.difficulty, item.item_class.capitalize())

        stats.append("Defense: %d" % item.defense)

    elif item.item_class == 'battery':
        area_height = pane.height / 4

        description = "LVL %d %s" % (item.difficulty, item.item_class.capitalize())

        stats.append("Power: %d" % item.power)

    else:  # item.item_class == 'reactor'
        area_height = pane.height / 3
        item_type, num = item.id.rsplit("_")

        description = "LVL %d %s %s" % (item.difficulty, item_type.capitalize(), item.item_class.capitalize())

        stats.append("Max Charge: %.1f" % item.max_charge)
        stats.append("Recharge Rate: %.1f" % item.recharge_rate)
        stats.append("Recovery Time: %.1f" % item.recovery_time)
        stats.append("Recoil Charge: %.1f" % item.recoil_charge)

    actions = ["(d)rop"]

    if item.item_class == 'battery':
        actions.append("u(s)e")
    elif item in item.location.equipped.values():
        actions.append("(u)nequip")
    elif item.item_class == 'weapon' and item.is_quick_draw:
        actions.append("(e)quip(fast)")
    else:
        actions.append("(e)quip")

    # Item Area dimensions
    area_width = pane.width / 4
    area = pygame.Rect(0, 0, area_width, area_height)
    area.center = (pane.width * (3/4), pane.centery)
    border_width = 3

    # Draw Item Area
    pygame.draw.rect(surface, bg_color, area, 0)
    pygame.draw.rect(surface, border_color, area, border_width)

    # Distance from the the top of the area to the name of the item
    title_y_margin = area.height / 15

    # Draw the item name at the top of the Inventory area
    title = header_font.render(item.name, True, font_color, bg_color)
    title_rect = title.get_rect()
    title_rect.midtop = (area.centerx, area.top + title_y_margin)
    surface.blit(title, title_rect)

    # Draw Item Image
    image_area = pygame.Rect(0, title_rect.bottom + line_size, CELL_SIZE, CELL_SIZE)
    image_area.centerx = area.centerx
    surface.blit(item.image, image_area)

    # Render Item Level and class
    desc_surf = main_font.render(description, True, font_color, bg_color)
    desc_rect = desc_surf.get_rect()
    desc_rect.midtop = (area.centerx, image_area.bottom + half_line_size)
    surface.blit(desc_surf, desc_rect)

    # Create stat surfs and rects
    stat_surfs = [main_font.render(stat, True, font_color, bg_color) for stat in stats]
    stat_rects = [surf.get_rect() for surf in stat_surfs]

    # Create actions surfs and rects
    action_surfs = [action_font.render(action, True, font_color, bg_color) for action in actions]
    action_rects = [surf.get_rect() for surf in action_surfs]

    # Place Stat Rects
    x_margin = area.width / 10
    line_left = area.left + x_margin
    for i, rect in enumerate(stat_rects):
        rect.topleft = (line_left, desc_rect.bottom + line_size + (i*(line_size*1.5)))

    # Place Action Rects
    action_y = area.bottom - line_size
    horizontal_divider = len(actions) + 1
    for i, rect in enumerate(action_rects, 1):
        rect.center = (area.left + (area.width / horizontal_divider) * i, action_y)

    # Blit Stats to Surface
    for i, surf in enumerate(stat_surfs):
        surface.blit(surf, stat_rects[i])

    # Blit Actions to Surface
    for i, surf in enumerate(action_surfs):
        surface.blit(surf, action_rects[i])
