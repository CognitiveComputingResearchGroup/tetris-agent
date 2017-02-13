import pygame

import resources
from constants import *
from next_previewer import next_previewer
from playing_field import playing_field
from score_display import score_display


class game_submenu(object):
    '''
    the main game screen, it has on it the playing field, the next piece
    previewer, the score displayer, a quit button, and a pause button.
    When the pause button is clicked it toggles between the playing field
    being updated and not. When not the pause button also flashes.
    '''

    def __init__(self, main, screenrect):
        self.main = main
        self.screenrect = screenrect

        self.paused = False
        self.colorchange = PAUSE_BUTTON_COLOR_CHANGE_RATE

        self.background = resources.images.play_background

        self.field = playing_field(FIELD_WIDTH, FIELD_HEIGHT, resources.images.bg_tile, PIECE_MAPS, self.end_game)

        fieldrect = pygame.Rect(0, 0, (FIELD_WIDTH + 2) * TILE_SIZE[0], (FIELD_HEIGHT + 2) * TILE_SIZE[1])
        fieldrect.center = (screenrect.center[0] / 2, screenrect.center[1])
        self.fieldpos = fieldrect.topleft

        self.next_previewer = next_previewer(self.field)
        previewer_rect = pygame.Rect(0, 0, 140, 225)
        previewer_rect.midtop = (round(screenrect.width * 0.75, 0), 30)
        self.previewer_pos = previewer_rect.topleft

        self.score_display = score_display(self.field)
        score_display_rect = pygame.Rect(0, 0, 150, 150)
        score_display_rect.midtop = previewer_rect.midbottom
        score_display_rect.top += 30
        self.score_display_pos = score_display_rect.topleft

        self.textwidgets = []

    def draw(self, screen):
        rects = []
        rects += self.field.render(screen, self.fieldpos)
        rects += self.score_display.render(screen, self.score_display_pos)
        rects += self.next_previewer.render(screen, self.previewer_pos)
        for widget in self.textwidgets:
            if widget.dirty:
                r = widget.draw(screen, self.background)
                if r != None:
                    rects.append(r)
        return rects

    def draw_all(self, screen):
        screen.blit(self.background, (0, 0))
        self.field.render_all(screen, self.fieldpos)
        self.score_display.render_all(screen, self.score_display_pos)
        self.next_previewer.render_all(screen, self.previewer_pos)
        for widget in self.textwidgets:
            widget.dirty = True
            widget.draw(screen, self.background)

    def update(self):
        self.field.update()
        self.score_display.update()
        self.next_previewer.update()

    def destroy(self):
        self.field.destroy()
        self.score_display.destroy()
        self.next_previewer.destroy()
        del self.field, self.score_display, self.next_previewer

    def key_press(self, event):
        pass

    def mouse_button_down(self, event):
        for text in self.textwidgets:
            text.on_mouse_button_down(event)

    def mouse_button_up(self, event):
        for text in self.textwidgets:
            text.on_mouse_button_up(event)

    def mouse_motion(self, event):
        for text in self.textwidgets:
            text.highlight = text.rect.collidepoint(event.pos)

    def up_pressed(self):
        if self.field.piece != None:
            self.field.piece.pressed['up'] = True

    def up_unpressed(self):
        if self.field.piece != None:
            self.field.piece.pressed['up'] = False

    def down_pressed(self):
        if self.field.piece != None:
            self.field.piece.pressed['down'] = True

    def down_unpressed(self):
        if self.field.piece != None:
            self.field.piece.pressed['down'] = False

    def left_pressed(self):
        if self.field.piece != None:
            self.field.piece.pressed['left'] = True

    def left_unpressed(self):
        if self.field.piece != None:
            self.field.piece.pressed['left'] = False

    def right_pressed(self):
        if self.field.piece != None:
            self.field.piece.pressed['right'] = True

    def right_unpressed(self):
        if self.field.piece != None:
            self.field.piece.pressed['right'] = False

    def end_game(self, lost):
        self.main.change_submenu(game_submenu(self.main, self.screenrect))
