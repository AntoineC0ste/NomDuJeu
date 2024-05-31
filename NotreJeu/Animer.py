import pygame
from pygame.sprite import _Group
class AnimationSprite(pygame.sprite.Sprite):
    def __init__(self,nom):
        super().__init__()
        self.sprit_sheet = pygame.image.load(f'Image/{nom}.pnj')
