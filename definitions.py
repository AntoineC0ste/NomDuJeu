import csv
# Définition des classes de base

class Entity :
    def __init__(self, nom, pv, atk, defense, pos=[0,0]):   
        self.nom = nom
        self.pv = pv
        self.atk = atk
        self.defense = defense
        self.pos = pos
    
    def mvDroite(self, amount): 
        self.pos[0] += amount # 0 pour la position sur x, 1 pour y
    def mvGauche(self, amount):
        self.pos[0] -= amount 
    def mvHaut(self, amount):
        self.pos[1] += amount
    def mvBas(self, amount):
        self.pos[1] -= amount

class Arme :
    def __init__(self,degat):
        self.degat = degat

class Personnage(Entity):
    def __init__(self, nom, pv, atk, defense, inventaire, arme, pos=[0,0]):
        super().__init__(nom, pv, atk, defense, pos)
        self.inventaire = inventaire
        self.arme = arme
    def attaquer(self,cible):
        degat= self.atk + self.arme
        cible.subirDegat(degat)
    def subirDegat(self,degat):
        if degat>self.defense:
            self.pv-=(degat-self.defense)



class Ennemis:
    def __init__(self,ennemisList=[]):
        self.ennemisList= ennemisList
    
    def ajouter(self, nom, pv, atk, defense, inventaire, arme=None, pos=[0,0]):
        self.ennemisList.append(Personnage(nom, pv, atk, defense, inventaire, arme, pos))

    def retirer(self):
        pass # à coder plus tard, il faut trouver un moyen de trouver un élément de la liste par son nom ou un truc comme ça
    def save(self, emplacementSave):
        pass # Je le ferais ce soir je pense

        
        
