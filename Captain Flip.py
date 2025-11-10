# Remarque : Il est parfois nécessaire de cliquer deux fois sur le bouton se connecter
#ou d'appuyer deux fois sur entrée lors de la connexion et l'inscription
# Remarque : L'action de s'inscrire avec un compte existant revient à connecter celui-ci

# On importe tout ce qu'on a besoin pour faire fonctionner le programme
import pygame, sys, pygame_gui
from CF_bouton import Button
from Classe_Joueur import *
from Pioche import Pioche
import math
pygame.init()

# Pour faire fonctionner les classes Joueur et GestionJoueurs
gestion = GestionJoueurs("Joueurs.txt")
joueurs = gestion.charger_joueurs()

# Mise en place des variables globales
global ECRAN
ECRAN = ""
global nom_joueur1
nom_joueur1 = ""
global nom_joueur2
nom_joueur2 = ""
global compte_a_creer
compte_a_creer = False
global connexion_j1
connexion_j1 = True
global connexion_j2
connexion_j2 = True
global VICTOIRE
VICTOIRE = ""
global promotion
promotion = True

clock = pygame.time.Clock()
manager = pygame_gui.UIManager((1600, 900))

# Taille de la fenetre
WIDTH, HEIGHT = 1500, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# Nom de la fenetre
pygame.display.set_caption("Comptes")

# Rectangle d'input de texte dans l'ecran connexion
text_input = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((WIDTH/2-300, HEIGHT/2-25), (600, 50)), manager = manager,
                                               object_id = '#main_text_entry')

# Chargement des fonds d'écran, images, plateaux et réductions des tailles si besoin
BGbateau = pygame.image.load("Images/fond_comptes.png")
BGbateau = pygame.transform.scale(BGbateau, (WIDTH, HEIGHT))

BGbateau_arrive = pygame.image.load("Images/bateau_arrive.png")
BGbateau_arrive = pygame.transform.scale(BGbateau_arrive, (WIDTH, HEIGHT))

BGjack = pygame.image.load("Images/jack.png")
BGjack = pygame.transform.scale(BGjack, (WIDTH, HEIGHT))

BGexplications = pygame.image.load("Images/Image accueil.png")
BGexplications = pygame.transform.scale(BGexplications, (WIDTH, HEIGHT))

BGparchemin = pygame.image.load("Images/Parchemin.jpeg")
BGparchemin = pygame.transform.scale(BGparchemin, (WIDTH, HEIGHT))

background = pygame.image.load("Images/CF_blue_background.png")

plateau = pygame.image.load("Images/Plateau_1.jpeg")
plateau = pygame.transform.scale(plateau, (plateau.get_width() // 5, plateau.get_height() // 5))

drapeau = pygame.image.load("Images/Drapeau pirate.png")
drapeau = pygame.transform.scale(drapeau, (85, 85))

pochon = pygame.image.load("Images/Pochon.png")
pochon = pygame.transform.scale(pochon, (180, 180))

carte = pygame.image.load("Images/Carte.png")
carte = pygame.transform.scale(carte,(125,150))

# Choisir la police d'ecriture
def get_font(size) :
    return pygame.font.SysFont("twcencondensedextra", size)
    
# Premier menu avec connexion et inscription
def menu_comptes() :
    # Nom de la fenetre
    pygame.display.set_caption("Comptes")
    
    while True :
        SCREEN.blit(BGbateau, (0, 0))
        
        # Position de la souris pour savoir si on appuie sur un bouton ou si on passe dessus
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        global connexion_j1
        global connexion_j2
        if connexion_j1 : # Quand c'est au joueur 1 de se connecter
            # Texte "Joueur 1"
            MENU_TEXT = get_font(160).render("Joueur 1", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center = (550, 80))
        elif connexion_j2 : # Quand c'est au joueur 2 de se connecter
            # Texte "Joueur 2"
            MENU_TEXT = get_font(160).render("Joueur 2", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center = (550, 80))
        else : # Quand les deux joueurs sont connectes
            main_menu()
        # On affiche le texte "Joueur X"
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Creation des 3 boutons pour naviguer dans le menu
        CONNEXION_BUTTON = Button(image = pygame.image.load("Images/Le_SAINT_Bouton.png"), pos = (350, 275),
                             text_input = "CONNEXION", font = get_font(70), base_color = "white", hovering_color = "#b68f40")
        INSCRIPTION_BUTTON = Button(image = pygame.image.load("Images/Le_SAINT_Bouton.png"), pos = (350, 425),
                             text_input = "INSCRIPTION", font = get_font(70), base_color = "white", hovering_color = "#b68f40")
        QUITTER_BUTTON = Button(image = pygame.image.load("Images/Le_SAINT_Bouton.png"), pos = (350, 575),
                             text_input = "QUITTER", font = get_font(70), base_color = "white", hovering_color = "#b68f40")

        # On verifie pour les trois boutons si une action est faite (appui/passage)
        for button in [CONNEXION_BUTTON, INSCRIPTION_BUTTON, QUITTER_BUTTON] :
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            
        for event in pygame.event.get() :
            # Appui sur croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()    
            # Verifie si on a appuye sur la souris pour faire l'action du bouton correspondant
            if event.type == pygame.MOUSEBUTTONDOWN :
                global ECRAN
                if CONNEXION_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    ECRAN = "connexion"
                    connexion()
                if INSCRIPTION_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    ECRAN = "inscription"
                    connexion()
                if QUITTER_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

# Fonction permettant l'entree du nom du compte et gerant les cas possibles
def get_user_name() :
    while True :
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get() :
            # On ferme la fenêtre si la croix est cliquée
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            # Quand le texte est fini d'être entré
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#main_text_entry') :
                global nom_joueur1
                global nom_joueur2
                global connexion_j1
                global connexion_j2
                global compte_a_creer
                global ECRAN
                # Si le nom du compte existe dans le registre
                if gestion.est_enregistre(event.text) :
                    # Si on en est à la connexion du joueur 1, on garde le nom en mémoire et on passe à la connexion du joueur 2
                    if connexion_j1 :
                        nom_joueur1 = event.text
                        connexion_j1 = False
                        menu_comptes()
                    # Si on en est à la connexion du joueur 2, on passe au menu
                    else :
                        nom_joueur2 = event.text
                        connexion_j2 = False
                        menu_comptes()
                # Si le nom du compte n'existe pas dans le registre, fonction compte_non_existant
                else :
                    compte_a_creer = True
                    compte_non_existant(event.text)

            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        SCREEN.blit(BGbateau_arrive, (0, 0))
        manager.draw_ui(SCREEN)
        pygame.display.update()

# Connexion
def connexion() :
    # Nom de la fenetre
    pygame.display.set_caption("Connexion / Inscription")
    
    while True :
        get_user_name()
        for event in pygame.event.get() :
            # Quitter avec la croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        
        pygame.display.update()
        
# Si compte n'existe pas
def compte_non_existant(user_name) :
    while True :
        global compte_a_creer
        CONNEXION_MOUSE_POS = pygame.mouse.get_pos()
        # On ferme la fenêtre si la croix est cliquée
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        # On blit le background
        SCREEN.blit(BGbateau_arrive, (0, 0))
        # Si on veut se connecter
        if ECRAN == "connexion" :
            # Création du texte "Ce compte n'existe pas" et affichage sur l'écran
            new_text = pygame.font.SysFont("bahnschrift", 75).render("Ce compte n'existe pas", True, "black")
            new_text_rect = new_text.get_rect(center = (WIDTH/2, HEIGHT/2-25))
            SCREEN.blit(new_text, new_text_rect)
            # Création du bouton retour et affichage à l'écran
            BACK_BUTTON = Button(image = None, pos = (WIDTH/2, HEIGHT/2+100),
                            text_input = "RETOUR", font = get_font(60), base_color = "black", hovering_color = "green")
            BACK_BUTTON.changeColor(pygame.mouse.get_pos())
            BACK_BUTTON.update(SCREEN)
            # Si le bouton est cliqué, on fait l'action correspondante
            for event in pygame.event.get() :
                if event.type == pygame.MOUSEBUTTONDOWN and BACK_BUTTON.checkForInput(CONNEXION_MOUSE_POS) :
                    menu_comptes()
        # Si on veut s'inscrire
        if ECRAN == "inscription" :
            # Ces 3 lignes servent à enregistrer le compte une unique fois
            if compte_a_creer :
                gestion.enregistrer_joueur(Joueur(user_name))
                compte_a_creer = False
            # Creation du texte "Compte cree" et affichage a l'ecran
            new_text = pygame.font.SysFont("bahnschrift", 75).render("Compte créé", True, "black")
            new_text_rect = new_text.get_rect(center = (WIDTH/2, HEIGHT/2-25))
            SCREEN.blit(new_text, new_text_rect)
            # Sert à differencier si on inscrit le joueur 1 ou le joueur 2
            global connexion_j1
            global nom_joueur1
            global nom_joueur2
            if connexion_j1 :
                nom_joueur1 = user_name
            else :
                nom_joueur2 = user_name
            
            # Creation du bouton SE_CONNECTER + le mettre sur l'ecran
            SE_CONNECTER = Button(image = None, pos = (WIDTH/2, HEIGHT/2+100),
                            text_input = "SE CONNECTER", font = get_font(60), base_color = "black", hovering_color = "Green")
            SE_CONNECTER.changeColor(CONNEXION_MOUSE_POS)
            SE_CONNECTER.update(SCREEN)
            # On verifie si le bouton est utilisé
            SE_CONNECTER.changeColor(CONNEXION_MOUSE_POS)
            SE_CONNECTER.update(SCREEN)
            for event in pygame.event.get() :
                if event.type == pygame.MOUSEBUTTONDOWN and SE_CONNECTER.checkForInput(CONNEXION_MOUSE_POS) :
                    # Si on connecte le J1, on passe a la connexion du J2
                    if connexion_j1 :
                        connexion_j1 = False
                        menu_comptes()
                    # Si on connecte le J2, on passe au main_menu
                    else :
                        main_menu()

        clock.tick(60)
        pygame.display.update()        

# Menu principal avec les boutons jouer et statistiques
def main_menu() :
    # Nom de la fenetre
    pygame.display.set_caption("Menu")
    
    while True :
        # Affichage fond d'ecran
        SCREEN.blit(BGjack, (0, 0))
        
        # Position de la souris pour savoir si on appuie sur un bouton ou si on passe dessus
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        # Texte "MENU PRINCIPAL"
        MENU_TEXT = get_font(160).render("MENU PRINCIPAL", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center = (640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Creation des 3 boutons pour naviguer dans le menu
        JOUER_BUTTON = Button(image = pygame.image.load("Images/Le_SAINT_Bouton.png"), pos = (350, 275),
                             text_input = "JOUER", font = get_font(75), base_color = "white", hovering_color = "#b68f40")
        STATS_BUTTON = Button(image = pygame.image.load("Images/Le_SAINT_Bouton.png"), pos = (350, 425),
                             text_input = "STATS", font = get_font(75), base_color = "white", hovering_color = "#b68f40")
        QUITTER_BUTTON = Button(image = pygame.image.load("Images/Le_SAINT_Bouton.png"), pos = (350, 575),
                             text_input = "QUITTER", font = get_font(75), base_color = "white", hovering_color = "#b68f40")
        
        # On verifie pour les trois boutons si une action est faite (appui/passage)
        for button in [JOUER_BUTTON, STATS_BUTTON, QUITTER_BUTTON] :
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            
        for event in pygame.event.get() :

            # Appui sur croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
                
            # Verifie si on a appuye sur un bouton pour faire son action
            if event.type == pygame.MOUSEBUTTONDOWN :
                if JOUER_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    a_labordage()
                if STATS_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    statistiques()
                if QUITTER_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
    
# Menu des statistiques
def statistiques() : 
    # Nom de la fenetre
    pygame.display.set_caption("Statistiques")
    
    while True :
        # Verifie constamment la position de la souris
        STATS_MOUSE_POS = pygame.mouse.get_pos()
        
        # Affichage du fond d'écran
        SCREEN.blit(BGparchemin, (0, 0))
        
        # Creation du texte

        # Joueur 1

        # Captain [nom]
        J1_NOM = get_font(60).render(f"Captain {nom_joueur1}", True, "Black")
        # Victoires / Défaites
        J1_RECT_NOM = J1_NOM.get_rect(center = (WIDTH*1/4, 75))
        J1_VICTOIRES = get_font(40).render(f"Victoires : {gestion.lire_parametre(nom_joueur1, 'victoires')}", True, "Black")
        J1_RECT_VICTOIRES = J1_VICTOIRES.get_rect(center = (WIDTH*1/4, 175))
        J1_DEFAITES = get_font(40).render(f"Défaites : {gestion.lire_parametre(nom_joueur1, 'defaites')}", True, "Black")
        J1_RECT_DEFAITES = J1_DEFAITES.get_rect(center = (WIDTH*1/4, 225))
        # Grades
        J1_GRADES = get_font(40).render("Grades :", True, "Black")
        J1_RECT_GRADES = J1_GRADES.get_rect(center = (WIDTH*1/4, 300))
        J1_G1 = get_font(35).render(f"Passager clandestin : {gestion.lire_parametre(nom_joueur1, 'passager_clandestin')}", True, "Black")
        J1_RECT_G1 = J1_G1.get_rect(center = (WIDTH*1/4, 350))
        J1_G2 = get_font(35).render(f"Matelot : {gestion.lire_parametre(nom_joueur1, 'matelot')}", True, "Black")
        J1_RECT_G2 = J1_G2.get_rect(center = (WIDTH*1/4, 400))
        J1_G3 = get_font(35).render(f"Marin : {gestion.lire_parametre(nom_joueur1, 'marin')}", True, "Black")
        J1_RECT_G3 = J1_G3.get_rect(center = (WIDTH*1/4, 450))
        J1_G4 = get_font(35).render(f"Lieutenant : {gestion.lire_parametre(nom_joueur1, 'lieutenant')}", True, "Black")
        J1_RECT_G4 = J1_G4.get_rect(center = (WIDTH*1/4, 500))
        J1_G5 = get_font(35).render(f"Amiral : {gestion.lire_parametre(nom_joueur1, 'amiral')}", True, "Black")
        J1_RECT_G5 = J1_G5.get_rect(center = (WIDTH*1/4, 550))
        J1_G6 = get_font(35).render(f"Légende des mers : {gestion.lire_parametre(nom_joueur1, 'legende_des_mers')}", True, "Black")
        J1_RECT_G6 = J1_G6.get_rect(center = (WIDTH*1/4, 600))

        # Joueur 2

        # Captain [nom]
        J2_NOM = get_font(60).render(f"Captain {nom_joueur2}", True, "Black")
        # Victoires / Défaites
        J2_RECT_NOM = J2_NOM.get_rect(center = (WIDTH*3/4, 75))
        J2_VICTOIRES = get_font(40).render(f"Victoires : {gestion.lire_parametre(nom_joueur2, 'victoires')}", True, "Black")
        J2_RECT_VICTOIRES = J2_VICTOIRES.get_rect(center = (WIDTH*3/4, 175))
        J2_DEFAITES = get_font(40).render(f"Défaites : {gestion.lire_parametre(nom_joueur2, 'defaites')}", True, "Black")
        J2_RECT_DEFAITES = J2_DEFAITES.get_rect(center = (WIDTH*3/4, 225))
        # Grades
        J2_GRADES = get_font(40).render("Grades :", True, "Black")
        J2_RECT_GRADES = J2_GRADES.get_rect(center = (WIDTH*3/4, 300))
        J2_G1 = get_font(35).render(f"Passager clandestin : {gestion.lire_parametre(nom_joueur2, 'passager_clandestin')}", True, "Black")
        J2_RECT_G1 = J2_G1.get_rect(center = (WIDTH*3/4, 350))
        J2_G2 = get_font(35).render(f"Matelot : {gestion.lire_parametre(nom_joueur2, 'matelot')}", True, "Black")
        J2_RECT_G2 = J2_G2.get_rect(center = (WIDTH*3/4, 400))
        J2_G3 = get_font(35).render(f"Marin : {gestion.lire_parametre(nom_joueur2, 'marin')}", True, "Black")
        J2_RECT_G3 = J2_G3.get_rect(center = (WIDTH*3/4, 450))
        J2_G4 = get_font(35).render(f"Lieutenant : {gestion.lire_parametre(nom_joueur2, 'lieutenant')}", True, "Black")
        J2_RECT_G4 = J2_G4.get_rect(center = (WIDTH*3/4, 500))
        J2_G5 = get_font(35).render(f"Amiral : {gestion.lire_parametre(nom_joueur2, 'amiral')}", True, "Black")
        J2_RECT_G5 = J2_G5.get_rect(center = (WIDTH*3/4, 550))
        J2_G6 = get_font(35).render(f"Légende des mers : {gestion.lire_parametre(nom_joueur2, 'legende_des_mers')}", True, "Black")
        J2_RECT_G6 = J2_G6.get_rect(center = (WIDTH*3/4, 600))

        # On met le texte cree sur l'ecran
        #J1
        SCREEN.blit(J1_NOM, J1_RECT_NOM)
        SCREEN.blit(J1_VICTOIRES, J1_RECT_VICTOIRES)
        SCREEN.blit(J1_DEFAITES, J1_RECT_DEFAITES)
        SCREEN.blit(J1_GRADES, J1_RECT_GRADES)
        SCREEN.blit(J1_G1, J1_RECT_G1)
        SCREEN.blit(J1_G2, J1_RECT_G2)
        SCREEN.blit(J1_G3, J1_RECT_G3)
        SCREEN.blit(J1_G4, J1_RECT_G4)
        SCREEN.blit(J1_G5, J1_RECT_G5)
        SCREEN.blit(J1_G6, J1_RECT_G6)
        # J2
        SCREEN.blit(J2_NOM, J2_RECT_NOM)
        SCREEN.blit(J2_VICTOIRES, J2_RECT_VICTOIRES)
        SCREEN.blit(J2_DEFAITES, J2_RECT_DEFAITES)
        SCREEN.blit(J2_GRADES, J2_RECT_GRADES)
        SCREEN.blit(J2_G1, J2_RECT_G1)
        SCREEN.blit(J2_G2, J2_RECT_G2)
        SCREEN.blit(J2_G3, J2_RECT_G3)
        SCREEN.blit(J2_G4, J2_RECT_G4)
        SCREEN.blit(J2_G5, J2_RECT_G5)
        SCREEN.blit(J2_G6, J2_RECT_G6)

        # Creation du bouton RETOUR + le mettre sur l'ecran
        STATS_BACK = Button(image = None, pos = (WIDTH/2, 680),
                              text_input = "RETOUR", font = get_font(75), base_color = "Black", hovering_color = "Green")
        
        STATS_BACK.changeColor(STATS_MOUSE_POS)
        STATS_BACK.update(SCREEN)
        
        for event in pygame.event.get() :
            # Quitter avec la croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            # Revenir au menu principal en cliquant sur le bouton RETOUR
            if event.type == pygame.MOUSEBUTTONDOWN :
                if STATS_BACK.checkForInput(STATS_MOUSE_POS) :
                    main_menu()
                    
        pygame.display.update()

# Menu qui donne une petite explication du principe du jeu et qui permet de jouer
def a_labordage() :
    # Nom de la fenetre
    pygame.display.set_caption("Jouer")
    
    while True :
        # Verifie constamment la position de la souris
        a_labordage_MOUSE_POS = pygame.mouse.get_pos()
        
        # On met le fond sur l'ecran
        SCREEN.blit(BGexplications, (0, 0))
        
        # Creation des boutons + les mettre sur l'ecran
        a_labordage_BACK = Button(image = None, pos = (300,720),
                           text_input = "QUITTER LE NAVIRE", font = get_font(50), base_color = "white", hovering_color = "Green")
        a_labordage_BACK.changeColor(a_labordage_MOUSE_POS)
        a_labordage_BACK.update(SCREEN)
        a_labordage_JEU = Button(image = None, pos = (800,720),
                           text_input = "A L'ABORDAGE !", font = get_font(50), base_color = "white", hovering_color = "Green")
        a_labordage_JEU.changeColor(a_labordage_MOUSE_POS)
        a_labordage_JEU.update(SCREEN)

        for event in pygame.event.get() :
            # Quitter avec la croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            # Gestion des clics sur les boutons
            if event.type == pygame.MOUSEBUTTONDOWN :
                # Aller au jeu en cliquant sur le bouton "A L'ABORDAGE !"
                if a_labordage_JEU.checkForInput(a_labordage_MOUSE_POS) :
                    play()
                # Revenir au menu principal en cliquant sur le bouton "QUITTER LE NAVIRE"
                if a_labordage_BACK.checkForInput(a_labordage_MOUSE_POS) :
                    main_menu()
        
        pygame.display.update()
    
# Jeu
def play() : 
    #Définition de la fenêtre
    pygame.display.set_caption("Captain flip")

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
            SCREEN.blit(plateau, self.position)
            for col in self.grille:
                for case in col:
                    if case != None and case.est_occupee():
                        SCREEN.blit(case.get_tuile().get_personnage(), case.position_pixel(self.position))
            if self.tuile_piochee!=None and self.derniere_case_valide!=None:
                SCREEN.blit(self.tuile_piochee.get_personnage(), self.derniere_case_valide.position_pixel(self.position))
            SCREEN.blit(get_font(50).render("Gain = "+str(self.gain), True, (0,0,0)),(self.position[0]+50,self.position[1]-50))
            if self.get_a_la_carte():
                SCREEN.blit(carte,(self.position[0]+425,self.position[1]+25))

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
            #On parourt l'ensemble de la grille pour compter les charpentières, vigies, mousses, perroquets et cannnières
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

                        #On compte le nombre de canonnières présentes sur la grille
                        if case.get_tuile().is_canonniere():
                            nb_canonniere+=1
    
                        #On compte le nombre de mousses présents sur la grille
                        if case.get_tuile().is_mousse():
                            nb_mousse+=1

                        #On compte le nombre de perroquets présents sur la grille
                        if case.get_tuile().is_perroquet():
                            nb_perroquet+=1
            
            #Si on a 3 canonnières ou plus on a automatiquement perdu
            if nb_canonniere>=3:
                self.gain=0
            #Sinon on rajoute les points en fonction du nombre de mousses et de perroquets
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
    VALIDER = Button(image=None, pos=(WIDTH // 2, 544),
                            text_input="[OK]", font=get_font(50), base_color="Black", hovering_color="Green")

    PIOCHER = Button(image=None, pos=(WIDTH // 2, 50),
                            text_input="[PIOCHER]", font=get_font(50), base_color="Black", hovering_color="Green")

    FLIP = Button(image=None, pos=(WIDTH // 2, 100),
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
            #On calcule les points
            grille_1.gain_fin_de_partie()
            grille_2.gain_fin_de_partie()
            

        SCREEN.blit(background, (0, 0))
        SCREEN.blit(pochon, (500,-10))
        #Si on a pioché une tuile, on l'affiche
        if tuile_piochee != None and afficher_tuile_piochee :
            SCREEN.blit(tuile_piochee.get_personnage(),(550,30))
        grille_1.afficher()
        grille_2.afficher()
        if not grille_1.get_a_la_carte() and not grille_2.get_a_la_carte():
            SCREEN.blit(carte,(0,0))
        SCREEN.blit(drapeau, (100,150))
        global nom_joueur1
        global nom_joueur2
        user = ""
        if joueur == 1 :
            user = nom_joueur1
        else :
            user = nom_joueur2
        SCREEN.blit(get_font(40).render("Captain "+ user, True, (0,0,0)),position_texte)

        if fin_de_partie:
            global VICTOIRE
        #On trouve le vainqueur et on l'affiche
            if grille_1.get_gain()>grille_2.get_gain():
                #Victoire joueur 1
                VICTOIRE = Button(image=None, pos=(WIDTH/2, HEIGHT/2),
                            text_input=f"Victoire de Captain {nom_joueur1}", font=get_font(100), base_color="#b68f40", hovering_color="Green")
                gestion.incrementer_parametre(nom_joueur1, "victoires")
                gestion.incrementer_parametre(nom_joueur2, "defaites")
            elif grille_2.get_gain()>grille_1.get_gain():
                #Victoire joueur 2
                VICTOIRE = Button(image=None, pos=(WIDTH/2, HEIGHT/2),
                            text_input=f"Victoire de Captain {nom_joueur2}", font=get_font(100), base_color="#b68f40", hovering_color="Green")
                gestion.incrementer_parametre(nom_joueur2, "victoires")
                gestion.incrementer_parametre(nom_joueur1, "defaites")
            elif grille_1.get_gain()==grille_2.get_gain():
                #si égalité le détenteur de la carte gagne
                if grille_1.get_a_la_carte():
                    VICTOIRE = Button(image=None, pos=(WIDTH/2, HEIGHT/2),
                            text_input=f"Victoire de Captain {nom_joueur1}", font=get_font(100), base_color="#b68f40", hovering_color="Green")
                    gestion.incrementer_parametre(nom_joueur1, "victoires")
                    gestion.incrementer_parametre(nom_joueur2, "defaites")
                elif grille_2.get_a_la_carte():
                    VICTOIRE = Button(image=None, pos=(WIDTH/2, HEIGHT/2),
                            text_input=f"Victoire de Captain {nom_joueur2}", font=get_font(100), base_color="#b68f40", hovering_color="Green")
                    gestion.incrementer_parametre(nom_joueur2, "victoires")
                    gestion.incrementer_parametre(nom_joueur1, "defaites")
            pygame.draw.rect(SCREEN, (255, 255, 255), (WIDTH/2-500, HEIGHT/2-75, 1000, 150))
            VICTOIRE.changeColor(pygame.mouse.get_pos())
            VICTOIRE.update(SCREEN)
            #On sauvegarde la victoire et la défaite dans les comptes + les grades obtenus
            global promotion
            if promotion :
                gain1, gain2 = grille_1.get_gain(), grille_2.get_gain()
                if gain1 <= 20 :
                    gestion.incrementer_parametre(nom_joueur1, "passager_clandestin")
                elif gain1 <= 30 :
                    gestion.incrementer_parametre(nom_joueur1, "matelot")
                elif gain1 <= 40 :
                    gestion.incrementer_parametre(nom_joueur1, "marin")
                elif gain1 <= 50 :
                    gestion.incrementer_parametre(nom_joueur1, "lieutenant")
                elif gain1 <= 60 :
                    gestion.incrementer_parametre(nom_joueur1, "amiral")
                else :
                    gestion.incrementer_parametre(nom_joueur1, "legende_des_mers")
                
                if gain2 <= 20 :
                    gestion.incrementer_parametre(nom_joueur2, "passager_clandestin")
                elif gain2 <= 30 :
                    gestion.incrementer_parametre(nom_joueur2, "matelot")
                elif gain2 <= 40 :
                    gestion.incrementer_parametre(nom_joueur2, "marin")
                elif gain2 <= 50 :
                    gestion.incrementer_parametre(nom_joueur2, "lieutenant")
                elif gain2 <= 60 :
                    gestion.incrementer_parametre(nom_joueur2, "amiral")
                else :
                    gestion.incrementer_parametre(nom_joueur2, "legende_des_mers")

                promotion = False

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
                            #On regarde qui a la carte
                            if grille.get_derniere_case_valide().get_tuile().is_cartographe() or grille.case_carte():
                                if grille==grille_1:
                                    grille_2.set_a_la_carte(False)

                                if grille==grille_2:
                                    grille_1.set_a_la_carte(False)

                            if grille.case_carte():
                                #Si on complète la colonne qui nous permet de récupérer la carte on attache la carte a cette grille
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

                            a_piocher=False #Le tour est terminé, on peut de nouveau piocher
                            a_flipper=False #Le tour est terminé, on peut de nouveau flipper
                            tuile_piochee=None #Le tour est terminé, il n'y a plus de tuile piochée
                    
                    #Vérifier si le bouton "Piocher" est cliqué   
                    if PIOCHER.checkForInput(event.pos):
                        if not a_piocher: #Pour pouvoir piocher qu'une seule fois pendant un tour             
                            tuile_piochee = la_pioche.piocher()
                            afficher_tuile_piochee=True
                            SCREEN.blit(tuile_piochee.get_personnage(),(550,30))
                            a_piocher=True

                    #Vérifier si le bouton "Flip" est cliqué
                    elif FLIP.checkForInput(event.pos):
                        if not a_flipper: #Pour pouvoir flipper la tuile qu'une seule fois dans le tour
                            if tuile_piochee != None :  
                                tuile_piochee.flipper()
                                if afficher_tuile_piochee :
                                    SCREEN.blit(tuile_piochee.get_personnage(),(550,30))
                                a_flipper=True

                    # Vérifier si le clic de souris est dans une case et que le bouton "Valider" n'a pas été cliqué
                    elif not valider_clic:
                        if grille.placer_tuile(event.pos,tuile_piochee) :
                            #La tuile piochée est sur la grille, il ne faut plus l'afficher sur la pioche
                            afficher_tuile_piochee=False
                    
                affichage()
            elif fin_de_partie :
                VICTOIRE.changeColor(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONDOWN and VICTOIRE.checkForInput(event.pos) :
                    global promotion
                    promotion = True
                    main_menu()

        #Affichage des boutons + vérification si on passe la souris dessus
        VALIDER.changeColor(pygame.mouse.get_pos())
        VALIDER.update(SCREEN)

        PIOCHER.changeColor(pygame.mouse.get_pos())
        PIOCHER.update(SCREEN)

        FLIP.changeColor(pygame.mouse.get_pos())
        FLIP.update(SCREEN)

        pygame.display.flip()

    pygame.quit()

menu_comptes()