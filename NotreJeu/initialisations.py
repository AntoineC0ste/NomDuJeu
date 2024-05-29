import os
from definitions import *


ennemisDeBase = Ennemis()
personnagePrincipal = Ennemis()
villageois = []
baton = Arme("baton", 2, "Image/Gobelin.png") # TODO changer l'image pour un vrai baton

if not os.path.exists("Sauvegardes/personnage.json"):

    personnagePrincipal.ajouter("Hero", 50, 5, 2, 3,
                        sprite="Image/Joueur_Principale.png",
                        position=[0, 0],
                        inventaire=[],
                        arme=baton)
else:
    personnagePrincipal.charger("personnage")

if not os.path.exists("Sauvegardes/ennemis.json"):

    ennemisDeBase.ajouter("Slime", 15,2,2,4,
                        sprite="Image/Slime.png",
                        position=[300,200],
                        inventaire=[])

    ennemisDeBase.ajouter("MONSIEUR Porc", 25, 7, 3, 3,
                        sprite="Image/Sanglier.png",
                        position=[300,300],
                        inventaire=[])
else:
    ennemisDeBase.charger("ennemis")

#(villageois)

villageois.append(Npc("Paul", 3, "Image/Paul.png", position=[50,50]))
