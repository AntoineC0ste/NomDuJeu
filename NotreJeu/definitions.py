import json
import pygame
from math import *
from random import *

from Animer import AnimationSprite

# Définition des classes de base

class Entity(AnimationSprite) :
    def __init__(self, nom, vitesse, position=[0,0]):  
        super().__init__(nom) 
        
        self.nom = nom
        self.vitesse = vitesse
        self.image = self.get_image(0, 0)
        
        self.rect = self.image.get_rect()
        self.image.set_colorkey([0,0,0])
        self.position = position
        self.root = pygame.Rect(0,0,5,5)
        self.posPrec = self.position.copy()
        self.facing = 0 # 0 = N ; 1 = E ; 2 = S ; 3 = O

    
    
    def mvDroite(self, amount): 
        self.position[0] += amount # 0 pour la position sur x, 1 pour y
        self.facing = 1
    def mvGauche(self, amount):
        self.position[0] -= amount 
        self.facing = 3
    def mvHaut(self, amount):
        self.position[1] -= amount
        self.facing = 0
    def mvBas(self, amount):
        self.position[1] += amount
        self.facing = 2
    def reculer(self):
        self.position = self.posPrec
        self.update()

    def sauvegarderPos(self):
        self.posPrec = self.position.copy()
    def animer(self, x, y):
        self.image = self.get_image(x,y)
        self.image.set_colorkey([0,0,0])
    def update(self):
        self.rect.center = self.position
        self.root.midbottom = self.rect.midbottom


    

class Personnage(Entity):
    def __init__(self, nom, pv, atk, defense, vitesse, position, inventaire, arme=None):
        super().__init__(nom,vitesse, position)
        self.pv = pv
        self.atk = atk
        self.defense = defense
        self.inventaire = inventaire
        self.arme = arme
        self.attackReady = False
        

    def update(self):
        self.rect.center = self.position
        self.root.center = self.rect.center
        if self.arme is not None:
            if self.attackReady:
                # On suit la position du personnage
                if self.facing == 0: 
                    self.arme.rect.midbottom = self.rect.midtop
                    self.arme.animer(0,32)
                elif self.facing == 1: 
                    self.arme.rect.midleft = self.rect.midright
                    self.arme.animer(32,0)
                elif self.facing == 2: 
                    self.arme.rect.midtop = self.rect.midbottom
                    self.arme.animer(0,0)
                elif self.facing == 3: 
                    self.arme.rect.midright = self.rect.midleft
                    self.arme.animer(32,32)
            else:
                self.arme.animer(64,64) # On vient chercher une image transparente
                
    
    def attaquer(self,cible):
        if self.arme is not None:
            degat = self.atk + self.arme.degat
        else:
            degat = self.atk
        cible.subirDegat(degat)

    def subirDegat(self,degat):
        if degat > self.defense:
            self.pv-=(degat-self.defense)

    def activation(self, hero, timer):
        vecteurDistancePerso = [hero.position[0] - self.position[0], hero.position[1] - self.position[1]]
        distancePerso = (vecteurDistancePerso[0]**2 + vecteurDistancePerso[1]**2)**0.5 # On normalise le vecteur
        if  40 < distancePerso < 300:
            if randint(0,1) == 0:
                if self.position[0] < hero.position[0]: # Si a gauche
                    self.mvDroite(self.vitesse)
                    self.animer(32,32)
                else:
                    self.mvGauche(self.vitesse)
                    self.animer(32,0)
            else:
                if self.position[1] > hero.position[1]:
                    self.mvHaut(self.vitesse)
                    self.animer(0,32)
                else:
                    self.mvBas(self.vitesse)
                    self.animer(0,0)
        elif timer%30 == 1 and distancePerso < 40: 
            self.attaquer(hero)
        
    def teleport(self, coords):
        '''Téléporte le personnage vers l'objet spécifié'''
        self.position = [int(coords[0]), int(coords[1])]
        self.update()
        # if distancePerso < 34:
        #     if timer%360 == 1:
        #         pass # TODO gérer les attaques

class Npc(Entity):
    def __init__(self, nom,vitesse, position=[0,0]):
        super().__init__(nom, vitesse, position)  # Appel au constructeur de Entity et donc de pygame.sprite.Sprite
        self.checkpointsDuNpc = []

    def suivreChemin(self, checkpoints):
        if self.checkpointsDuNpc == []:
            for nom, point in checkpoints.items():
                if self.nom in nom:
                    self.checkpointsDuNpc.append(point)
        point = self.checkpointsDuNpc[0]
        vecteurDistancePoint = [point.x - self.position[0], point.y - self.position[1]]
        distancePoint = (vecteurDistancePoint[0]**2 + vecteurDistancePoint[1]**2)**0.5 # On normalise le vecteur
        # print(f"Point [{point.x}, {point.y}] \n PNJ {self.position} \n {vecteurDistancePoint}\n") à ne remettre que pour débugger
        if round(distancePoint) != 0:
            if abs(vecteurDistancePoint[0]) > abs(vecteurDistancePoint[1]):
                if vecteurDistancePoint[0] > 0: # Si a gauche
                    self.mvDroite(self.vitesse)
                    self.animer(32,32)
                else:
                    self.mvGauche(self.vitesse)
                    self.animer(32,0)
            else:
                if vecteurDistancePoint[1] < 0:
                    self.mvHaut(self.vitesse)
                    self.animer(0,32)
                else:
                    self.mvBas(self.vitesse)
                    self.animer(0,0)
        else:
            del(self.checkpointsDuNpc[0])

class Ennemis:
    def __init__(self,ennemisList={}):
        self.ennemisList= ennemisList
    
    def ajouter(self, nom, pv, atk, defense, vitesse, position, inventaire, arme=None):
        self.ennemisList[nom] = Personnage(nom, pv, atk, defense, vitesse, position, inventaire, arme)

    def retirer(self, nom):
        del(self.ennemisList[nom])
    def sauvegarder(self, emplacementSave):
        with open("Sauvegardes/"+emplacementSave+".json", 'w', newline='') as jsonfile : # On ouvre/crée le fichier json, puis on le manipule avec la bibliothèque.
            ennemisDict = {}
            for perso in self.ennemisList.values():  # Pour chaque ennemi
                ennemiActuel = {} # On crée un dictionnaire de ses attributs
                perso = perso.__dict__
                ennemiActuel["nom"] = perso["nom"] # Obligé de faire ça à cause de Pygame qui ajoute des trucs avec la superclasse Sprite
                ennemiActuel["pv"] = perso["pv"]
                ennemiActuel["atk"] = perso["atk"]
                ennemiActuel["defense"] = perso["defense"]
                ennemiActuel["vitesse"] = perso["vitesse"]
                
                

                ennemiActuel["position"] = perso["position"]
                ennemiActuel["inventaire"] = perso["inventaire"]

                if perso['arme'] is not None:
                    ennemiActuel['arme'] = [perso['arme'].__dict__["nom"], perso['arme'].__dict__["degat"], perso['arme'].__dict__["sprite"]]
                else:
                    ennemiActuel["arme"] = perso["arme"]
    
                ennemisDict[perso["nom"]] = ennemiActuel

            json.dump(ennemisDict, jsonfile, indent=4) # Et on l'écrit dans le fichier JSON

    def charger(self, emplacementSave): # C'est la même chose que la sauvegarde mais avec une liste d'attributs
        with open("Sauvegardes/"+emplacementSave+".json", "r") as jsonfile:
            charge = json.load(jsonfile)
            
            self.ennemisList = {}
            ennemiActuel = []
            for perso in charge.values():
                for nom, attribut in perso.items():
                    if nom == "arme" and attribut is not None:
                        ennemiActuel.append(Arme(attribut[0], attribut[1], attribut[2]))
                    else:
                        ennemiActuel.append(attribut)
                
                self.ennemisList[ennemiActuel[0]]= Personnage(ennemiActuel[0],ennemiActuel[1],ennemiActuel[2],ennemiActuel[3],ennemiActuel[4],ennemiActuel[5],ennemiActuel[6],ennemiActuel[7])
                ennemiActuel = []

class Arme(pygame.sprite.Sprite):
    def __init__(self, nom, degat, sprite):
        super().__init__()
        self.nom = nom
        self.degat = degat
        self.sprite = sprite
        self.sprite_sheet = pygame.image.load(sprite)
        self.image = self.get_image(0,0)
        self.rect = self.image.get_rect()
        self.image.set_colorkey([0,0,0])

    def animer(self, x, y):
        self.image = self.get_image(x,y)
        self.image.set_colorkey([0,0,0])
    def get_image(self,x,y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

class Element():
    def __init__(self, largeur=32, hauteur=32, color=(255,255,255)):
        self.image = pygame.Surface((largeur,hauteur))
        self.image.fill(color)
    
    def render(self, surf, x, y):
        surf.blit(self.image, (x, y))

class Text(Element):
    def __init__(self, text, font, color):
        self.image = font.render(text, True, color)

class ProgressBar(Element):
    def __init__(self, largeur, hauteur, couleur):
        super().__init__(hauteur, largeur)
        self.color = couleur

    
    def render(self, surf, x, y, valeur, cible):
        surf.blit(self.image, (x+4, y+4))
        for i in range(round((self.image.get_width()/cible)*valeur)-4): # Largeur de chaque pv pour obtenir la largeur max, multiplié par la valeur actuelle.
            Element(self.image.get_width()/cible, self.image.get_height()-3, self.color).render(surf, i+6, y+6)


