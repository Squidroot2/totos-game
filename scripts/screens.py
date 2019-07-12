"""Contains the screens, each of which contains its own while loop"""

from scripts.constants import *
from scripts.utilities import checkForQuit

import pygame
from pygame.constants import *


def titleScreen(window, fps_clock):
    """Displays the Title Screen. Runs its own while loop until the player hits enter to continue"""

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
