import pygame
import random
import numpy as np 
import pygame.mixer
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

        #Son
        self.son= Son()  # Ajout du lecteur audio


    def afficher(self):
        self.screen.blit(self.lancement,(0,0))
        self.screen.blit(self.btn_play,(400,300))
        self.screen.blit(self.btn_regles,(320,425))
        self.son.lire_audio("triple_town/sounds/accueil.mp3")
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
                    self.son.fermer_audio("triple_town/sounds/accueil.mp3")
                    
                    self.screen.blit(self.regles, (0, 0))  # Si c'est le cas on affiche les règles
                    self.screen.blit(self.btn_retour, (890, 20))
                    pygame.display.flip()

                elif self.pos_retour.collidepoint(mouse_pos):
                    self.pieces_placees = []
                    self.afficher()

        return True  # L'écran d'accueil reste affiché 


#==================================================================================================================
#===============================================     SONS    ===================================================
#==================================================================================================================



class Son:
    def __init__(self):
        pygame.mixer.init()

    def lire_audio(self, nom_fichier):
        pygame.mixer.music.load(nom_fichier)
        pygame.mixer.music.play()
        
    def fermer_audio(self,nom_fichier):
        pygame.mixer.music.load(nom_fichier)
        pygame.mixer.music.stop()


#==================================================================================================================
#===============================================     GRILLE     ===================================================
#==================================================================================================================

class Grille:
    def __init__(self, taille_x, taille_y):
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.screen = pygame.display.set_mode((1000,750))
        self.cases = []
        self.grille = np.zeros((taille_x,taille_y), dtype=object)
        self.panier = None
        taille_case = 750/taille_x 
        for y in range(taille_y): # nombre de lignes
            for x in range(taille_x):  # nombre de colonnes
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



    
    # Place un élément à une position donnée dans la grille
    def placer_element(self, element, x, y):
        if x <= self.taille_x and y <= self.taille_y :
            self.grille[x, y] = element
        else:  
            pass

    # Supprime un élément à une position donnée dans la grille
    def supprimer_elements(self, x, y, taille):
        for i in range(x - taille + 1, x + 1):
            for j in range(y - taille + 1, y + 1):
                if 0 <= i < self.taille_x and 0 <= j < self.taille_y:
                    self.grille[i, j] = None



    # Vérifie s'il y a un alignement de 3 éléments identiques (horizontalement ou verticalement) à partir de la position (x, y).
    # Elle renvoie l'élément aligné et la taille de l'alignement (3 dans ce cas).
    def verifier_alignement(self, x, y):
        if x + 2 < self.taille_x and self.grille[x, y] == self.grille[x + 1, y] == self.grille[x + 2, y]:
            return self.grille[x, y], 3
        # Vérifier l'alignement vertical
        if y + 2 < self.taille_y and self.grille[x, y] == self.grille[x, y + 1] == self.grille[x, y + 2]:
            return self.grille[x, y], 3
        # Vérifier l'alignement diagonal (descendant)
        if x + 2 < self.taille_x and y + 2 < self.taille_y and self.grille[x, y] == self.grille[x + 1, y + 1] == self.grille[x + 2, y + 2]:
            return self.grille[x, y], 3
        # Vérifier l'alignement diagonal (ascendant)
        if x + 2 < self.taille_x and y - 2 >= 0 and self.grille[x, y] == self.grille[x + 1, y - 1] == self.grille[x + 2, y - 2]:
            return self.grille[x, y], 3
        return None, 0
    



    def afficher_grille_console(self):
        # Affiche la grille dans la console
        for y in range(self.taille_y):
            ligne = ""
            for x in range(self.taille_x):
                element = self.grille[x, y]
                if element is None:
                    ligne += "- "
                else:
                    ligne += str(element) + " "
            print(ligne)

        if self.panier is not None:
            print(f"Panier: {self.panier}")

# Création de la grille de jeu
grille = Grille(5,5)

# Placement d'éléments dans la grille
grille.placer_element("P", 0, 0)
grille.placer_element("R", 1, 1)
grille.placer_element("E", 2, 2)
grille.placer_element("H", 3, 3)
grille.placer_element("H", 4, 3)
grille.placer_element("H", 2, 3)

grille.afficher_grille_console()


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
        self.grille = Grille(5,5)
        self.accueil = Accueil()
        self.items = Items()
        

        self.liste_items = self.items.liste()  # On initialise la liste
        self.piece_suivante = self.liste_items.pop(0) # Premiere pièce que l'on prend et supprime
        self.pieces_placees = [] # Liste pour stocker les positions des pieces dejà placées  

        self.btn_retour = pygame.image.load("triple_town/img/retour.png")
        self.pos_retour = self.btn_retour.get_rect(topleft=(890, 20)) # On recupère l'emplacement (le rectangle rect) du btn retour
        self.son= Son()  # Ajout du lecteur audio




    def score(self,compt):


        # Affichage du score courant
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {compt}", True, (255,255,0))
        self.screen.blit(score_text, (800, 120))
        



    def jeu(self):
        self.son.lire_audio("triple_town/sounds/aventure.mp3")
        positions_curseur = []
        self.accueil = Accueil()

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


                    # Gestion des clics dans la zone grise
                    
                    if mouse_pos[0] > 750 : # zone score etc... 
                        
                        if accueil.pos_retour.collidepoint(mouse_pos):
                            self.accueil.afficher()


                    # Gestion des clics dans la zone de jeu 

                    else:

                        # On calcul les coordonnés de la case avc la position de la souris
                        case_x = mouse_pos[0] // (750 / self.grille.taille_x) 
                        case_y = mouse_pos[1] // (750 / self.grille.taille_y)  
                        self.grille.placer_element(self.piece_suivante, int(case_x), int(case_y))  # Placer l'élément sur la grille
                        self.grille.afficher_grille_console()  # Ajouter la pièce dans la grille de la console
                        positions_curseur.append(event.pos)
                        compt += 1

                        if self.liste_items:
                            self.pieces_placees.append(self.piece_suivante)
                            self.piece_suivante = self.liste_items.pop(0)
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

            partie_grise = (750,0)
            if pygame.mouse.get_pos() < partie_grise:
                pygame.mouse.set_visible(False) # On rend invisible le curseur par défaut

                # Si il y a une piece à placer
                if self.piece_suivante:
                    # Le curseur prend la forme de cette pièce
                    self.screen.blit(self.piece_suivante, pygame.mouse.get_pos())

            else:
                pygame.mouse.set_visible(True)


            

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

    game = Game()
    game.jeu()

    pygame.quit()









