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
        with open("Sauvegardes/"+emplacementSave+".csv", 'w') as csvfile : # On ouvre/crée le fichier csv, puis on le manipule avec la bibliothèque csv.
            sauvegarde = csv.writer(csvfile)
            listeAttributs = []

            for i in range(len(self.ennemisList)):
                listeAttributs.append([])
                for attribut in self.ennemisList[i].__dict__.values() :
                    if isinstance(attribut, Arme):
                        listeAttributs[i].append(attribut.degat)
                    else:
                        listeAttributs[i].append(attribut)
            sauvegarde.writerow(listeAttributs)  # Si on met cette ligne dans la boucle principale, ça semble bien mais y'a des champs vides et ça plante quand il faut charger (peut être retirer ces champs vides ?)



    def charger(self, emplacementSave):
        with open("Sauvegardes/"+emplacementSave+".csv") as csvfile:
            charge = csv.reader(csvfile)
            self.ennemisList = []
            ennemiActuel = []

            for perso in charge :
                ennemiActuel = perso
                print(ennemiActuel[0]) # Semble afficher une liste ?
                self.ennemisList.append(Personnage(ennemiActuel[0][0],ennemiActuel[0][1],ennemiActuel[0][2] ,ennemiActuel[0][3],ennemiActuel[0][5],ennemiActuel[0][6])) # Théoriquement ça marche, mais il ne semble pas comprendre que c'est une liste et le prend comme une chaîne de caractères
                ennemiActuel = []

                
# Documentation du module csv :
# https://docs.python.org/3/library/csv.html