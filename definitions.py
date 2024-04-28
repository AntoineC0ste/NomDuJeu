import json
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
        with open("Sauvegardes/"+emplacementSave+".json", 'w', newline='') as jsonfile : # On ouvre/crée le fichier json, puis on le manipule avec la bibliothèque.
            ennemisDict = {}
            for i in range(len(self.ennemisList)):  # Pour chaque ennemi
                ennemiActuel = self.ennemisList[i].__dict__ # On crée un dictionnaire de ses attributs
                if ennemiActuel['arme'] is not None:
                    ennemiActuel['arme'] = ennemiActuel['arme'].__dict__
                ennemisDict[self.ennemisList[i].nom] = ennemiActuel
            json.dump(ennemisDict, jsonfile, indent=4) # Et on l'écrit dans le fichier JSON

    def charger(self, emplacementSave): # C'est la même chose que la sauvegarde mais avec une liste d'attributs
        with open("Sauvegardes/"+emplacementSave+".json", "r") as jsonfile:
            charge = json.load(jsonfile)
            
            self.ennemisList = []
            ennemiActuel = []
            print(charge)
            for perso in charge.values():
                for nom, attribut in perso.items():
                    if nom == "arme" and attribut is not None:
                        ennemiActuel.append(Arme(attribut['nom'], attribut['degat']))
                    else:
                        ennemiActuel.append(attribut)
                
                self.ennemisList.append(Personnage(ennemiActuel[0],ennemiActuel[1],ennemiActuel[2],ennemiActuel[3],ennemiActuel[4],ennemiActuel[5],ennemiActuel[6]))
                ennemiActuel = []


