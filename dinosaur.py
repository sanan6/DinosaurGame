from pygame.mask import from_surface
from pygame.image import load
from pygame.rect import Rect
from settings import *

class Dinosaur:
    def __init__(self, x=WIN_WIDTH / 16, y=BASELINE):
        self.X = x
        self.Y = y
        self.vel = 0
        self.acc = 0.2
        self.force = 20
        self.time_since_jump = 0
        self.left_leg_up = None
        self.right_leg_up = None
        self.state = 0
        self._load_images()
        self.mask = from_surface(self.left_leg_up)
        self.up = 0
        self.distance = 0

    def _load_images(self):
        self.left_leg_up = load("./assets/images/left_leg_up.png")
        self.right_leg_up = load("./assets/images/right_leg_up.png")
        self.width = self.left_leg_up.get_width()
        self.height = self.right_leg_up.get_height()

    def update(self):
        self.up = 0

        if self.time_since_jump:
            self.up = self.force
            self.time_since_jump += 1
            if self.time_since_jump >= self.force:
                self.time_since_jump = 0

        self.vel += 1.7 * self.acc
        self.Y += self.vel - self.up

        if self.Y > BASELINE:
            self.Y = BASELINE

    def jump(self):
        if self.Y == BASELINE:
            self.time_since_jump = 1
            self.vel = 0

    def duck(self):
        return

    def draw(self, target):
        """
        Draw the player on the target object.

        :param target: The target surface on which the player should be drawn, the background or the screen.
        :return: None
            """
        self.state += 1
        if self.state > STEP_SPEED * 2 - 1:
            self.state = 0

        if self.state < STEP_SPEED:
            target.blit(self.left_leg_up, (self.X, self.Y))
        else:
            target.blit(self.right_leg_up, (self.X, self.Y))

    @property
    def rect(self):
        """
        The rectangle encapsulating the player sprite.

        :return: rectangle encapsulating the player
        """
        return Rect(self.X, self.Y, self.width, self.height)