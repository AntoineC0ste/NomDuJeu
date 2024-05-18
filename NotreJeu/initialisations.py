# import pytmx
import os
from definitions import *


ennemisDeBase = Ennemis()
personnagePrincipal = Ennemis()

if not os.path.exists("Sauvegardes/personnage.json"):

    personnagePrincipal.ajouter("Hero", 50, 5, 2, 3,
                        sprite="Image/Joueur_Principale.png",
                        position=[0, 0],
                        inventaire=[])
else:
    personnagePrincipal.charger("personnage")

if not os.path.exists("Sauvegardes/ennemis.json"):

    ennemisDeBase.ajouter("Slime", 5,2,2,4,
                        sprite="Image/Slime.png",
                        position=[300,200],
                        inventaire=[])

    ennemisDeBase.ajouter("MONSIEUR Porc", 15, 7, 3, 3,
                        sprite="Image/Sanglier.png",
                        position=[300,300],
                        inventaire=[])
else:
    ennemisDeBase.charger("ennemis")