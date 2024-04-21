import pygame
import random
import numpy as np 
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
pieces=[pygame.image.load("triple_town/img/pierre.png").convert_alpha(),
pygame.image.load("triple_town/img/rocher.png").convert_alpha(),
pygame.image.load("triple_town/img/eglise.png").convert_alpha(),
pygame.image.load("triple_town/img/cathedrale.png").convert_alpha(),
pygame.image.load("triple_town/img/herbe.png").convert_alpha(),
pygame.image.load("triple_town/img/buisson.png").convert_alpha(),
pygame.image.load("triple_town/img/arbre.png").convert_alpha(),
pygame.image.load("triple_town/img/cabane.png").convert_alpha(),
pygame.image.load("triple_town/img/maison.png").convert_alpha(),
pygame.image.load("triple_town/img/villa.png").convert_alpha(),
pygame.image.load("triple_town/img/chateau.png").convert_alpha(),
pygame.image.load("triple_town/img/chateaumagique.png").convert_alpha()]


#Couleur de texte
Noir = (0, 0, 0)
Blanc = (255, 255, 255)
Gris = (128, 128, 128)
Vert=(78,189,34)

# Score
score = 0

# Définition des éléments du jeu
class Element:
    def __init__(self, nom, symbole, sprite):
        self.nom = nom
        self.symbole = symbole
        self.sprite = sprite

# Création des éléments
pierre = Element("pierre", "P", pieces[0])
rocher = Element("rocher", "R", pieces[1])
eglise = Element("église", "E", pieces[2])
basilique = Element("basilique", "B", pieces[3])
herbe = Element("herbe", "H", pieces[4])
buisson = Element("buisson", "B", pieces[5])
arbre = Element("arbre", "A", pieces[6])
maison = Element("cabane", "CA", pieces[7])
demeure = Element("maison", "M", pieces[8])
villa = Element("villa", "V", pieces[9])
chateau = Element("château", "C", pieces[10])
chateau_enchante = Element("château magique", "CM", pieces[11])

# Chargement des fichiers sons
son_jeu = pygame.mixer.Sound("triple_town/sounds/aventure.mp3")
son_accueil = pygame.mixer.Sound("triple_town/sounds/accueil.mp3")

# Modélisation de l'aire de jeu
class Grille:
    #La grille est modélisée sous forme d'une matrice de taille taille_x x taille_y, où chaque case peut contenir un élément du jeu (de type Element) ou être vide (None). La grille possède également un "panier" qui permet de stocker temporairement un élément.
    def __init__(self, taille_x, taille_y):
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.grille = np.zeros((taille_x, taille_y), dtype=object)
        self.panier = None
    # Place un élément à une position donnée dans la grille
    def placer_element(self, element, x, y):
        self.grille[x, y] = element
    # Supprime un élément à une position donnée dans la grille
    def supprimer_elements(self, x, y, taille):
        for i in range(x - taille + 1, x + 1):
            for j in range(y - taille + 1, y + 1):
                if 0 <= i < self.taille_x and 0 <= j < self.taille_y:
                    self.grille[i, j] = None
    
    
    #Vérifie s'il y a un alignement de 3 éléments identiques (horizontalement ou verticalement) à partir de la position (x, y). Elle renvoie l'élément aligné et la taille de l'alignement (3 dans ce cas).
    def verifier_alignement(self, x, y):
        # Vérifier l'alignement horizontal
        if x + 2 < self.taille_x and self.grille[x, y] == self.grille[x + 1, y] == self.grille[x + 2, y]:
            return self.grille[x, y], 3
        # Vérifier l'alignement vertical
        if y + 2 < self.taille_y and self.grille[x, y] == self.grille[x, y + 1] == self.grille[x, y + 2]:
            return self.grille[x, y], 3
        return None, 0

    def update(self):
        # Logique de mise à jour de la grille
        pass

# Création de la grille de jeu
grille = Grille(5, 5)

# Placement d'éléments dans la grille
grille.placer_element(pierre, 0, 0)
grille.placer_element(rocher, 1, 1)
grille.placer_element(eglise, 2, 2)
grille.placer_element(basilique, 3, 3)
grille.placer_element(herbe, 4, 4)

# Vérification de l'alignement
element, taille = grille.verifier_alignement(0, 0)
if element:
    print(f"Alignement de {element.nom} sur {taille} cases")
    grille.supprimer_elements(0, 0, taille)

# Uniquement la page d'accueil est active ( = True)
accueil = True
running = False
regles = False


son_accueil.play()
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
                son_accueil.stop()
                son_jeu.play() 


            # On vérifie si on a cliqué sur le bouton jouer
            elif pos_regles.collidepoint(event.pos):
                print("regles")
                accueil = False
                regles = True
                son_accueil.stop()
                son_jeu.stop() 
                


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
                    son_jeu.stop()
                    son_accueil.play()



# ======================================================================================
# ==================================   JEU   ===========================================
# ======================================================================================



    positions_curseur = []  # Liste pour stocker les positions du curseur
    piece_suivante = random.choice(pieces)  # Choisir une pièce aléatoirement


    while running == True:
        # Chargement et affichage des images
        fond_jeu = pygame.image.load("triple_town/img/fond.jpg")
        screen.blit(fond_jeu,(0,0))

        fond_score = pygame.image.load("triple_town/img/fond_score.png")
        screen.blit(fond_score,(736,0))

        # Affichage du score courant
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, Blanc)
        screen.blit(score_text, (750, 20))

        screen.blit(btn_retour,(890,20))



        # Gestion curseur (objet à positionner)  --TEST
        curseur = piece_suivante
        pygame.mouse.set_visible(False)
        screen.blit(curseur, pygame.mouse.get_pos())



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



        # Afficher le curseur à toutes les positions enregistrées
        for pos in positions_curseur:
            screen.blit(curseur, pos)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # On vérifie si on a cliqué sur le bouton retur
                if pos_retour.collidepoint(event.pos):
                    print("retour")
                    running = False
                    accueil = True
                    son_jeu.stop()
                    son_accueil.play()

                else:

                    position_souris = pygame.mouse.get_pos()
                    if position_souris[0] < 710:  # Vérifier si la position est en dehors de la zone du score
                        positions_curseur.append(position_souris)
                    case_x = position_souris[0] // case
                    case_y = position_souris[1] // case
                    if case_x!=6.0:
                        print(f"Vous avez choisi la case ({case_x}, {case_y})")
                        score += 1  # Incrémenter le score
                        piece_suivante = random.choice(pieces)  # Choisir une pièce aléatoirement



        #Place de la pièce suivante
        screen.blit(piece_suivante,(850,110))


       

        pygame.display.flip() # mise à jour de la page


    # Fermeture de la fenêtre    
    pygame.quit
