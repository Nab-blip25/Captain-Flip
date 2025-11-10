#Ajouter le menu
#Les comptes joueurs
#Modifier l'affichage pour dire quel joueur joue avec le nom des comptes


#Jeu (Programme principal)

import pygame
import math
from Pioche import Pioche
from CF_bouton import Button

#Initialisation de Pygame
pygame.init()

#Définition de la fenêtre
largeur, hauteur = 1500, 750
screen = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Captain flip")

#Chargement de l'arrière-plan, du plateau, du drapeau pirate, du pochon et de la carte + réduction des tailles d'images
background = pygame.image.load("Images/CF_blue_background.png")

plateau = pygame.image.load("Images/Plateau_1.jpeg")
plateau = pygame.transform.scale(plateau, (plateau.get_width() // 5, plateau.get_height() // 5))

drapeau = pygame.image.load("Images/Drapeau pirate.png")
drapeau = pygame.transform.scale(drapeau, (85, 85))

pochon = pygame.image.load("Images/Pochon.png")
pochon = pygame.transform.scale(pochon, (180, 180))

carte = pygame.image.load("Images/Carte.png")
carte = pygame.transform.scale(carte,(125,150))

#Choisir la police d'écriture
def get_font(size) :
    return pygame.font.SysFont("twcencondensedextra", size)

#Définition de la classe Case
class Case():
    def __init__(self,x,y,derniere):
        #On définit les éléments d'une case
        self.position=x,y
        self.occupee=False
        self.tuile=None
        self.derniere=derniere #Dis si c'est la dernière case de la colonne ou non
    
    #Méthode pour récupérer la position
    def position_pixel(self,position_case):
        return self.position[0]+position_case[0],self.position[1]+position_case[1]

    #Méthode d'affichage pour vérifier que tout ce passe bien
    def afficher(self):
        print(self.position,"=(",self.occupee,",",self.derniere,")")

    #Méthode qui récupère l'état d'une case
    def est_occupee(self):
        return self.occupee

    #Méthode qui change l'état d'une case si on place une tuile
    def placer_carte(self, tuile):
        self.occupee=True
        self.tuile=tuile

    #Methode pour récuperer la tuile
    def get_tuile(self):
        return self.tuile

    #Méthode qui retourne si une case est la dernière de la colonne ou non
    def est_derniere (self):
        return self.derniere

#Définition de la classe grille 
class Grille():
    def __init__(self, position):
        self.grille = [[None,None,None,Case(44,352,False),Case(44,450,True)],
                        [None,None,Case(143,254,False),Case(143,352,False),Case(143,450,True)],
                        [Case(241,59,False),Case(241,156,False),Case(241,254,False),Case(241,352,False),Case(241,450,True)],
                        [None,Case(341,156,False),Case(341,254,True),None,None],
                        [None,None,Case(440,254,False),Case(440,352,False),Case(440,450,True)]]
        self.limite = plateau.get_width(),plateau.get_height()
        self.position=position #Position de la grille
        self.derniere_case_valide=None
        self.tuile_piochee=None
        self.gain=0
        self.mode_singe=False
        self.action_realisee=False
        self.a_la_carte=False

    def placer_tuile(self,position_clic,tuile):
        position_valide=False
        #On calcule l'emplacement de la case dans la grille en fonction de la position de notre clic
        case_x = math.floor((position_clic[0]-self.position[0]-44)/100)
        case_y = math.floor((position_clic[1]-self.position[1]-44)/100)

        if self.mode_singe: #Si on a placer un singe (ou retourne un singe suite à un précédent singe)
            x,y=self.derniere_case_valide.position
            #On récupère à quelle position est placé le singe
            x=math.floor(self.derniere_case_valide.position[0]/100)
            y=math.floor(self.derniere_case_valide.position[1]/100)
            if (case_x==x and (case_y==y+1 or case_y==y-1)) or (case_y==y and (case_x==x+1 or case_x==x-1)):
                if case_x>=0 and case_x<5 and case_y>= 0 and case_y<5:
                    position_valide=True
                    case = self.grille[case_x][case_y]
                    if case!= None and case.est_occupee():
                        case.get_tuile().flipper()
                        self.mode_singe=False
                        self.tuile_piochee=None #On a plus de tuile piochée
                        self.derniere_case_valide=case #On considère la tuile flipper comme étant la dernière active et on applique les effets lorsqu'on clique sur valider
                        self.action_realisee=True #On a réalisé l'action du singe

        elif case_x>=0 and case_x<5 and case_y>= 0 and case_y<5: #On vérifie qu'on a une case comprise dans la grille
            case = self.grille[case_x][case_y]
            if case!=None and not case.est_occupee(): #On a cliquer sur une case et elle est libre
                position_valide=True
                while not case.est_derniere() and not case.est_occupee(): #On cherche si il y une case libre en dessous
                    case_y+=1
                    case=self.grille[case_x][case_y]
                    #On sort soit parce que occupée soit parce que dernière case

                if case.est_occupee():
                    case=self.grille[case_x][case_y-1]

                self.derniere_case_valide=case
            self.tuile_piochee=tuile
        return position_valide

    #Méthode qui affiche le plateau, les tuiles sur le plateau, la carte si elle est ative et le gain
    def afficher(self):
        screen.blit(plateau, self.position)
        for col in self.grille:
            for case in col:
                if case != None and case.est_occupee():
                    screen.blit(case.get_tuile().get_personnage(), case.position_pixel(self.position))
        if self.tuile_piochee!=None and self.derniere_case_valide!=None:
            screen.blit(self.tuile_piochee.get_personnage(), self.derniere_case_valide.position_pixel(self.position))
        screen.blit(get_font(50).render("Gain = "+str(self.gain), True, (0,0,0)),(self.position[0]+50,self.position[1]-50))
        if self.get_a_la_carte():
            screen.blit(carte,(self.position[0]+425,self.position[1]+25))

    def valider_placement(self):
        if self.derniere_case_valide != None and self.tuile_piochee != None :
            #On place la tuile dans la dernière case valide enregistrée
            self.derniere_case_valide.placer_carte(self.tuile_piochee)

        if self.derniere_case_valide.get_tuile().is_canonniere() :
            #Si on a une canonnière on gagne 5 points
            self.gain+=5

        elif self.derniere_case_valide.get_tuile().is_cartographe() :
            #Si on a un cartographe, on récupère la carte
            self.a_la_carte=True

        elif self.derniere_case_valide.get_tuile().is_cuistot() :
            case_y = math.floor((self.derniere_case_valide.position[1])/100) #En fonction dela position on retrouve le numéro de la ligne
            for i in range (5):
                if self.grille[i][case_y] != None and self.grille[i][case_y].est_occupee():
                    #Gain en fonction du nombre de case occupée dans la ligne du cuistot
                    self.gain+=1

        elif self.derniere_case_valide.get_tuile().is_navigatrice() :
            #On calcule le gain en focntion du nombre de cartographe présent sur le grille
            #On parcourt la grille pour retrouver le nombre de cartographe présent
            nb_cartographe=0
            for col in self.grille:
                for case in col:
                    if case != None and case.est_occupee():
                        if case.get_tuile().is_cartographe():
                            nb_cartographe+=1
                            self.gain+=2*nb_cartographe

        elif self.derniere_case_valide.get_tuile().is_singe() :
            if not self.mode_singe:
                self.gain += 1
            #On récupère la case dans laquelle est posé le singe
            x=math.floor(self.derniere_case_valide.position[0]/100)
            y=math.floor(self.derniere_case_valide.position[1]/100)
            existe_case_valide=False
            #On vérifie qu'au une case est occupée
            if x-1>=0 :
                case_gauche=self.grille[x-1][y]
                if case_gauche!=None and case_gauche.est_occupee():
                    existe_case_valide =True
            if x+1<5:
                case_droite=self.grille[x+1][y]
                if case_droite!=None and case_droite.est_occupee():
                    existe_case_valide =True
            if y-1>=0:
                case_haut=self.grille[x][y-1]
                if case_haut!=None and case_haut.est_occupee():
                    existe_case_valide =True
            if y+1<5:
                case_bas=self.grille[x][y+1]
                if case_bas!=None and case_bas.est_occupee():
                    existe_case_valide =True
            if existe_case_valide :
                #On passe en mode singe uniquement si il y a possibilité de retourner une tuile autour
                self.mode_singe=True

        #Si on complète la colonne du milieu on gagne 5 points
        if self.derniere_case_valide==self.grille[2][0]:
            self.gain+=5

        #Si on complète la colonne complètement à droite du plateau, on gagne 3 points
        if self.derniere_case_valide==self.grille[4][2]:
            self.gain+=3

        #Si on complète la colonne avec le dessin de la carte au dessus, on récupère la carte
        if self.a_la_carte:
            self.gain+=1

        #Le placement est validé, il n'y a plus de tuile piochée pour la grille
        self.tuile_piochee=None

    #Méthode qui compte au fur et à mesure le nombre de colonne pleine
    def nb_colonne_pleine(self):
        nb_colonne_remplie=0
        if self.grille[0][3].est_occupee():
            nb_colonne_remplie+=1
        if self.grille[1][2].est_occupee():
            nb_colonne_remplie+=1
        if self.grille[2][0].est_occupee():
            nb_colonne_remplie+=1
        if self.grille[3][1].est_occupee():
            nb_colonne_remplie+=1
        if self.grille[4][2].est_occupee():
            nb_colonne_remplie+=1
        return nb_colonne_remplie

    #Méthode qui permet de déclencher la fin de la partie si un des deux joueurs a compléter 4 de ses colonnes
    def fin_de_partie(self):
        return self.nb_colonne_pleine()==4

    #Méthode qui calcule les points de fin de partie (pour la charpentière, la vigie, les mousse, le perroquet)
    def gain_fin_de_partie(self):
        nb_canonniere=0
        nb_mousse=0
        nb_perroquet=0
        #On parours l'ensemble de la grille pour compter les charpentières, vigies, mousses, perroquets et cannnières
        for col in self.grille:
            for case in col:
                if case != None and case.est_occupee():
                    #On gère la charpentière
                    if case.get_tuile().is_charpentiere():
                        presence_canonniere=False
                        case_x = math.floor((case.position[0])/100) #En fonction dela position on retrouve le numéro de la colonne
                        case_y = math.floor((case.position[1])/100) #En fonction dela position on retrouve le numéro de la ligne
                        #On regarde si il y a une canonnière dans la colonne
                        for i in range (5):
                            if self.grille[i][case_y] != None and self.grille[i][case_y].est_occupee():
                                if self.grille[i][case_y].get_tuile().is_canonniere():
                                    presence_canonniere=True
                        #Si il n'y a pas de canonnière dans la colonne, on regarde si il y a une canonnière dans la ligne
                        if not presence_canonniere :
                            for j in range(5):
                                if self.grille[case_x][j] != None and self.grille[case_x][j].est_occupee():
                                    if self.grille[case_x][j].get_tuile().is_canonniere():
                                        presence_canonniere=True
                        #Si il n'y a aucune canonnière alors on gagne 3 points
                        if not presence_canonniere:
                            self.gain+=3

                    #On gère la vigie
                    if  case.get_tuile().is_vigie():
                        case_x = math.floor((case.position[0])/100)
                        case_y = math.floor((case.position[1])/100)
                        #On regarde si la case au dessus est occupée
                        if case_y==0 or self.grille[case_x][case_y-1]==None or (self.grille[case_x][case_y-1]!=None and not self.grille[case_x][case_y-1].est_occupee())  :
                        #Trois cas : on est sur la plus haute case (y=0), il n'y a pas de case au dessus (case=None), il y a une case au dessus, on vérifie qu'elle n'est pas occuppée
                            self.gain+=4

                    #On compte le nombre de canonnière présentes sur la grille
                    if case.get_tuile().is_canonniere():
                        nb_canonniere+=1
 
                    #On compte le nombre de mousse présents sur la grille
                    if case.get_tuile().is_mousse():
                        nb_mousse+=1

                    #On compte le nombre de perroquet présents sur la grille
                    if case.get_tuile().is_perroquet():
                        nb_perroquet+=1
        
        #Si on a 3 canonnières ou plus on a automatiquement perdu
        if nb_canonniere>=3:
            self.gain=0
        #Sinon on rajoute les points en fonction du nombre de mousse et de perroquet
        else:
            self.gain= self.gain + nb_mousse**2 - nb_perroquet

    #Méthode pour récupérer le gain et ainsidéfinir le gagant
    def get_gain(self):
        return self.gain

    #Méthode qui permet de récupérer la dernière case valide (case à laquelle on a poser notre tuile)
    def get_derniere_case_valide(self):
        return self.derniere_case_valide

    #Méthode qui permet de savoir on rentre dans l'action du singe
    def est_en_mode_singe(self):
        return self.mode_singe

    #Méthode qui permet de savoir si la grille a la carte
    def get_a_la_carte(self):
        return self.a_la_carte

    #Méthode qui permet de donner la case à la grille (en comlétant la colonne par exemple)
    def set_a_la_carte(self,a_la_carte):
        self.a_la_carte=a_la_carte

    #Méthode qui permet de savoir si on a compléter la colonne qui nous permet de récupérer la carte
    def case_carte(self):
        self.derniere_case_valide.afficher()
        self.grille[1][2].afficher()
        return self.derniere_case_valide==self.grille[1][2]

    #Méthode qui permet ed définir une case comme étant valide (case à laquelle on pose notre tuile)
    def set_derniere_case_valide(self,case) :
        self.derniere_case_valide=case

# Création des boutons Valider, Piocher et Flip
VALIDER = Button(image=None, pos=(largeur // 2, 544),
                        text_input="[OK]", font=get_font(50), base_color="Black", hovering_color="Green")

PIOCHER = Button(image=None, pos=(largeur // 2, 50),
                        text_input="[PIOCHER]", font=get_font(50), base_color="Black", hovering_color="Green")

FLIP = Button(image=None, pos=(largeur // 2, 100),
                        text_input="[FLIP]", font=get_font(50), base_color="Black", hovering_color="Green")

    
#Initialisation des variable 'suiveuses'
valider_clic = False # Variable qui suit l'état du bouton Valider
a_piocher=False# Variable qui suit l'état du bouton Piocher 
tuile_piochee=None #Initialisation de la tuile piochée
a_flipper=False #Suit l'état du bouton Flip
dernier_tour=False #Un p'tit tour en plus pour le joueur 2
fin_de_partie=False #Parce qu'un moment, il faut finir !
afficher_tuile_piochee=False

#Initialisation de la pioche
la_pioche=Pioche()

#Initialisation d'une grille pour chaque joueur
grille_1=Grille((100,150))
grille_2=Grille((830,150))

position_1=275,710 #Position pour aficher 'Joueur 1'
position_2=1050,710 #Position pour aficher 'Joueur 2'

#On commence par le joueur 1
joueur = 1
grille=grille_1
position_texte=position_1

# Affichage de l'arrière-plan, des plateaux, du drapeau pirate et du pochon
def affichage() :
    if fin_de_partie :
        #On calcul les points
        grille_1.gain_fin_de_partie()
        grille_2.gain_fin_de_partie()
        

    screen.blit(background, (0, 0))
    screen.blit(pochon, (500,-10))
    #Si on a pioché une tuile, on l'affiche
    if tuile_piochee != None and afficher_tuile_piochee :
        screen.blit(tuile_piochee.get_personnage(),(550,30))
    grille_1.afficher()
    grille_2.afficher()
    if not grille_1.get_a_la_carte() and not grille_2.get_a_la_carte():
        screen.blit(carte,(0,0))
    screen.blit(drapeau, (100,150))
    screen.blit(get_font(40).render("Joueur "+str(joueur), True, (0,0,0)),position_texte)

    if fin_de_partie:
    #On trouve le vainquer et on l'affiche
        if grille_1.get_gain()>grille_2.get_gain():
            #Victoire joueur 1
            screen.blit(get_font(50).render("Victoire", True, (0,0,0)),(plateau.get_width() /2+100, plateau.get_height() /2+150))

        elif grille_2.get_gain()>grille_1.get_gain():
            #Victoire joueur 2
            screen.blit(get_font(50).render("Victoire", True, (0,0,0)),(plateau.get_width() /2+830, plateau.get_height() /2+150))

        elif grille_1.get_gain()==grille_2.get_gain():
            #si égalité le détenteur de la carte gagne
            if grille_1.get_a_la_carte():
                screen.blit(get_font(50).render("Victoire", True, (0,0,0)),(plateau.get_width() /2+100, plateau.get_height() /2+150))
            elif grille_2.get_a_la_carte():
                screen.blit(get_font(50).render("Victoire", True, (0,0,0)),(plateau.get_width() /2+830, plateau.get_height() /2+150))

affichage()

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        #Si on clique sur la croix rouge on ferme la fenêtre
        if event.type == pygame.QUIT:
            running = False

        elif not fin_de_partie:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier si le bouton "Valider" est cliqué
                if VALIDER.checkForInput(event.pos):
                    # Gestion du premier tour, clique sur Valider avant de placer la carte
                    if grille.get_derniere_case_valide()!=None :
                        grille.valider_placement()
                        #On ragarde qui a la carte
                        if grille.get_derniere_case_valide().get_tuile().is_cartographe() or grille.case_carte():
                            if grille==grille_1:
                                grille_2.set_a_la_carte(False)

                            if grille==grille_2:
                                grille_1.set_a_la_carte(False)

                        if grille.case_carte():
                            #Si on compplète la colonne qui nous permet de récupérer la carte on attache la carte a cette grille
                            grille.set_a_la_carte(True)

                        if not grille.get_derniere_case_valide().get_tuile().is_perroquet() and not grille.est_en_mode_singe():
                            #On change de joueur et donc de grille sauf si c'est un perroquet ou un singe
                            if not dernier_tour :
                                if grille.fin_de_partie() :
                                    if joueur==1 : #Si c'est le joueur 1 qui termine, le joueur 2 a le droit à un dernier tour
                                        dernier_tour=True

                                    else : #Sinon c'est la fin de la partie
                                        fin_de_partie=True

                                #On change de joueur
                                if grille == grille_1:
                                    grille=grille_2
                                    joueur=2
                                    position_texte=position_2

                                elif grille==grille_2:
                                    grille=grille_1
                                    joueur=1
                                    position_texte=position_1
                            
                            else :
                                fin_de_partie=True
                            #On a fini, on réinitialise la dernière case valide        
                            grille.set_derniere_case_valide(None)

                        a_piocher=False #Le tour est terminé, on peut de nouveau de piocher
                        a_flipper=False #Le tour est terminé, on peut de nouveau flipper
                        tuile_piochee=None #Le tour est terminé, il n'y a plus de tuile piochée
                
                #Vérifier si le bouton "Piocher" est cliqué   
                if PIOCHER.checkForInput(event.pos):
                    if not a_piocher: #Pour pouvoir piocher qu'une seule fois pendant un tour             
                        tuile_piochee = la_pioche.piocher()
                        afficher_tuile_piochee=True
                        screen.blit(tuile_piochee.get_personnage(),(550,30))
                        a_piocher=True

                #Vérifier si le bouton "Flip" est cliqué
                elif FLIP.checkForInput(event.pos):
                    if not a_flipper: #Pour pouvoir flipper la tuile qu'une seule fois dans le tour
                        if tuile_piochee != None :  
                            tuile_piochee.flipper()
                            if afficher_tuile_piochee :
                                screen.blit(tuile_piochee.get_personnage(),(550,30))
                            a_flipper=True

                # Vérifier si le clic de souris est dans une case et que le bouton "Valider" n'a pas été cliqué
                elif not valider_clic:
                    if grille.placer_tuile(event.pos,tuile_piochee) :
                        #La tuile piochée est sur la grille, il ne faut plus l'afficher sur la pioche
                        afficher_tuile_piochee=False
                   
            affichage()

    #Affichage des boutons + vérification si on passe la souris dessus
    VALIDER.changeColor(pygame.mouse.get_pos())
    VALIDER.update(screen)

    PIOCHER.changeColor(pygame.mouse.get_pos())
    PIOCHER.update(screen)

    FLIP.changeColor(pygame.mouse.get_pos())
    FLIP.update(screen)

    pygame.display.flip()

pygame.quit()