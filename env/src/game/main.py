'''
'''
import pygame
from PIL import Image
from StringIO import StringIO

import lidapy
from sensor_msgs.msg import CompressedImage

import resources
from constants import *
from game_submenu import game_submenu


class main(object):
    '''
    The primary runner of the game, it regulates the sub-menus, provides
    them with input from the user, keeps track of the high scores, and holds
    the mainloop.
    '''

    def make_screen(self):
        flags = pygame.RESIZABLE
        screen = pygame.display.set_mode(SCREEN_SIZE, flags)
        pygame.display.set_caption(WINDOW_CAPTION)
        return screen

    def __init__(self):
        print "initializing"
        pygame.init()
        self.screen = self.make_screen()
        self.screenrect = self.screen.get_rect()

        resources.images = resources.load_all_images()

        pygame.display.set_icon(resources.images.icon)

        self.submenu = game_submenu(self, self.screenrect)
        self.submenu.draw_all(self.screen)

        pygame.display.flip()

        self.tochangeto = ''

        self.run = True

        lidapy.init(process_name='Environment')

        self.image_topic = lidapy.Topic('images', msg_type=CompressedImage, queue_size=1)
        self.action_topic = lidapy.Topic('actions', queue_size=1)

        self.mainloop()

    def change_submenu(self, sub):
        self.tochangeto = sub

    def destroy(self):
        self.run = False

    def mainloop(self):
        self.timer = pygame.time.Clock()

        while self.run == True:

            if self.tochangeto != '':
                self.submenu.destroy()
                self.submenu = self.tochangeto
                self.submenu.draw_all(self.screen)
                pygame.display.flip()
                self.tochangeto = ''

            # agent actions
            agent_action = self.action_topic.receive(timeout=0.01)
            if agent_action:
                self.process_agent_action(agent_action)
            else:
                # events
                pygame.event.pump()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                    elif event.type == ACTIVEEVENT:
                        if event.gain == 1:
                            # our window has come to the front after being hidden, refresh
                            self.submenu.draw_all(self.screen)
                            pygame.display.flip()
                        elif event.state == 2:
                            # our window is hidden so wait for the next event
                            pygame.event.post(pygame.event.wait())
                    elif event.type == pygame.MOUSEMOTION:
                        self.submenu.mouse_motion(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.submenu.mouse_button_down(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.submenu.mouse_button_up(event)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.run = False
                        elif event.key in LEFT_KEYS:
                            self.submenu.left_pressed()
                        elif event.key in RIGHT_KEYS:
                            self.submenu.right_pressed()
                        elif event.key in UP_KEYS:
                            self.submenu.up_pressed()
                        elif event.key in DOWN_KEYS:
                            self.submenu.down_pressed()
                        else:
                            self.submenu.key_press(event)
                    elif event.type == pygame.KEYUP:
                        if event.key in LEFT_KEYS:
                            self.submenu.left_unpressed()
                        elif event.key in RIGHT_KEYS:
                            self.submenu.right_unpressed()
                        elif event.key in UP_KEYS:
                            self.submenu.up_unpressed()
                        elif event.key in DOWN_KEYS:
                            self.submenu.down_unpressed()
            # update
            self.submenu.update()
            # display
            pygame.display.update(self.submenu.draw(self.screen))

            # image_string = pygame.image.tostring(self.screen, 'RGB')
            screenshot = Image.frombytes('RGB', self.screen.get_size(), pygame.image.tostring(self.screen, 'RGB'))

            buffer = StringIO()
            screenshot.save(buffer, 'JPEG')

            msg = CompressedImage()
            msg.format = 'jpeg'
            msg.data = buffer.getvalue()

            self.image_topic.send(msg)

            # wait and continue
            self.timer.tick(FPS)

        # end of game
        pygame.quit()

    def process_agent_action(self, action):

        if action == 'LEFT':
            self.submenu.left_pressed()
            self.submenu.update()
            self.submenu.left_unpressed()
        elif action == 'RIGHT':
            self.submenu.right_pressed()
            self.submenu.update()
            self.submenu.right_unpressed()
        elif action == 'ROTATE':
            self.submenu.up_pressed()
            self.submenu.update()
            self.submenu.up_unpressed()
        elif action == 'DOWN':
            self.submenu.down_pressed()
            self.submenu.update()
            self.submenu.down_unpressed()
