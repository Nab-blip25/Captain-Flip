import pygame, sys
from CF_bouton import Button
pygame.init()

# Taille de la fenêtre créée
SCREEN = pygame.display.set_mode((1280, 720))
# Nom de la fenêtre
pygame.display.set_caption("Menu")

BG = pygame.image.load("CF_blue_background.png")

# Choisir la police d'écriture
def get_font(size) :
    return pygame.font.SysFont("twcencondensedextra", size)
    
def play() :
    # Nom de la fenêtre
    pygame.display.set_caption("Play")
    
    while True :
        # Check constamment la position de la souris
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        
        # Remplit l'écran de noir pour donner l'illusion d"un nouvel écran ouvert
        SCREEN.fill("black")
        
        # Création du texte
        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        # On met le texte créé sur l'écran
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        
        # Création du bouton BACK + le mettre sur l'écran
        PLAY_BACK = Button(image=None, pos=(640,460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        
        for event in pygame.event.get() :
            # Quitter avec la croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            # Revenir au menu principal en cliquant sur le bouton BACK
            if event.type == pygame.MOUSEBUTTONDOWN :
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS) :
                    main_menu()
        
        pygame.display.update()
    
def options() :
    # Nom de la fenêtre
    pygame.display.set_caption("Options")
    
    while True :
        # Check constamment la position de la souris
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        # Remplit l'écran de noir pour donner l'illusion d"un nouvel écran ouvert
        SCREEN.fill("White")
        
        # Création du texte
        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        # On met le texte créé sur l'écran
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        # Création du bouton BACK + le mettre sur l'écran
        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        
        for event in pygame.event.get() :
            # Quitter avec la croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            # Revenir au menu principal en cliquant sur le bouton BACK
            if event.type == pygame.MOUSEBUTTONDOWN :
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS) :
                    main_menu()
                    
        pygame.display.update()
    
def main_menu() :
    # Nom de la fenêtre
    pygame.display.set_caption("Menu")
    
    while True :
        SCREEN.blit(BG, (0, 0))
        
        # Position de la souris pour savoir si on appuie sur un bouton ou si on passe dessus
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        # Texte "MAIN MENU"
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        
        # Création des 3 boutons pour naviguer dans le menu
        PLAY_BUTTON = Button(image=pygame.image.load("CF_button.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="black", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("CF_button.png"), pos=(640, 400),
                             text_input="OPTIONS", font=get_font(75), base_color="black", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("CF_button.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="black", hovering_color="White")
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        
        # On vérifie pour les trois boutons si une action est faite (appui/passage)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON] :
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            
        for event in pygame.event.get() :
            
            # Appui sur croix rouge
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
                
            # Check si on a appuyé sur la souris pour faire l'action du bouton correspondant
            if event.type == pygame.MOUSEBUTTONDOWN :
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
    
main_menu()