import pygame
pygame.init()

# Nom Fenêtre
pygame.display.set_caption("Triple Town")

# Dimension écran
screen = pygame.display.set_mode((1000,700))

# ======================================================================================
# ===============================   Page d'accueil   ===================================
# ======================================================================================

# Ecran d'accueil
lancement = pygame.image.load("triple_town/img/home.png")

# Bouton Play
btn_play = pygame.image.load("triple_town/img/play.png")
pos_play = btn_play.get_rect(topleft=(400, 300)) # On recupère l'emplacement (le rectangle rect) du btn play

# Bouton Règles
btn_regles = pygame.image.load("triple_town/img/btn_regles.png")
pos_regles = btn_regles.get_rect(topleft=(320, 425)) # On recupère l'emplacement (le rectangle rect) du btn regles

# Bouton Retour
btn_retour = pygame.image.load("triple_town/img/retour.png")
pos_retour = btn_regles.get_rect(topleft=(890, 20)) # On recupère l'emplacement (le rectangle rect) du btn regles

#Image des pièces
pierre=pygame.image.load("triple_town/img/pierre.png").convert_alpha()
rocher=pygame.image.load("triple_town/img/rocher.png").convert_alpha()
eglise=pygame.image.load("triple_town/img/eglise.png").convert_alpha()
cathedrale=pygame.image.load("triple_town/img/cathedrale.png").convert_alpha()
herbe=pygame.image.load("triple_town/img/herbe.png").convert_alpha()
buisson=pygame.image.load("triple_town/img/buisson.png").convert_alpha()
arbre=pygame.image.load("triple_town/img/arbre.png").convert_alpha()
cabane=pygame.image.load("triple_town/img/cabane.png").convert_alpha()
maison=pygame.image.load("triple_town/img/maison.png").convert_alpha()
villa=pygame.image.load("triple_town/img/villa.png").convert_alpha()
chateau=pygame.image.load("triple_town/img/chateau.png").convert_alpha()
chateaumagique=pygame.image.load("triple_town/img/chateaumagique.png").convert_alpha()


# Uniquement la page d'accueil est active ( = True)
accueil = True
running = False
regles = False
while accueil == True:

    # On affiche les images 
    screen.blit(lancement,(0,0))
    screen.blit(btn_play,(400,300))
    screen.blit(btn_regles,(320,425))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            accueil = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # On vérifie si on a cliqué sur le bouton jouer
            if pos_play.collidepoint(event.pos):
                print("play")
                accueil = False
                running = True


            # On vérifie si on a cliqué sur le bouton jouer
            elif pos_regles.collidepoint(event.pos):
                print("regles")
                accueil = False
                regles = True
                


# ======================================================================================
# ============================   Pages règles du jeu   =================================
# ======================================================================================


    while regles == True:

        # Chargement de l'image de fond
        fond_regles = pygame.image.load("triple_town/img/regles.png")

        # On affiche les images 
        screen.blit(fond_regles,(0,0))
        screen.blit(btn_retour,(890,20))

        pygame.display.flip() # mise à jour de la page 

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                regles = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # On vérifie si on a cliqué sur le bouton retour
                if pos_retour.collidepoint(event.pos):
                    print("retour")
                    regles = False
                    accueil = True



# ======================================================================================
# ==================================   JEU   ===========================================
# ======================================================================================

    while running == True:
        # Chargement et affichage des images
        fond_jeu = pygame.image.load("triple_town/img/fond.jpg")
        screen.blit(fond_jeu,(0,0))

        fond_score = pygame.image.load("triple_town/img/fond_score.png")
        screen.blit(fond_score,(736,0))

        screen.blit(btn_retour,(890,20))

        grille = [
            [1,2,3,4,5],
            [6,7,8,9,10],
            [11,12,13,14,15],
            [16,17,18,19,20],
            [21,22,23,24,25]
        ]

        font = pygame.font.Font(None, 36)
        case = 738/6  # Taille de chaque case
        for i in range(len(grille)):
            for j in range(len(grille[i])):
                text = font.render(str(grille[i][j]), True, (255, 255, 255))  # ecire les chiffres de la grilles
                x =  j * (case + 10)  # Calcul des coordonnées x
                y =  i * (case + 10)  # Calcul des coordonnées y
                screen.blit(text, (x, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # On vérifie si on a cliqué sur le bouton retur
                if pos_retour.collidepoint(event.pos):
                    print("retour")
                    running = False
                    accueil = True
                position_souris = pygame.mouse.get_pos()
                case_x = position_souris[0] // case
                case_y = position_souris[1] // case
                if case_x!=6.0:
                    print(f"Vous avez choisi la case ({case_x}, {case_y})")
        #Place de la pièce suivante

        screen.blit(chateau,(850,110))


        # Gestion curseur (objet à positionner)
        curseur = chateau
        pygame.mouse.set_visible(False)
        screen.blit(curseur, pygame.mouse.get_pos())

        pygame.display.flip() # mise à jour de la page


    # Fermeture de la fenêtre    
    pygame.quit
