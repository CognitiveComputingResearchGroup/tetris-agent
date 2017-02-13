import game_submenu
import resources
from TextWidget import TextWidget
from constants import *
from image_holder import image_holder


class main_submenu():
    '''
    the main menu, has a title image, and buttons for starting a game, looking
    at the high scores, and quitting.
    '''

    def __init__(self, main, screenrect):
        self.main = main
        self.screenrect = screenrect

        self.widgets = []

        self.background = resources.images.main_menu_background

        headerimg = resources.images.main_menu_header
        headerrect = headerimg.get_rect()
        headerrect.midtop = (screenrect.midtop[0], screenrect.midtop[1] + 20)
        self.header = image_holder(headerimg, headerrect)

        self.playbutton = TextWidget(text='Play', color=BUTTON_COLOR, font_filename=resources.fontfilename)
        self.playbutton.on_mouse_click = self.play_click
        self.playbutton.rect.midtop = self.header.rect.midbottom
        self.playbutton.rect.top += 30
        self.widgets.append(self.playbutton)

        self.highbutton = TextWidget(text='High Scores', color=BUTTON_COLOR, font_filename=resources.fontfilename)
        self.highbutton.on_mouse_click = self.high_click
        self.highbutton.rect.midtop = self.playbutton.rect.midbottom
        self.highbutton.rect.top += 30
        self.widgets.append(self.highbutton)

        self.quitbutton = TextWidget(text='Quit', color=BUTTON_COLOR, font_filename=resources.fontfilename)
        self.quitbutton.on_mouse_click = self.quit_click
        self.quitbutton.rect.midtop = self.highbutton.rect.midbottom
        self.quitbutton.rect.top += 30
        self.widgets.append(self.quitbutton)

        r = self.playbutton.rect.unionall([self.highbutton.rect, self.quitbutton.rect])
        r.inflate_ip(200, 30)

    def draw(self, screen):
        rects = []
        rects += self.update_background(screen)
        screen.blit(self.background, (0, 0))
        self.header.draw(screen)
        for widget in self.widgets:
            widget.dirty = True
            rects.append(widget.draw(screen, self.background))
        return rects

    def draw_all(self, screen):
        self.update_background(screen)
        screen.blit(self.background, (0, 0))
        self.header.draw(screen)
        for widget in self.widgets:
            widget.dirty = True
            widget.draw(screen, self.background)

    def destroy(self):
        del self.main, self.widgets

    def update(self):
        pass

    def key_press(self, event):
        pass

    def mouse_button_down(self, event):
        for text in self.widgets:
            text.on_mouse_button_down(event)

    def mouse_button_up(self, event):
        for text in self.widgets:
            text.on_mouse_button_up(event)

    def mouse_motion(self, event):
        for text in self.widgets:
            text.highlight = text.rect.collidepoint(event.pos)

    def up_pressed(self):
        pass

    def up_unpressed(self):
        pass

    def down_pressed(self):
        pass

    def down_unpressed(self):
        pass

    def left_pressed(self):
        pass

    def left_unpressed(self):
        pass

    def right_pressed(self):
        pass

    def right_unpressed(self):
        pass

    def play_click(self, event):
        self.main.change_submenu(game_submenu.game_submenu(self.main, self.screenrect))
        resources.sounds.change_submenu.play()
