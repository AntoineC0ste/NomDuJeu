import os
from definitions import *

bossGame= SauvegardeBoss()
ennemisDeBase = Sauvegarde()
personnagePrincipal = Sauvegarde()
villageois = []
baton = Arme("baton", 2, "Image/baton.png") # TODO changer l'image pour un vrai baton

if not os.path.exists("Sauvegardes/personnage.json"):

    personnagePrincipal.ajouter("Joueur_Principale",50, 5, 2, 3,
                        sprite= "Joueur_Principale",
                        nbAnime=3,
                        position=[0, 0], 
                        inventaire=[],
                        arme=baton)
else:
    personnagePrincipal.charger("personnage")

if not os.path.exists("Sauvegardes/ennemis.json"):

    ennemisDeBase.ajouter("Slime1", 15,5,2,3,
                        sprite= "Squelette",
                        nbAnime=3,
                        position=[7920,5450],
                        inventaire=[]
                        )

                    
    
    ennemisDeBase.ajouter("Slime2", 15,5,2,3,
                        sprite= "Slime",
                        nbAnime=4,
                        position=[7820,5350],
                        inventaire=[]
                        )
    ennemisDeBase.ajouter("Slime3", 20,2,2,4,
                        sprite= "Slime",
                        nbAnime=4,
                        position=[9450,5395],
                        inventaire=[]
                        )
    ennemisDeBase.ajouter("Slime4", 20,7,2,4,
                        sprite= "Slime",
                        nbAnime=4,
                        position=[9000,5425],
                        inventaire=[]
                        )
    ennemisDeBase.ajouter("Slime5", 20,2,2,4,
                        sprite= "Slime",
                        nbAnime=4,
                        position=[9000,5500],
                        inventaire=[]
                        )
                        
else:
    ennemisDeBase.charger("ennemis")

if not os.path.exists("Sauvegardes/boss"):
        bossGame.ajouter("Dragon", 150,20,2,0,
                        position=[9200,5555],
                        )
else:
     bossGame.charger("boss")

#(villageois)

villageois.append(Npc("Paul", 1,
                    sprite="Paul",
                    nbAnime=3,
                    position=[200,200]))
