import unittest
from dinosaur import Dinosaur
from settings import *
import pygame


class TestDino(unittest.TestCase):
    pygame.init()

    def test_player_creation(self):
        dino = Dinosaur(x=50, y=100)
        self.assertEqual(dino.X, 50)

    def test_player_update(self):
        dino = Dinosaur(x=50, y=100)
        dino.update()
        self.assertGreater(dino.Y, 100)

    def test_jump(self):
        dino = Dinosaur(x=50, y=BASELINE)
        dino.jump()
        self.assertEqual(dino.time_since_jump, 1)

    def test_cant_jump(self):
        dino = Dinosaur(x=50, y=100)
        dino.jump()
        self.assertNotEqual(dino.time_since_jump, 1)
    
    def test_duck(self):
        dino = Dinosaur(x=50, y=BASELINE)
        dino.duck()
        self.assertEqual(dino.is_duck, True)

    def test_cant_duck(self):
        dino = Dinosaur(x=50, y=100)
        dino.duck()
        self.assertEqual(dino.is_duck, False)

    def test_rect(self):
        dino = Dinosaur(x=50, y=100)
        self.assertIsInstance(dino.rect, pygame.rect.Rect)