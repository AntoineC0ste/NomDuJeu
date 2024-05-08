import json
import pygame
# Définition des classes de base

class Entity(pygame.sprite.Sprite) :
    def __init__(self, nom, pv, atk, defense, vitesse, sprite, position=[0,0]):  
        super().__init__() 
        self.nom = nom
        self.pv = pv
        self.atk = atk
        self.defense = defense
        self.vitesse = vitesse
        self.sprite = sprite # Pour la sauvegarde
        self.sprite_sheet = pygame.image.load(sprite)
        self.image = self.get_image(0,32)
        self.rect = self.image.get_rect()
        self.image.set_colorkey([0,0,0])
        self.position = position
    

    def mvDroite(self, amount): 
        self.position[0] += amount # 0 pour la position sur x, 1 pour y
    def mvGauche(self, amount):
        self.position[0] -= amount 
    def mvHaut(self, amount):
        self.position[1] -= amount
    def mvBas(self, amount):
        self.position[1] += amount

    def animer(self, x, y):
        self.image = self.get_image(x,y)
        self.image.set_colorkey([0,0,0])
    def update(self):
        self.rect.topleft = self.position
    def get_image(self,x,y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

class Arme :
    def __init__(self, nom ,degat):
        self.nom = nom
        self.degat = degat

class Personnage(Entity):
    def __init__(self, nom, pv, atk, defense, vitesse, sprite, position, inventaire, arme=None):
        super().__init__(nom, pv, atk, defense, vitesse, sprite, position)
        self.inventaire = inventaire
        self.arme = arme
    def attaquer(self,cible):
        degat= self.atk + self.arme
        cible.subirDegat(degat)
    def subirDegat(self,degat):
        if degat>self.defense:
            self.pv-=(degat-self.defense)



class Ennemis:
    def __init__(self,ennemisList={}):
        self.ennemisList= ennemisList
    
    def ajouter(self, nom, pv, atk, defense, vitesse, sprite, position, inventaire, arme=None):
        self.ennemisList[nom] = Personnage(nom, pv, atk, defense, vitesse, sprite, position, inventaire, arme)

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
                ennemiActuel["sprite"] = perso["sprite"]
                ennemiActuel["position"] = perso["position"]
                ennemiActuel["inventaire"] = perso["inventaire"]
                ennemiActuel["arme"] = perso["arme"]

                if ennemiActuel['arme'] is not None:
                    ennemiActuel['arme'] = ennemiActuel['arme'].__dict__
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
                        ennemiActuel.append(Arme(attribut['nom'], attribut['degat']))
                    else:
                        ennemiActuel.append(attribut)
                
                self.ennemisList[ennemiActuel[0]]= Personnage(ennemiActuel[0],ennemiActuel[1],ennemiActuel[2],ennemiActuel[3],ennemiActuel[4],ennemiActuel[5],ennemiActuel[6],ennemiActuel[7],ennemiActuel[8])
                ennemiActuel = []
