import pygame 
import pytmx
import pyscroll
import os

from initialisations import *
from definitions import *

pygame.init()



class Game:
    def __init__(self):

        self.appuiBouton=0
        self.dashbouton=0
        self.rechargementDash=0
        self.rechargementAtk=0

        self.screen=pygame.display.set_mode((1000, 576))
        pygame.display.set_caption(("notreJeu")) #c'est juste le nom
        self.running= True
        self.isded = False # Si le joueur est mort
        
        #charger la carte
        self.tmx_data = pytmx.util_pygame.load_pygame("Carte/Carte.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        map_layer.zoom = 2.5

        # Créer un dictionnaire de checkpoints pour les pnj
        self.checkpointList = {}
        for obj in self.tmx_data.get_layer_by_name("Chemin_NPC"):
            self.checkpointList[obj.name] = obj

        #generer un joueur
        spawn1 = self.tmx_data.get_object_by_name("Spawn_Player1")
        self.player = personnagePrincipal.ennemisList["Joueur_Principale"]

        if not os.path.exists("Sauvegardes/personnage.json") or self.isded: # Si une sauvegarde n'existe pas ou que le joueur doit respawn
            self.player.position[0] = spawn1.x
            self.player.position[1] = spawn1.y
        
        #dessiner le groupe de calques

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=21)

        self.group.add(self.player)
        self.group.add(self.player.arme)
        for personnage in ennemisDeBase.ennemisList.values():
            self.group.add(personnage)
            if personnage.arme is not None:
                self.group.add(personnage.arme)
    
        for villager in villageois:
            self.group.add(villager)

        # charger les autres éléments du jeu
        police = pygame.font.SysFont("Arial", 36)
        self.barreDeVie = ProgressBar(16, 128, (0,0,255))

    def entreeDuJoueur(self):        
        entree = pygame.key.get_pressed() # Liste des entrées du joueur
        if entree[pygame.K_z]:
            self.player.mvHaut()
        if entree[pygame.K_s]:
            self.player.mvBas()
        if entree[pygame.K_d]:
            self.player.mvDroite()
        if entree[pygame.K_q]:
            self.player.mvGauche()
        if entree[pygame.K_SPACE] and self.rechargementDash>50: 
            if self.dashbouton < 6:
                self.player.dash()
                self.dashbouton += 1
            if self.dashbouton>=4:         
                self.rechargementDash=0  
                
        elif not entree[pygame.K_SPACE]:
            self.dashbouton = 0
            self.rechargementDash+=1
            if self.rechargementDash>1000:
                self.rechargementDash=70
            
        if entree[pygame.K_e] and self.rechargementAtk>25:
            self.rechargementAtk=0
            if self.appuisBouton < 1:
                self.player.attackReady = True
                self.appuisBouton += 1
                print("appuisBouton = ",self.appuisBouton)
        
        if not entree[pygame.K_e]:
            self.appuisBouton = 0
            self.rechargementAtk+=1
            if self.rechargementAtk>200:
                self.rechargementAtk=20
    def boucleEnnemis(self, timer):
        if timer%5 == 1: # Délai d'un douzième de seconde (60/12 = 5)
            for ennemi in ennemisDeBase.ennemisList.values():
                ennemi.sauvegarderPos()
                ennemi.activation(self.player, timer)
                if ennemi.pv <= 0:
                    ennemi.animer(0,0)
                    ennemisDeBase.retirer(str(ennemi.nom))
                    break

    def boucleNpc(self, timer):
        if timer%5 == 1:
            for villager in villageois:
                villager.suivreChemin(self.checkpointList)


    def run(self):
        clock = pygame.time.Clock()
        ennemisTimer = 0 # Chrono qui augmente toutes les 60ièmes de secondes pour gérer les ennemis

        while self.running: #garder la fenetre ouverte
            ennemisTimer += 1
            if ennemisTimer%20 == 1:
                self.player.attackReady = False
            self.boucleEnnemis(ennemisTimer)
            self.boucleNpc(ennemisTimer)
            self.player.sauvegarderPos()
            self.entreeDuJoueur()
            self.group.center(self.player.rect.center)
            self.group.update()
            self.group.draw(self.screen)

            self.barreDeVie.render(self.screen, 0, 0, self.player.pv, 50)

            pygame.display.flip() #pour actualiser tout en boucle a temps réel

            layer_index = 0
            for layer in self.tmx_data.visible_layers: # Trouve la couche de collisions dans le tmx.
                layer_index += 1
                if isinstance(layer, pytmx.TiledObjectGroup):
                    if layer.name == "Objets":
                        for obj in layer:
                            if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(self.player.root):
                                if "TP" in obj.name: 
                                        self.player.teleport(obj.type.split()) # On téléporte vers les coordonnées de la "classe" dans Tiled
                    if layer.name == "Collisions":
                        for obj in layer: # Vérifie pour chaque objet l'état de collision du personnage et des ennemis
                            if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(self.player.root):
                                self.player.reculer()
                            for ennemi in ennemisDeBase.ennemisList.values():
                                if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(ennemi.root):
                                    ennemi.reculer()
                                elif self.player.root.colliderect(ennemi.root):
                                    ennemi.reculer()
                                    self.player.reculer()
                                elif self.player.arme.rect.colliderect(ennemi.rect):
                                    if self.player.attackReady:
                                        self.player.attaquer(ennemi)
                                        self.player.attackReady = False                          

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:   #detecte l'evenement "fenetre fermé"
                    self.running=False    # si oui running= False et la boucle sarrete
            if self.player.pv == 0:
                self.isded = True
                personnagePrincipal.ennemisList["Hero"].pv = 50
                personnagePrincipal.sauvegarder("personnage")
                self.running = False
            else:
                personnagePrincipal.sauvegarder("personnage")
            clock.tick(60)

        
        ennemisDeBase.sauvegarder("ennemis")
        pygame.quit()   #quitter le jeu

        