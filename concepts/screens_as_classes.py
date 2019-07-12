"""Potential idea to use classes for screens. These are unfinished"""
import pygame


class Screen:
    FPS = 144
    COLORS = {'BLACK': (0, 0, 0),
              'WHITE': (255, 255, 255)}
    FONTS = {'TITLE': pygame.font.Font('freesansbold.ttf', 70),
             'MAIN': pygame.font.Font('freesansbold.ttf', 28)}

    def __init__(self, window, fps_clock):
        self.window = window
        self.window_rect = window.get_rect()
        self.fps_clock = fps_clock


class TitleScreen:
    def __init__(self, window, fps_clock):
        # Extends the Screen init
        super().__init__(window, fps_clock)

        self.text_surfs, self.text_rects = self._getTextRenderObjs()

        # Surface used to give the illusion of transparency to the Continue Prompt
        self.cover = pygame.Surface((self.text_rects['continue'].width, self.text_rects['continue'].height))

        # Sets variables for the alpha of the cover
        self.alpha_max = 200
        self.alpha_min = 25
        self.alpha_change_rate = 5

    def _getTextRenderObjs(self):
        """Returns two dictionaries, one with surfaces for the font renders and another for the rects"""
        text_surfs = dict()

        text_surfs['title'] = self.FONTS['TITLE'].render('Grim Ranger', True, self.COLORS['BLACK'])
        text_surfs['subtitle'] = self.FONTS['MAIN'].render("A Game By Hayden Foley", True, self.COLORS['BLACK'])
        text_surfs['continue'] = self.FONTS['MAIN'].render("Press Enter to Continue", True, self.COLORS['BLACK'])

        rects = {surf: surf.get_rect() for surf in text_surfs}

        return text_surfs, rects

    def setup(self):
        # Sets the location of the text
        self.text_rects['title'].center = (self.window_rect.centerx, self.window_rect.height / 6)
        self.text_rects['subtitle'].midtop = (self.window_rect.centerx, self.title_rect.bottom + self.FONTS['MAIN'].get_linesize())
        self.text_rects['continue'].center = (self.window_rect.centerx, self.window_rect.height * (2 / 3))

        # Sets the
        self.set_alpha(self.alpha_max)
        self.cover.fill(self.COLORS['WHITE'])

    def run(self):
        pass


class GameScreen(Screen):
    def __init__(self, player, window, fps_clock):
        # Extends the Screen init
        super().__init__(window, fps_clock)
        self.player = player

        self.panes = self._createPanes()

    def _createPanes(self):
        """Returns a dictionary of python.rect objects that represent the three main panes of the Game Screen"""
        pass