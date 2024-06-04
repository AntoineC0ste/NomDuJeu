import os
from definitions import *


ennemisDeBase = Ennemis()
personnagePrincipal = Ennemis()
villageois = []
baton = Arme("baton", 2, "Image/baton.png") # TODO changer l'image pour un vrai baton

if not os.path.exists("Sauvegardes/personnage.json"):

    personnagePrincipal.ajouter("Joueur_Principale",50, 5, 2, 3,
                        sprite= "Joueur_Principale",
                        position=[0, 0],
                        inventaire=[],
                        arme=baton)
else:
    personnagePrincipal.charger("personnage")

if not os.path.exists("Sauvegardes/ennemis.json"):

    ennemisDeBase.ajouter("Slime1", 50,2,2,4,
                        sprite= "Slime",
                        position=[300,400],
                        inventaire=[]
                        )
    ennemisDeBase.ajouter("Slime2", 40,2,2,4,
                        sprite= "Slime",
                        position=[350,400],
                        inventaire=[]
                        )

    ennemisDeBase.ajouter("Sanglier1", 25, 7, 3, 3,
                        sprite= "Sanglier",
                        position=[300,500],
                        inventaire=[]
                        )
else:
    ennemisDeBase.charger("ennemis")

#(villageois)

villageois.append(Npc("Paul", 1,
                    sprite="Paul",
                    position=[200,200]))
