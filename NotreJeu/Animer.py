import pygame

class AnimationSprite(pygame.sprite.Sprite):
    def __init__(self,sprite,nbAnime):
        super().__init__()
        self.nbAnime=nbAnime
        self.clock = 0
        self.sprite=sprite
        self.sprite_sheet = pygame.image.load(f'Image/{sprite}.png')
        self.animation_index = 0
        self.images = {
            "up": self.get_images(96),
            "down": self.get_images(0),
            "right": self.get_images(64),
            "left": self.get_images(32) }
    def change_animation(self, sprite):
        self.image = self.images[sprite][self.animation_index]
        self.image.set_colorkey(0,0)
        self.clock += self.vitesse * 6
        if self.clock >100:
            self.animation_index+=1
            if self.animation_index>= len(self.images[sprite]):
                self.animation_index=0
            self.clock=0
        
    def get_images(self, y):
        images=[]
        for i in range(0,self.nbAnime):
            x = i*32
            image = self.get_image(x, y)
            images.append(image)
        return images

    def get_image(self,x,y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
