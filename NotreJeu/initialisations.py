import os
from definitions import *


ennemisDeBase = Ennemis()
personnagePrincipal = Ennemis()
villageois = []
baton = Arme("baton", 2, "Image/baton.png") # TODO changer l'image pour un vrai baton

if not os.path.exists("Sauvegardes/personnage.json"):

    personnagePrincipal.ajouter("Joueur_Principale",50, 5, 2, 3,
                        position=[0, 0],
                        inventaire=[],
                        arme=baton)
else:
    personnagePrincipal.charger("personnage")

if not os.path.exists("Sauvegardes/ennemis.json"):

    ennemisDeBase.ajouter("Slime", 15,2,2,4,
                        position=[300,200],
                        inventaire=[])

    ennemisDeBase.ajouter("Sanglier", 25, 7, 3, 3,
                        position=[300,300],
                        inventaire=[])
else:
    ennemisDeBase.charger("ennemis")

#(villageois)

villageois.append(Npc("Paul", 1, position=[200,200]))
