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
