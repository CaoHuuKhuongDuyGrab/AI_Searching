import os
import pygame
from .button import Button, Text
from ..command import Command_Play, Command_NextMove, Command_PreviousMove, Command_BackChoosingMap, Command_BackChoosingAlgorithm

NAVY_BLUE = (16, 44, 82)
WIDTH_BUTTON = 240
HEIGHT_BUTTON = 50
VSPACE = 80
BUTTON_BACK = './gui/assets/back2.png'


PLAY_EVENT = pygame.USEREVENT + 1
PLAY_INTERVAL = 500

class Sidebar:
    def __init__(self, width, height, map_view, screen_manager, time, fuel):
        self.width = width
        self.height = height
        self.color =  NAVY_BLUE
        self.time = time
        self.fuel = fuel
        self.screen_manager = screen_manager
        self.pathIndex = 0
        self.text_Time = Text(width / 2 - WIDTH_BUTTON / 2 + 120,200, "time: " + str(self.time))
        self.text_Fuel = Text(width / 2 - WIDTH_BUTTON / 2 + 120,250, "tuel: " + str(self.fuel))
        self.text_Step = Text(width / 2 - WIDTH_BUTTON / 2 + 120,300, "step: " + str(self.pathIndex))
        self.text_GameOver = Text(width / 2 - WIDTH_BUTTON / 2 + 120,150, "game end!")
        self.button_Back = Button(width / 2 - WIDTH_BUTTON / 2 + 10, 50 , WIDTH_BUTTON, HEIGHT_BUTTON, 'BACK', command=Command_BackChoosingMap(screen_manager), isCircle= True, image_path= BUTTON_BACK) 
        self.button_Play = Button(width / 2 - WIDTH_BUTTON / 2, 360, WIDTH_BUTTON, HEIGHT_BUTTON, 'PLAY', command=Command_Play(self))
        self.button_Next = Button(width / 2 - WIDTH_BUTTON / 2, 360 + VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'NEXT', command= Command_NextMove(self))
        self.button_Previous = Button(width / 2 - WIDTH_BUTTON / 2, 360 + 2 * VSPACE, WIDTH_BUTTON, HEIGHT_BUTTON, 'PREVIOUS', command=Command_PreviousMove(self))
        self.map_view = map_view

        self.is_playing = False
    def draw(self, screen):
        sidebar_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(screen, self.color, sidebar_rect)
        self.text_Step.draw(screen)
        if self.screen_manager.choosinglevel_screen.currentLevel >= 2:
            self.text_Time.draw(screen)
            if self.screen_manager.choosinglevel_screen.currentLevel>= 3:
                self.text_Fuel.draw(screen)
        self.button_Back.draw(screen)
        self.button_Play.draw(screen)
        self.button_Next.draw(screen)
        self.button_Previous.draw(screen)
        if self.pathIndex == self.map_view.agents[0].numberSteps:
            # if self.map_view.agents
            self.is_playing = False 
            pygame.time.set_timer(PLAY_EVENT, 0)
            self.text_GameOver.draw(screen)
            self.button_Play.update_text("PLAY")
        else:
            None
    def handle_event(self, event):
        for button in [self.button_Back, self.button_Play, self.button_Next, self.button_Previous]:
            if button.is_clicked(event):
                if button == self.button_Back and self.screen_manager.choosinglevel_screen.currentLevel == 1:
                    self.screen_manager.choosingalgorithm_screen.set_unhighlighted_button()
                    button = Button(self.width / 2 - WIDTH_BUTTON / 2 + 10, 50 , WIDTH_BUTTON, HEIGHT_BUTTON, 'BACK', command=Command_BackChoosingAlgorithm(self.screen_manager), isCircle= True, image_path= BUTTON_BACK)
                elif button == self.button_Back and self.screen_manager.choosinglevel_screen.currentLevel != 1:
                    self.button_Back = Button(self.width / 2 - WIDTH_BUTTON / 2 + 10, 50 , WIDTH_BUTTON, HEIGHT_BUTTON, 'BACK', command=Command_BackChoosingMap(self.screen_manager), isCircle= True, image_path= BUTTON_BACK) 
                button.command.execute()
    def next_step(self):
        for agent in self.map_view.agents:
            if agent.path != '-1':
                # print(agent.pathIndex, len(agent.path))
                if agent.pathIndex < len(agent.path):       
                    self.map_view.draw_line(agent.path[agent.pathIndex][0], agent.path[agent.pathIndex][1], agent)
        if self.pathIndex != self.map_view.agents[0].numberSteps:
            self.pathIndex += 1
            self.text_Step.update_text("step: " + str(self.pathIndex))

