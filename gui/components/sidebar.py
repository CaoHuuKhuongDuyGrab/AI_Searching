import os
import pygame
from .button import Button


NAVY_BLUE = (16, 44, 82)
WIDTH_BUTTON = 160
HEIGHT_BUTTON = 50
VSPACE = 80
BUTTON_BACK = './gui/assets/back2.png'


PLAY_EVENT = pygame.USEREVENT + 1
PLAY_INTERVAL = 500

class Sidebar:
    def __init__(self, width, height, map_view):
        self.width = width
        self.height = height
        self.color =  NAVY_BLUE 
        self.button_BackMenu = Button(width / 2 - WIDTH_BUTTON / 2, 50 , WIDTH_BUTTON, HEIGHT_BUTTON, 'Back', isCircle= True, image_path= BUTTON_BACK) 
        self.button_Play = Button(width / 2 - WIDTH_BUTTON / 2, 250, WIDTH_BUTTON, HEIGHT_BUTTON, 'Play')
        self.button_Next = Button(width / 2 - WIDTH_BUTTON / 2, 250 + VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'Next')
        self.button_Previous = Button(width / 2 - WIDTH_BUTTON / 2, 250 + 2 * VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'Previous')
        self.map_view = map_view
        self.pathIndex = 0
        self.is_playing = False


    def draw(self, screen):
        sidebar_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(screen, self.color, sidebar_rect)
        self.button_BackMenu.draw(screen)
        self.button_Play.draw(screen)
        self.button_Next.draw(screen)
        self.button_Previous.draw(screen)

    def handle_event(self, event):
        if self.button_Play.is_clicked(event):
            self.is_playing = not self.is_playing
            if self.is_playing:
                print("Play started")
                pygame.time.set_timer(PLAY_EVENT, PLAY_INTERVAL)
                self.button_Play.update_text("Stop")
            else:
                print("Play stopped")
                pygame.time.set_timer(PLAY_EVENT, 0)
                self.button_Play.update_text("Play")
        elif self.button_Next.is_clicked(event):
            print("Next move")
            self.is_playing = False
            pygame.time.set_timer(PLAY_EVENT, 0)
            self.button_Play.update_text("Play")
            self.next_step()
        elif self.button_Previous.is_clicked(event):
            print("Previous move")
            for agent in self.map_view.agents:
                if agent.pathIndex > 0:
                    self.is_playing = False
                    pygame.time.set_timer(PLAY_EVENT, 0)
                    self.button_Play.update_text("Play")
                    self.map_view.remove_line(agent)
        elif self.button_BackMenu.is_clicked(event):
            print("BackMenu move")


    def next_step(self):
            for agent in self.map_view.agents:
                if agent.pathIndex < len(agent.path):       
                    self.map_view.draw_line(agent.path[agent.pathIndex][0], agent.path[agent.pathIndex][1], agent)

