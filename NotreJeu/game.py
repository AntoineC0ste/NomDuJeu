import pygame 
import pytmx
import pyscroll

from definitions import Player
pygame.init()


print("1")
class Game:
    print("2")
    def __init__(self):
        print("3")
        self.screen=pygame.display.set_mode((1000, 576))
        pygame.display.set_caption(("notreJeu")) #c'est juste le nom
        
                    #charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("Carte/Carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        map_layer.zoom = 2
        #generer un joueur
        player_position = tmx_data.get_object_by_name("Spawn_Player1")  
        print(player_position)  
        self.player = Player([player_position.x, player_position.y])


        #dessiner le groupe de calques
        
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=4)
        self.group.add(self.player)

        print("4")

    
    def run(self):
        print("5")
        running= True
        while running: #garder la fenetre ouverte
            self.group.center(self.player.rect.center)
            self.group.update()
            self.group.draw(self.screen)
            pygame.display.flip() #pour actualiser tout en boucle a temps réel
            

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:   #detecte l'evenement "fenetre fermé?"
                    running=False    # si oui running= False et la boucle sarrete
                # if event.type == pygame.KEYDOWN

        pygame.quit()   #quitter le jeu

        