#Piocher une tuile
import pygame
from random import randint
pygame.init()

#On définit le nombre de personnage
nb_personnage = 9

#Tuile (chargement des images + réductions de la taille de chaque tuile)
#associé nombre 1
canonniere = pygame.image.load("Images/Canonnière.jpeg")
canonniere = pygame.transform.scale(canonniere,(85, 85))

#associé nombre 2
cartographe = pygame.image.load("Images/Cartographe.jpeg")
cartographe = pygame.transform.scale(cartographe,(85, 85))

#associé nombre 3
charpentiere = pygame.image.load("Images/Charpentière.jpeg")
charpentiere = pygame.transform.scale(charpentiere,(85, 85))

#associé nombre 4
cuistot = pygame.image.load("Images/Cuistot.jpeg")
cuistot = pygame.transform.scale(cuistot,(85, 85))

#associé nombre 5
mousse = pygame.image.load("Images/Mousse.jpeg")
mousse = pygame.transform.scale(mousse,(85, 85))

#associé nombre 6
navigatrice = pygame.image.load("Images/Navigatrice.jpeg")
navigatrice = pygame.transform.scale(navigatrice,(85, 85))

#associé nombre 7
perroquet = pygame.image.load("Images/Perroquet.jpeg")
perroquet = pygame.transform.scale(perroquet,(85, 85))

#associé nombre 8
singe = pygame.image.load("Images/Singe.jpeg")
singe = pygame.transform.scale(singe,(85, 85))

#associé nombre 9
vigie = pygame.image.load("Images/Vigie.jpeg")
vigie = pygame.transform.scale(vigie,(85, 85))

#Définition de la classe Tuile
class Tuile ():
    def __init__(self,recto,verso):
        #On définit les caractéristiques d'une Tuile
        self.recto=recto
        self.verso=verso
        self.flip=False

    #Méthode afficher pour varifier que tous se passe comme prévu
    def afficher(self):
        print(self.recto,":",self.verso)

    #Méthode pour retourner une tuile si on le souhaite
    def flipper (self):
        self.flip=not self.flip

    #Méthode qui sert à récupérer le personnage piocher
    def get_personnage(self):
        if self.flip:
            self.numero_personnage=self.verso 
        else:
            self.numero_personnage=self.recto

        if self.numero_personnage==1:
            return canonniere 
        
        elif self.numero_personnage==2:
            return cartographe 
        
        elif self.numero_personnage==3:
            return charpentiere 
        
        elif self.numero_personnage==4:
            return cuistot 
        
        elif self.numero_personnage==5:
            return mousse 
        
        elif self.numero_personnage==6:
            return navigatrice 
        
        elif self.numero_personnage==7:
            return perroquet 
        
        elif self.numero_personnage==8:
            return singe 
        
        elif self.numero_personnage==9:
            return vigie 

#Méthodes qui permettent de savoir quel personnage on a piocher  
    def is_canonniere(self):
        if self.numero_personnage==1:
            return True

    def is_cartographe(self):
        if self.numero_personnage==2:
            return True

    def is_charpentiere(self):
        if self.numero_personnage==3:
            return True

    def is_cuistot(self):
        if self.numero_personnage==4:
            return True

    def is_mousse(self):
        if self.numero_personnage==5:
            return True

    def is_navigatrice(self):
        if self.numero_personnage==6:
            return True

    def is_perroquet(self):
        if self.numero_personnage==7:
            return True

    def is_singe(self):
        if self.numero_personnage==8:
            return True

    def is_vigie(self):
        if self.numero_personnage==9:
            return True

#Création de la classe Pioche (permet de créer la pioche et de piocher une tuile)
class Pioche():
    def __init__ (self):
        #On définit les caractéristiques de la Pioche
        self.nb_tuiles=nb_personnage*(nb_personnage-1) #si jamais on change le nombre de perso
        self.la_pioche = []
        self.creer_pioche()

    #Méthode qui crée la pioche
    def creer_pioche(self):
        for i in range (1 ,nb_personnage+1) :
            for j in range (1 ,nb_personnage+1) :
                if i!=j :
                    une_carte = Tuile(i,j)
                    self.la_pioche.append(une_carte) 

    #Méthode qui récupère une tuile au hasard dans la piocher créée
    def piocher(self):
        nb=randint(0,self.nb_tuiles-1)
        self.nb_tuiles-=1
        tuile=self.la_pioche[nb]
        del(self.la_pioche[nb])
        return tuile

    #Méthode qui affiche la pioche complète pour vérifier que toutes les tuiles sont bien créées
    def afficher(self):
        for une_carte in self.la_pioche :
            une_carte.afficher()