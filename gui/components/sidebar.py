import os
import pygame
from .button import Button, Text
from ..command import Command_Play, Command_NextMove, Command_PreviousMove, Command_BackMenu

NAVY_BLUE = (16, 44, 82)
WIDTH_BUTTON = 240
HEIGHT_BUTTON = 50
VSPACE = 80
BUTTON_BACK = './gui/assets/back2.png'


PLAY_EVENT = pygame.USEREVENT + 1
PLAY_INTERVAL = 500

class Sidebar:
    def __init__(self, width, height, map_view, screen_manager):
        self.width = width
        self.height = height
        self.color =  NAVY_BLUE
        self.text_GameOver = Text(width / 2 - WIDTH_BUTTON / 2 + 120,150, "game over!")
        self.button_BackMenu = Button(width / 2 - WIDTH_BUTTON / 2 + 10, 50 , WIDTH_BUTTON, HEIGHT_BUTTON, 'BACK', command=Command_BackMenu(screen_manager), isCircle= True, image_path= BUTTON_BACK) 
        self.button_Play = Button(width / 2 - WIDTH_BUTTON / 2, 250, WIDTH_BUTTON, HEIGHT_BUTTON, 'PLAY', command=Command_Play(self))
        self.button_Next = Button(width / 2 - WIDTH_BUTTON / 2, 250 + VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'NEXT', command= Command_NextMove(self))
        self.button_Previous = Button(width / 2 - WIDTH_BUTTON / 2, 250 + 2 * VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'PREVIOUS', command=Command_PreviousMove(self))
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
        if self.pathIndex == self.map_view.agents[0].numberSteps:
            self.is_playing = False 
            pygame.time.set_timer(PLAY_EVENT, 0)
            self.text_GameOver.draw(screen)
            self.button_Play.update_text("PLAY")

        else:
            None
    def handle_event(self, event):
        for button in [self.button_BackMenu, self.button_Play, self.button_Next, self.button_Previous]:
            if button.is_clicked(event):
                button.command.execute()
    def next_step(self):
            for agent in self.map_view.agents:
                if agent.pathIndex < len(agent.path):       
                    self.map_view.draw_line(agent.path[agent.pathIndex][0], agent.path[agent.pathIndex][1], agent)
            if self.pathIndex != self.map_view.agents[0].numberSteps:
                self.pathIndex += 1


