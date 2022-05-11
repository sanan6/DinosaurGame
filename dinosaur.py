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
        self.duck_left_up = None
        self.duck_right_up = None
        self.curr_Y = y
        self.state = 0
        self._load_images()
        self.mask = from_surface(self.left_leg_up)
        self.up = 0
        self.distance = 0
        self.is_duck = False

    def _load_images(self):
        self.left_leg_up = load("./assets/images/left_leg_up.png")
        self.right_leg_up = load("./assets/images/right_leg_up.png")
        self.width = self.left_leg_up.get_width()
        self.height = self.right_leg_up.get_height()
        self.duck_left_up = load("./assets/images/duck_left_up.png")
        self.duck_right_up = load("./assets/images/duck_right_up.png")
        self.duck_width = self.duck_left_up.get_width()
        self.duck_height = self.duck_right_up.get_height()

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
            if self.is_duck:
                if self.Y > BASELINE + self.height - self.duck_height:
                    self.Y = BASELINE + self.height - self.duck_height
            else:
                self.Y = BASELINE

    def jump(self):
        if self.Y == BASELINE:
            self.time_since_jump = 1
            self.vel = 0

    def duck(self):
        if self.Y == BASELINE:
            self.is_duck = True
            self.Y = BASELINE + self.height - self.duck_height

    def un_duck(self):
        if self.Y == BASELINE + self.height - self.duck_height:
            self.is_duck = False
            self.Y = BASELINE

    def draw(self, target):
        """
        Draw the player on the target object.

        :param target: The target surface on which the player should be drawn, the background or the screen.
        :return: None
            """
        self.state += 1
        if self.state > STEP_SPEED * 2 - 1:
            self.state = 0
        if self.is_duck:
            self.mask = from_surface(self.duck_left_up)
            if self.state < STEP_SPEED:
                target.blit(self.duck_left_up, (self.X, self.Y))
            else:
                target.blit(self.duck_right_up, (self.X, self.Y))
        else:
            self.mask = from_surface(self.left_leg_up)
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
        if self.is_duck:
            return Rect(self.X, self.Y, self.duck_width, self.duck_height)
        else:
            return Rect(self.X, self.Y, self.width, self.height)
