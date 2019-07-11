from scripts.constants import *
from scripts.utilities import checkForQuit

import pygame
from pygame.constants import *


def titleScreen(window, fps_clock):
    window.fill(COLORS['WHITE'])
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

    continue_cover = pygame.Surface((continue_prompt_rect.width,continue_prompt_rect.height))
    continue_cover.fill(COLORS['WHITE'])
    continue_cover.set_alpha(200)


    window.blit(title, title_rect)
    window.blit(subtitle, subtitle_rect)
    window.blit(continue_prompt, continue_prompt_rect)



    show_title = True

    continue_alpha = continue_cover.get_alpha()
    decrease_alpha = True

    #continue_prompt = continue_prompt.convert()

    while show_title:
        checkForQuit()
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_RETURN:
                show_title = False

        if decrease_alpha:
            continue_cover.set_alpha(continue_alpha-5)
        else:
            continue_cover.set_alpha(continue_alpha+5)

        continue_alpha = continue_cover.get_alpha()
        if continue_alpha == 25:
            decrease_alpha = False
        elif continue_alpha == 200:
            decrease_alpha = True

        window.blit(continue_prompt, continue_prompt_rect)
        window.blit(continue_cover, continue_prompt_rect)

        pygame.display.flip()
        fps_clock.tick(FPS)
