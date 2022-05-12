import pygame
from settings import *
from pygame.image import load
from pygame.rect import Rect


class Cacti:
    """
    Class for the obstacles on the ground which are cacti.
    """
    def __init__(self, x):
        """
        Initialize cacti.

        :param x: x position to create the cactus at
        """
        super().__init__()
        self.X = x
        self.is_cactus = 1
        self.cactus_body = load('assets/images/cactus.png')

        self.image = pygame.Surface((CACTUS_WIDTH, CACTUS_HEIGHT), flags=pygame.SRCALPHA)
        self.image.convert()
        self.image.fill((0, 0, 0, 0))

        self.BOTTOM_POS = BASELINE
        self.image.blit(self.cactus_body, (0, self.BOTTOM_POS))

        self.mask = pygame.mask.from_surface(self.image)
        
        
    def update(self):
        """
        Update position by a constant value which is the speed of the environment.

        :return: None
        """
        self.X -= ENV_SPEED

    def draw(self, target, is_alive = False):
        """
        Draw the cactus on the target object.

        :param target: The target surface on which the cactus should be drawn, the background or the screen.
        :param is_alive: Does nothing here, but necessary for the pterodactyls
        :return: None
        """
        target.blit(self.image, (self.X, 0))

    def collides(self, player):
        """
        Check if player collides with the cactus.

        :param player: player object to check collisions with
        :return: whether a collision is detected
        """
        if pygame.sprite.collide_mask(self, player):
            return True
        return False

    @property
    def rect(self):
        """
        The rectangle encapsulating the cactus.

        :return: rectangle object encapsulating the cactus
        """
        return Rect(self.X, 0, CACTUS_WIDTH, CACTUS_HEIGHT)


class Fly:
    """
    Class for the obstacles in the air which are the flying pterodactyls.
    """

    def __init__(self, x, y = FLY_HEIGHT):
        """
        Initialize pterodactyls.

        :param x: x position to create the pterodactyl at
        :param y: y position to create the pterodactyl at
        """
        super().__init__()
        self.X = x
        self.Y = y
        self.is_cactus = 0
        self.fly_up_body = load('assets/images/fly_up2.png')
        self.fly_down_body = load('assets/images/fly_down2.png')
        self.width = self.fly_up_body.get_width()
        self.height = self.fly_up_body.get_width()
        self.state = 0

        self.image = pygame.Surface((CACTUS_WIDTH, CACTUS_HEIGHT), flags=pygame.SRCALPHA)
        self.image.convert()
        self.image.fill((0, 0, 0, 0))
        self.BOTTOM_POS = 0

        self.BOTTOM_POS = self.Y
        self.image.blit(self.fly_up_body, (0, self.BOTTOM_POS))

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """
        Update position by a constant value which is the speed of the environment.

        :return: None
        """
        self.X -= ENV_SPEED

    def draw(self, target, is_alive = True):
        """
        Draw the pterodactyl on the target object.

        :param target: The target surface on which the pterodactyl should be drawn, the background or the screen.
        :param is_alive: If the game ends the sprite of the pterodactyls stop
        :return: None
        """
        if is_alive:
            self.state += 1
        if self.state > STEP_SPEED_FLY * 2 - 1:
            self.state = 0
        if self.state < STEP_SPEED_FLY:
            target.blit(self.fly_up_body, (self.X, self.BOTTOM_POS))
        else:
            target.blit(self.fly_down_body, (self.X, self.BOTTOM_POS))

    def collides(self, player):
        """
        Check if player collides with the pterodactyl.

        :param player: player object to check collisions with
        :return: whether a collision is detected
        """
        if pygame.sprite.collide_mask(self, player):
            return True
        return False

    @property
    def rect(self):
        """
        The rectangle encapsulating the pterodactyl.

        :return: rectangle object encapsulating the pterodactyl
        """
        return Rect(self.X, 0, self.width, self.height)