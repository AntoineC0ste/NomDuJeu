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
    def __init__(self,nom,degat):
        self.nom = nom
        self.degat = degat

class Personnage(Entity):
    def __init__(self, nom, pv, atk, defense, pos, inventaire, arme=None):
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
    
    def ajouter(self, nom, pv, atk, defense, pos, inventaire, arme=None):
        self.ennemisList.append(Personnage(nom, pv, atk, defense, pos, inventaire, arme))

    def retirer(self):
        pass # à coder plus tard, il faut trouver un moyen de trouver un élément de la liste par son nom ou un truc comme ça
    def sauvegarder(self, emplacementSave):
        with open("Sauvegardes/"+emplacementSave+".csv", 'w', newline='') as csvfile : # On ouvre/crée le fichier csv, puis on le manipule avec la bibliothèque csv.
            sauvegarde = csv.writer(csvfile)


            for i in range(len(self.ennemisList)):
                listeAttributs = []
                for attribut in self.ennemisList[i].__dict__.values() :
                    if isinstance(attribut, Arme):
                        listeAttributs.append([attribut.nom, attribut.degat])
                    else:
                        listeAttributs.append(attribut)
                sauvegarde.writerow(listeAttributs)



    def charger(self, emplacementSave):
        with open("Sauvegardes/"+emplacementSave+".csv", "r") as csvfile:
            charge = csv.reader(csvfile)
            self.ennemisList = []

            for perso in charge :
                print(perso[6])
                if perso[6] != '':
                    self.ennemisList.append(Personnage(perso[0],int(perso[1]),int(perso[2]),int(perso[3]),perso[4],perso[5],Arme(perso[6][0],int(perso[6][1])))) 
                else:
                    self.ennemisList.append(Personnage(perso[0],int(perso[1]),int(perso[2]),int(perso[3]),perso[4],perso[5],None)) 


