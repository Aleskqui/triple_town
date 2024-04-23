import pygame
import random
import numpy as np 
pygame.display.set_caption("Triple Town")


#==================================================================================================================
#===============================================     ACCUEIL     ==================================================
#==================================================================================================================



class Accueil:

    
    def __init__(self):
        self.screen = pygame.display.set_mode((1000,750))
        # Ecran d'accueil
        self.lancement = pygame.image.load("triple_town/img/home.png")

        # Bouton Play
        self.btn_play = pygame.image.load("triple_town/img/play.png")
        self.pos_play = self.btn_play.get_rect(topleft=(400, 300)) # On recupère l'emplacement (le rectangle rect) du btn play

        # Bouton Règles
        self.btn_regles = pygame.image.load("triple_town/img/btn_regles.png")
        self.pos_regles = self.btn_regles.get_rect(topleft=(320, 425)) # On recupère l'emplacement (le rectangle rect) du btn regles

        # Bouton Retour
        self.btn_retour = pygame.image.load("triple_town/img/retour.png")
        self.pos_retour = self.btn_retour.get_rect(topleft=(890, 20)) # On recupère l'emplacement (le rectangle rect) du btn regles

        # Règles
        self.regles = pygame.image.load("triple_town/img/regles.png")


    def afficher(self):
        self.screen.blit(self.lancement,(0,0))
        self.screen.blit(self.btn_play,(400,300))
        self.screen.blit(self.btn_regles,(320,425))
        pygame.display.flip()



    def en_cours(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                    pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # On vérifie si le btn play est cliqué
                if self.pos_play.collidepoint(mouse_pos):
                    return False  # Si c'est le cas on quitte l'accueil
                
                # On vérifie si le btn règles est cliqué
                elif self.pos_regles.collidepoint(mouse_pos):
                    
                    self.screen.blit(self.regles, (0, 0))  # Si c'est le cas on affiche les règles
                    self.screen.blit(self.btn_retour, (890, 20))
                    pygame.display.flip()

                elif self.pos_retour.collidepoint(mouse_pos):
                    self.pieces_placees = []
                    self.afficher()

        return True  # L'écran d'accueil reste affiché 





#==================================================================================================================
#===============================================     GRILLE     ===================================================
#==================================================================================================================

class Grille:
    def __init__(self, taille):
        self.grille = np.zeros(taille, dtype=object)
        self.screen = pygame.display.set_mode((1000,750))
        self.cases = []
        taille_case = 750/taille 
        for y in range(taille): # nombre de lignes
            for x in range(taille):  # nombre de colonnes
                case_x = x * taille_case 
                case_y = y * taille_case
                case = ((case_x, case_y), (case_x + taille_case, case_y), (case_x + taille_case, case_y + taille_case), (case_x, case_y + taille_case))
                self.cases.append(case)

    def afficher(self):
        for i in range(len(self.cases)):
            pygame.draw.polygon(self.screen, (0, 0, 0), self.cases[i], 2)

    def case(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                position_souris = pygame.mouse.get_pos()
                case_x = position_souris[0] // 50
                case_y = position_souris[1] // 50
                if case_x < 5.0:
                    print(f"Vous avez choisi la case ({case_x}, {case_y})")


#==================================================================================================================
#===============================================     ITEMS     ====================================================
#==================================================================================================================


class Items:


    def __init__(self):
        self.pierre = pygame.image.load("triple_town/img/pierre.png").convert_alpha()
        self.rocher = pygame.image.load("triple_town/img/rocher.png").convert_alpha()
        self.eglise = pygame.image.load("triple_town/img/eglise.png").convert_alpha()
        self.cathedrale = pygame.image.load("triple_town/img/cathedrale.png").convert_alpha()
        self.herbe = pygame.image.load("triple_town/img/herbe.png").convert_alpha()
        self.buisson = pygame.image.load("triple_town/img/buisson.png").convert_alpha()
        self.arbre = pygame.image.load("triple_town/img/arbre.png").convert_alpha()
        self.cabane = pygame.image.load("triple_town/img/cabane.png").convert_alpha()
        self.maison = pygame.image.load("triple_town/img/maison.png").convert_alpha()
        self.villa = pygame.image.load("triple_town/img/villa.png").convert_alpha()
        self.chateau = pygame.image.load("triple_town/img/chateau.png").convert_alpha()
        self.chateaumagique = pygame.image.load("triple_town/img/chateaumagique.png").convert_alpha()

        self.liste_items = []
        self.positions_curseur = []  # Liste pour stocker les positions du curseur

    def liste(self):

        self.liste_items = []

        for i in range(20):
            self.liste_items.append(self.herbe)
        for i in range(15):
            self.liste_items.append(self.pierre)
        for i in range(10):
            self.liste_items.append(self.buisson)

        random.shuffle(self.liste_items)
        return self.liste_items

    def suivant(self):
        
        return self.liste_items[0]
    





#==================================================================================================================
#===============================================     GAME     =====================================================
#==================================================================================================================


class Game:


    def __init__(self):
        self.screen = pygame.display.set_mode((1000,750))
        self.running = True
        self.grille = Grille(10)
        self.accueil = Accueil()
        self.items = Items()

        self.liste_items = self.items.liste()  # On initialise la liste
        self.piece_suivante = self.liste_items.pop(0) # Premiere pièce que l'on prend et supprime
        self.pieces_placees = [] # Liste pour stocker les positions des pieces dejà placées  

        self.btn_retour = pygame.image.load("triple_town/img/retour.png")
        self.pos_retour = self.btn_retour.get_rect(topleft=(890, 20)) # On recupère l'emplacement (le rectangle rect) du btn retour




    def score(self,compt):


        # Affichage du score courant
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {compt}", True, (255,255,0))
        self.screen.blit(score_text, (800, 120))
        



    def jeu(self):
        positions_curseur = []  # Liste pour stocker les positions du curseur  

        while self.running:
            curseur = self.piece_suivante
            compt = 0

            for pos in positions_curseur:
                self.screen.blit(curseur, pos)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False


                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    self.grille.case()
                    positions_curseur.append(event.pos)
                    compt += 1

                    if accueil.pos_retour.collidepoint(mouse_pos):
                    
                        accueil.afficher()


                    elif self.liste_items:  # Vérifie si la liste mélangée n'est pas vide
                        self.pieces_placees.append(self.piece_suivante)
                        self.piece_suivante = self.liste_items.pop(0)  # On récupère la pièce suivante (premiere de la liste que l'on supprime)

                    else:
                        self.piece_suivante = None 


            #----------------------------------------------------------------------------
            fond_jeu = pygame.image.load("triple_town/img/fond.jpg")
            fond_jeu_r = pygame.transform.scale(fond_jeu, (750, 750))
            self.screen.blit(fond_jeu_r, (0, 0))

            fond_score = pygame.image.load("triple_town/img/fond_score.png")
            fond_score_r = pygame.transform.scale(fond_score, (736, 750))
            self.screen.blit(fond_score_r, (750, 0)) 

            self.screen.blit(self.btn_retour,(890,20))
            #----------------------------------------------------------------------------


            self.grille.afficher() # On affiche la grille


            #----------------------------------------------------------------------------
            pygame.mouse.set_visible(False) # On rend invisible le curseur par défaut
            # Si il y a une piece à placer
            if self.piece_suivante:
                # Le curseur prend la forme de cette pièce
                self.screen.blit(self.piece_suivante, pygame.mouse.get_pos())

            # Pour chaque endroit ou l'on à cliqué 
            for i in range(len(positions_curseur)):
                pos = positions_curseur[i] # On prend la position
                piece = self.pieces_placees[i] # On recupère la piece que l'on a souhaité déposé
                self.screen.blit(piece, pos) # On l'a dessine

                compt += 1

            if self.piece_suivante:
                font = pygame.font.Font(None, 36)
                texte_suivant = font.render("Item à placer :", True, (255,255,0))
                self.screen.blit(texte_suivant, (800, 180))
                self.screen.blit(self.piece_suivante, (850, 210))
            #----------------------------------------------------------------------------



            self.score(compt)

            pygame.display.flip()

        pygame.quit()






#==================================================================================================================
#===============================================     MAIN     =====================================================
#==================================================================================================================



if __name__ == '__main__': 
    pygame.init()
    accueil = Accueil()
    running = False
    regles = False
    accueil.afficher()

    while accueil.en_cours():
        pass

    Game().jeu()

<<<<<<< HEAD
    pygame.quit()
=======
    pygame.quit()
>>>>>>> b408ed34f3a82ae953e77fe1d98cb31e91e2ac2e
