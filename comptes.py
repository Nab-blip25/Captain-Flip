import pygame, sys, pygame_gui
from CF_bouton import Button
#from fichier import Fichier
#from personne import Joueur
#import pickle
pygame.init()

#registre = ["Anaïs", "Fanny", "Chemnashaovirodaintrashivu"]
fichier = open("Joueurs.txt", "r")
fichier.close()

global ECRAN
ECRAN = ""
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((1600, 900))

# Taille de la fenetre
WIDTH, HEIGHT = 1500, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# Nom de la fenetre
pygame.display.set_caption("Comptes")

# Rectangle d'input de texte dans l'ecran connexion
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH/2-300, HEIGHT/2-25), (600, 50)), manager=manager,
                                               object_id='#main_text_entry')

# Chargement des fonds d'écran
BGbateau = pygame.image.load("Images/fond_comptes.png")
BGbateau = pygame.transform.scale(BGbateau, (WIDTH, HEIGHT))

BGbateau_arrive = pygame.image.load("Images/bateau_arrive.png")
BGbateau_arrive = pygame.transform.scale(BGbateau_arrive, (WIDTH, HEIGHT))

BGjack = pygame.image.load("Images/jack.png")
BGjack = pygame.transform.scale(BGjack, (WIDTH, HEIGHT))

BGexplications = pygame.image.load("Images/Image accueil.png")
BGexplications = pygame.transform.scale(BGexplications, (WIDTH, HEIGHT))

# Choisir la police d'ecriture
def get_font(size) :
    return pygame.font.SysFont("twcencondensedextra", size)
    
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

# Premier menu avec connexion et inscription
def menu_comptes() :
    # Nom de la fenetre
    pygame.display.set_caption("Comptes")
    
    while True :
        SCREEN.blit(BGbateau, (0, 0))
        
        # Position de la souris pour savoir si on appuie sur un bouton ou si on passe dessus
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        # Texte "COMPTES"
        MENU_TEXT = get_font(160).render("COMPTES", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(450, 80))
        
        # Creation des 3 boutons pour naviguer dans le menu
        CONNEXION_BUTTON = Button(image=pygame.image.load("Images/Le_SAINT_Bouton.png"), pos=(350, 275),
                             text_input="CONNEXION", font=get_font(70), base_color="white", hovering_color="#b68f40")
        INSCRIPTION_BUTTON = Button(image=pygame.image.load("Images/Le_SAINT_Bouton.png"), pos=(350, 425),
                             text_input="INSCRIPTION", font=get_font(70), base_color="white", hovering_color="#b68f40")
        QUITTER_BUTTON = Button(image=pygame.image.load("Images/Le_SAINT_Bouton.png"), pos=(350, 575),
                             text_input="QUITTER", font=get_font(70), base_color="white", hovering_color="#b68f40")
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        
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
    
# Si compte existe    
def compte_existant(user_name):
    # blit bateau
    SCREEN.blit(BGbateau_arrive, (0, 0))
    while True:
        # On ferme la fenêtre si la croix est cliquée
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # On differencie connexion et inscription
        if ECRAN == "connexion" :
            main_menu()

        if ECRAN == "inscription" :
            new_text1 = pygame.font.SysFont("bahnschrift", 75).render("Compte du nom de", True, "black")
            new_text2 = pygame.font.SysFont("bahnschrift", 75).render(user_name, True, "black")
            new_text3 = pygame.font.SysFont("bahnschrift", 75).render("déjà existant", True, "black")
            new_text_rect1 = new_text1.get_rect(center=(WIDTH/2, HEIGHT/2-100))
            new_text_rect2 = new_text2.get_rect(center=(WIDTH/2, HEIGHT/2))
            new_text_rect3 = new_text3.get_rect(center=(WIDTH/2, HEIGHT/2+100))
            SCREEN.blit(new_text1, new_text_rect1)
            SCREEN.blit(new_text2, new_text_rect2)
            SCREEN.blit(new_text3, new_text_rect3)

        clock.tick(60)
        pygame.display.update()
        
# Si compte n'existe pas
def compte_non_existant(user_name):
    while True:
        CONNEXION_MOUSE_POS = pygame.mouse.get_pos()
        # On ferme la fenêtre si la croix est cliquée
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # On blit le background
        SCREEN.blit(BGbateau_arrive, (0, 0))
        # On affiche le texte voulu dans la police d'écriture et la couleur souhaitées
        if ECRAN == "connexion" :
            new_text1 = pygame.font.SysFont("bahnschrift", 75).render("Pas de compte du nom de", True, "black")
            new_text2 = pygame.font.SysFont("bahnschrift", 75).render(user_name, True, "black")
            new_text_rect1 = new_text1.get_rect(center=(WIDTH/2, HEIGHT/2-50))
            new_text_rect2 = new_text2.get_rect(center=(WIDTH/2, HEIGHT/2+50))
            SCREEN.blit(new_text1, new_text_rect1)
            SCREEN.blit(new_text2, new_text_rect2)
        if ECRAN == "inscription" :
            new_text1 = pygame.font.SysFont("bahnschrift", 75).render("Compte créé", True, "black")
            new_text2 = pygame.font.SysFont("bahnschrift", 75).render(user_name, True, "black")
            new_text_rect1 = new_text1.get_rect(center=(WIDTH/2, HEIGHT/2-100))
            new_text_rect2 = new_text2.get_rect(center=(WIDTH/2, HEIGHT/2))
            SCREEN.blit(new_text1, new_text_rect1)
            SCREEN.blit(new_text2, new_text_rect2)
            # Creation du bouton SE_CONNECTER + le mettre sur l'ecran
            SE_CONNECTER = Button(image=None, pos=(WIDTH/2, HEIGHT/2+100),
                            text_input="SE CONNECTER", font=get_font(75), base_color="#b68f40", hovering_color="Green")
            SE_CONNECTER.changeColor(CONNEXION_MOUSE_POS)
            SE_CONNECTER.update(SCREEN)
            # On verifie pour les trois boutons si une action est faite (appui/passage)
            SE_CONNECTER.changeColor(CONNEXION_MOUSE_POS)
            SE_CONNECTER.update(SCREEN)
            for event in pygame.event.get() :
                if event.type == pygame.MOUSEBUTTONDOWN :
                    main_menu()

        clock.tick(60)
        pygame.display.update()        

# Fonction pour prendre un texte en input qui sera le nom du compte
def get_user_name():
    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000
        # On ferme la fenêtre si la croix est cliquée
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Quand le texte est fini d'être entré
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                # Si le nom du compte existe dans le registre, fonction compte_existant
                trouve = False
                fichier = open("Joueurs.txt", "r")
                for ligne in fichier :
                    # Enleve les espaces blancs autour du texte (sauts de ligne)
                    ligne = ligne.strip()
                    noms = ligne.split()
                    if event.text in noms :
                        trouve = True
                if trouve :
                    compte_existant(event.text)
                # Si le nom du compte n'existe pas dans le registre, fonction compte_non_existant
                else :
                    compte_non_existant(event.text)
                fichier.close()
            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        SCREEN.blit(BGbateau_arrive, (0, 0))
        manager.draw_ui(SCREEN)
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
        a_labordage_BACK = Button(image=None, pos=(300,720),
                           text_input="QUITTER LE NAVIRE", font=get_font(50), base_color="white", hovering_color="Green")
        a_labordage_BACK.changeColor(a_labordage_MOUSE_POS)
        a_labordage_BACK.update(SCREEN)
        a_labordage_JEU = Button(image=None, pos=(800,720),
                           text_input="A L'ABORDAGE !", font=get_font(50), base_color="white", hovering_color="Green")
        a_labordage_JEU.changeColor(a_labordage_MOUSE_POS)
        a_labordage_JEU.update(SCREEN)

        for event in pygame.event.get() :
            # Quitter avec la croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            # Revenir au menu principal en cliquant sur le bouton RETOUR
            if event.type == pygame.MOUSEBUTTONDOWN :
                if a_labordage_JEU.checkForInput(a_labordage_MOUSE_POS) :
                    play()
                if a_labordage_BACK.checkForInput(a_labordage_MOUSE_POS) :
                    main_menu()
        
        pygame.display.update()
    
# Jeu
def play() : 
    # Nom de la fenetre
    pygame.display.set_caption("Jeu")
    
    while True :
        # Verifie constamment la position de la souris
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        
        # Remplit l'ecran de blanc pour donner l'illusion d"un nouvel ecran ouvert
        SCREEN.fill("White")
        
        # Creation du texte
        PLAY_TEXT = get_font(45).render("Veuillez lancer le fichier jeu.", True, "Black")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(WIDTH/2, HEIGHT/2-50))
        # On met le texte cree sur l'ecran
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        
        # Creation du bouton RETOUR + le mettre sur l'ecran
        PLAY_BACK = Button(image=None, pos=(WIDTH/2, HEIGHT/2+50),
                              text_input="RETOUR", font=get_font(75), base_color="Black", hovering_color="Green")
        
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        
        for event in pygame.event.get() :
            # Quitter avec la croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            # Revenir au menu principal en cliquant sur le bouton RETOUR
            if event.type == pygame.MOUSEBUTTONDOWN :
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS) :
                    a_labordage()
                    
        pygame.display.update()

def options() : 
    # Nom de la fenetre
    pygame.display.set_caption("Options")
    
    while True :
        # Verifie constamment la position de la souris
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        # Remplit l'ecran de blanc pour donner l'illusion d"un nouvel ecran ouvert
        SCREEN.fill("White")
        
        # Creation du texte
        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH/2, HEIGHT/2-50))
        # On met le texte cree sur l'ecran
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        # Creation du bouton RETOUR + le mettre sur l'ecran
        OPTIONS_BACK = Button(image=None, pos=(WIDTH/2, HEIGHT/2+50),
                              text_input="RETOUR", font=get_font(75), base_color="Black", hovering_color="Green")
        
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        
        for event in pygame.event.get() :
            # Quitter avec la croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            # Revenir au menu principal en cliquant sur le bouton RETOUR
            if event.type == pygame.MOUSEBUTTONDOWN :
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS) :
                    main_menu()
                    
        pygame.display.update()

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
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Creation des 3 boutons pour naviguer dans le menu
        JOUER_BUTTON = Button(image=pygame.image.load("Images/Le_SAINT_Bouton.png"), pos=(350, 275),
                             text_input="JOUER", font=get_font(75), base_color="white", hovering_color="#b68f40")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Images/Le_SAINT_Bouton.png"), pos=(350, 425),
                             text_input="OPTIONS", font=get_font(75), base_color="white", hovering_color="#b68f40")
        QUITTER_BUTTON = Button(image=pygame.image.load("Images/Le_SAINT_Bouton.png"), pos=(350, 575),
                             text_input="QUITTER", font=get_font(75), base_color="white", hovering_color="#b68f40")
        
        # On verifie pour les trois boutons si une action est faite (appui/passage)
        for button in [JOUER_BUTTON, OPTIONS_BUTTON, QUITTER_BUTTON] :
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            
        for event in pygame.event.get() :

            # Appui sur croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
                
            # Verifie si on a appuye sur la souris pour faire l'action du bouton correspondant
            if event.type == pygame.MOUSEBUTTONDOWN :
                if JOUER_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    a_labordage()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    options()
                if QUITTER_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
    
menu_comptes()