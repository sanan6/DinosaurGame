import pygame
import pygame_menu
from game_engine import start
from multiplayer import multiplayer_run
from ai import AIstart
from settings import *

def menu():
    """
    This creates the menu which starts when we open the program.

    :return: None
    """
    pygame.init()
    surface = pygame.display.set_mode(SIZE) #global setting-ek egy külön fájlból

    icon_image = pygame.image.load('assets/images/icon.png')
    pygame.display.set_caption('Dino Game')
    pygame.display.set_icon(icon_image)

    mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
    mytheme.background_color = pygame_menu.baseimage.BaseImage(image_path='assets/images/menu.png')
    mytheme.widget_font = pygame_menu.font.FONT_8BIT
    mytheme.widget_font_color = pygame.Color(0,0,0)
    mytheme.widget_selection_effect = pygame_menu.widgets.HighlightSelection(border_width=1, margin_x=16, margin_y=8)
    mytheme.widget_selection_color = pygame.Color(100,100,100)
    mytheme.widget_box_background_color = pygame.Color(0,0,0)
    mytheme.widget_cursor = pygame.cursors.arrow #lehet csinálni menő pterodaktilusz alakút a dokumentációból
    mytheme.title_font = pygame_menu.font.FONT_8BIT

    menu = pygame_menu.Menu('Dinosaur Game', WIN_WIDTH/3, WIN_HEIGHT, theme=mytheme)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            exit()
    if menu.is_enabled():
        menu.update(events)
        menu.draw(surface)

    blanc = menu.add.button('')
    single_player = menu.add.button('single player', start)
    multiplayer = menu.add.button('multiplayer', multiplayer_run)
    ai_mode = menu.add.button('ai Mode', AIstart)
    quit = menu.add.button('quit', pygame_menu.events.EXIT)

    single_player.set_font(font=pygame_menu.font.FONT_8BIT, font_size=32, color=(0, 0, 0),
                           selected_color=(150, 150, 150), readonly_color=(0, 255, 0),
                           readonly_selected_color=(0, 255, 255), background_color=None, antialias=True)
    multiplayer.set_font(font=pygame_menu.font.FONT_8BIT, font_size=32, color=(0, 0, 0),
                         selected_color=(150, 150, 150), readonly_color=(0, 255, 0),
                         readonly_selected_color=(0, 255, 255), background_color=None, antialias=True)
    ai_mode.set_font(font=pygame_menu.font.FONT_8BIT, font_size=32, color=(0, 0, 0),
                      selected_color=(150, 150, 150), readonly_color=(0, 255, 0),
                      readonly_selected_color=(0, 255, 255), background_color=None, antialias=True)
    quit.set_font(font=pygame_menu.font.FONT_8BIT, font_size=32, color=(0, 0, 0),
                  selected_color=(150, 150, 150), readonly_color=(0, 255, 0),
                  readonly_selected_color=(0, 255, 255), background_color=None, antialias=True)
    menu.mainloop(surface)

    pygame.display.update()

if __name__ == '__main__':
    menu()

