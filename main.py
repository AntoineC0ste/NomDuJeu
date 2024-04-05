# Définition des classes de base

class Entity :
    def __init__(self, pv, atk, defense, posX=0, posY=0):   
        self.pv = pv
        self.atk = atk
        self.defense = defense
        self.posX = posX
        self.posY = posY
    
    def mvDroite(self, amount): 
        self.posX += amount
    def mvGauche(self, amount):
        self.posX -= amount 
    def mvHaut(self, amount):
        self.posY += amount
    def mvBas(self, amount):
        self.posY -= amount

#class Arme :
    #def __init__(self,degat):

class Personnage(Entity):
    def __init__(self, pv, atk, defense, inventaire, arme, posX=0, posY=0):
        super().__init__(pv, atk, defense, posX, posY)
        self.inventaire = inventaire
        self.arme = arme
    def attaquer(self,cible):
        degat= self.atk + self.arme
        cible.subirDegat(degat)
    def subirDegat(self,degat):
        if degat>self.defense:
            self.pv-=(degat-self.defense)



class Ennemis:
    def __init__(self,ennemisList):
        self.ennemisList= ennemisList
    
    #def ajouterEnnemi(self,attaque,vie,defense,arme,posX=0,posY=0):
        
        
        
        
