import pygame
from settings import *
from pygame.image import load
from pygame.rect import Rect

class Cacti:
    """
    Class for the obstacles on the ground
    """
    def __init__(self, x):
        """
        Initialize cactii.

        :param x: x position to create the cactus at
        """
        super().__init__()
        self.X = x
        self.cactus_body = load('assets/images/left_leg_up.png')

        self.image = pygame.Surface((CACTUS_WIDTH, CACTUS_HEIGHT), flags=pygame.SRCALPHA)
        self.image.convert()
        self.image.fill((0, 0, 0, 0))
        self.BOTTOM_POS = 0

        self.BOTTOM_POS = BASELINE
        self.image.blit(self.cactus_body, (0, self.BOTTOM_POS))

        self.mask = pygame.mask.from_surface(self.image)
        
        
    def update(self):
        """
        Update position.

        :return: None
        """
        self.X -= ENV_SPEED

    def draw(self, target):
        """
        Draw the cactus on the target object.

        :param target: The target surface on which the cactus should be drawn, the background or the screen.
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