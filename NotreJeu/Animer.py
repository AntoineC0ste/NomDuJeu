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
        image = pygame.Surface([32,32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

class AnimationSpriteBoss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.clock = 0
        self.sprite_sheet = pygame.image.load(f'Image/DRAGON3.png')
        self.animation_index = 0
        self.images = {
            "up": self.get_images(483),
            "down": self.get_images(0),
            "right": self.get_images(322),
            "left": self.get_images(161) }
    def change_animation(self, sprite):
        self.image = self.images[sprite][self.animation_index]
        self.image.set_colorkey(0,0)
        self.clock +=  80
        if self.clock >100:
            self.animation_index+=1
            if self.animation_index>= len(self.images[sprite]):
                self.animation_index=0
            self.clock=0
        
    def get_images(self, y):
        images=[]
        for i in range(0,3):
            x = i*191
            image = self.get_image(x, y)
            images.append(image)
        return images

    def get_image(self,x,y):
        image = pygame.Surface([191,161])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 191,161))
        return image
    
class AnimationSpriteAttaque(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.clock = 0
        self.sprite_sheet = pygame.image.load(f'Image/Baton.jpg')
        self.animation_index = 0
        self.images = {
            "up": self.get_images(0),
            "down": self.get_images(0),
            "right": self.get_images(0),
            "left": self.get_images(0) }
    def change_animation(self, sprite):
        self.image = self.images[sprite][self.animation_index]
        self.image.set_colorkey(0,0)
        self.clock += self.vitesse * 6
        if self.clock >100:
            self.animation_index+=1
            if self.animation_index>= len(self.images[sprite]):
                self.animation_index=0
            self.clock=0
        
    def get_images(self, x):
        images=[]
        for i in range(0,4):
            y = i*50
            image = self.get_image(x, y)
            images.append(image)
        return images

    def get_image(self,x,y):
        image = pygame.Surface([40,50])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 40, 50))
        return image