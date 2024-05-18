import pygame 
import pytmx
import pyscroll
import os

from initialisations import *
from definitions import *
pygame.init()



class Game:
    def __init__(self):
        self.screen=pygame.display.set_mode((1000, 576))
        pygame.display.set_caption(("notreJeu")) #c'est juste le nom
        self.running= True
        
        #charger la carte
        self.tmx_data = pytmx.util_pygame.load_pygame("Carte/Carte.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        map_layer.zoom = 2.5
        #generer un joueur
        spawn1 = self.tmx_data.get_object_by_name("Spawn_Player1")
        self.player = personnagePrincipal.ennemisList["Hero"]

        if not os.path.exists("Sauvegardes/personnage.json"): # Si une sauvegarde n'existe pas
            self.player.position[0] = spawn1.x
            self.player.position[1] = spawn1.y
        

        #dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=4)
        self.group.add(self.player)
        for personnage in ennemisDeBase.ennemisList.values():
            self.group.add(personnage)

    def entreeDuJoueur(self):
        entree = pygame.key.get_pressed() # Liste des entrées du joueur
        if entree[pygame.K_DOWN]:
            self.player.mvBas(self.player.vitesse)
            self.player.animer(0,0)
        elif entree[pygame.K_UP]:
            self.player.mvHaut(self.player.vitesse)
            self.player.animer(0,32)
            
        elif entree[pygame.K_RIGHT]:
            self.player.mvDroite(self.player.vitesse)
            self.player.animer(32,32)
        elif entree[pygame.K_LEFT]:
            self.player.mvGauche(self.player.vitesse)
            self.player.animer(32,0)
        # TODO: intégrer l'animation dans la méthode de mouvement pour les ennemis.

    def boucleEnnemis(self, timer):
        if timer%5 == 1: # Délai d'un douzième de seconde (60/12 = 5)
            for ennemi in ennemisDeBase.ennemisList.values():
                ennemi.sauvegarderPos()
                ennemi.activation(self.player.position)

        


    def run(self):
        clock = pygame.time.Clock()
        ennemisTimer = 0 # Chrono qui augmente toutes les 60ièmes de secondes pour gérer les ennemis

        while self.running: #garder la fenetre ouverte
            ennemisTimer += 1
            self.boucleEnnemis(ennemisTimer)
            self.player.sauvegarderPos()
            self.entreeDuJoueur()
            self.group.center(self.player.rect.center)
            self.group.update()
            self.group.draw(self.screen)

            pygame.display.flip() #pour actualiser tout en boucle a temps réel

            layer_index = 0
            for layer in self.tmx_data.visible_layers: # Trouve la couche de collisions dans le tmx.
                layer_index += 1
                if isinstance(layer, pytmx.TiledObjectGroup):
                    if layer.name == "Collisions":
                        for obj in layer: # Vérifie pour chaque objet l'état de collision du personnage et des ennemis
                            if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(self.player.root):
                                self.player.reculer()
                            for ennemi in ennemisDeBase.ennemisList.values():
                                if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(ennemi.root):
                                    ennemi.reculer()
                            # TODO: Créer des collisions entre joueur et ennemis (en utilisant le Rect du sprite)

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:   #detecte l'evenement "fenetre fermé"
                    self.running=False    # si oui running= False et la boucle sarrete
            clock.tick(60)

        personnagePrincipal.sauvegarder("personnage")
        ennemisDeBase.sauvegarder("ennemis")
        pygame.quit()   #quitter le jeu

        