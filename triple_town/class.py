import pygame
import random
import numpy as np
import pygame.mixer
import webbrowser # Pour acceder au site internet


pygame.display.set_caption("Triple Town")


#==================================================================================================================
#===============================================     ACCUEIL     ==================================================
#==================================================================================================================


class Accueil:

    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 750))
        # Ecran d'accueil
        self.lancement = pygame.image.load("triple_town/img/home.png")

        # Bouton Play
        self.btn_play = pygame.image.load("triple_town/img/play.png")
        self.pos_play = self.btn_play.get_rect(topleft=(400, 300))  # On récupère l'emplacement (le rectangle rect) du btn play

        # Bouton Règles
        self.btn_regles = pygame.image.load("triple_town/img/btn_regles.png")
        self.pos_regles = self.btn_regles.get_rect(topleft=(350, 425))  # On récupère l'emplacement (le rectangle rect) du btn règles

        # Bouton Règles
        self.btn_site = pygame.image.load("triple_town/img/btn-site.png")
        self.pos_site = self.btn_regles.get_rect(topleft=(520, 425))  # On récupère l'emplacement (le rectangle rect) du btn règles

        # Bouton Retour
        self.btn_retour = pygame.image.load("triple_town/img/retour.png")
        self.pos_retour = self.btn_retour.get_rect(topleft=(890, 20))  # On récupère l'emplacement (le rectangle rect) du btn regles

        # Règles
        self.regles = pygame.image.load("triple_town/img/regles.png")

        # Son
        self.son = Son()  # Ajout du lecteur audio

    def afficher(self):
        self.screen.blit(self.lancement, (0, 0))
        self.screen.blit(self.btn_play, (400, 300))
        self.screen.blit(self.btn_regles, (350, 425))
        self.screen.blit(self.btn_site, (520, 425))
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

                # On vérifie si le btn site web est cliqué
                elif self.pos_site.collidepoint(mouse_pos):
                    webbrowser.open("file:///C:/Users/berna/Documents/projet/site/index.html") # On ouvre notre site web (lien à changer en fonction de la machine)

                elif self.pos_retour.collidepoint(mouse_pos):
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

    def fermer_audio(self, nom_fichier):
        pygame.mixer.music.load(nom_fichier)
        pygame.mixer.music.stop()


#==================================================================================================================
#===============================================     GRILLE     ===================================================
#==================================================================================================================


class Grille:
    def __init__(self, taille_x, taille_y):
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.screen = pygame.display.set_mode((1000, 750))
        self.cases = []
        self.grille = np.zeros((taille_x, taille_y), dtype=object)
        self.panier = None
        taille_case = 750 / taille_x
        for y in range(taille_y):  # nombre de lignes
            for x in range(taille_x):  # nombre de colonnes
                case_x = x * taille_case
                case_y = y * taille_case
                case = ((case_x, case_y), (case_x + taille_case, case_y), (case_x + taille_case, case_y + taille_case),
                        (case_x, case_y + taille_case))
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
        if x < self.taille_x and y < self.taille_y:
            self.grille[x, y] = element

    # Vérifie s'il y a un alignement de 3 éléments identiques (horizontalement ou verticalement) à partir de la position (x, y).
    # Elle renvoie les positions des éléments alignés s'il y a un alignement de 3, sinon renvoie None.
    def verifier_alignement(self, x, y):
        # Vérifier l'alignement horizontal
        if x + 2 < self.taille_x and self.grille[x, y] == self.grille[x + 1, y] == self.grille[x + 2, y]:
            return [(x, y), (x + 1, y), (x + 2, y)]
        # Vérifier l'alignement vertical
        if y + 2 < self.taille_y and self.grille[x, y] == self.grille[x, y + 1] == self.grille[x, y + 2]:
            return [(x, y), (x, y + 1), (x, y + 2)]
        # Vérifier l'alignement diagonal (descendant)
        if x + 2 < self.taille_x and y + 2 < self.taille_y and self.grille[x, y] == self.grille[x + 1, y + 1] == self.grille[x + 2, y + 2]:
            return [(x, y), (x + 1, y + 1), (x + 2, y + 2)]
        # Vérifier l'alignement diagonal (ascendant)
        if x + 2 < self.taille_x and y - 2 >= 0 and self.grille[x, y] == self.grille[x + 1, y - 1] == self.grille[x + 2, y - 2]:
            return [(x, y), (x + 1, y - 1), (x + 2, y - 2)]
        return None

    # Méthode pour supprimer les éléments de la grille à partir des positions spécifiées
    def supprimer_elements_alignes(self, positions):
        for pos in positions:
            x, y = pos
            self.grille[x, y] = None

    
    def remplacer_alignement(self):
        for y in range(self.taille_y):
            for x in range(self.taille_x):
                positions_alignement = self.verifier_alignement(x, y)
                if positions_alignement:
                    element = self.grille[x, y]

                    if element == "P":
                        if len(positions_alignement) >= 2:  # Au moins deux pierres pour former un rocher
                            self.supprimer_elements_alignes(positions_alignement)
                            self.placer_element("R", x, y)  # Remplacer l'alignement par un rocher

                    elif element == "E":
                        if len(positions_alignement) >= 3:  # Au moins trois églises pour former une basilique
                            self.supprimer_elements_alignes(positions_alignement)
                            self.placer_element("Ba", x, y)  # Remplacer l'alignement par une basilique

                    elif element == "H":
                        if len(positions_alignement) >= 3:  # Au moins trois herbes pour former un buisson
                            self.supprimer_elements_alignes(positions_alignement)
                            self.placer_element("B", x, y)  # Remplacer l'alignement par un buisson

                    elif element == "B":
                        if len(positions_alignement) >= 3:  # Au moins trois buissons pour former un arbre
                            self.supprimer_elements_alignes(positions_alignement)
                            self.placer_element("A", x, y)  # Remplacer l'alignement par un arbre

                    elif element == "A":
                        if len(positions_alignement) >= 3:  # Au moins trois arbres pour former une maison
                            self.supprimer_elements_alignes(positions_alignement)
                            self.placer_element("M", x, y)  # Remplacer l'alignement par une maison

                    elif element == "M":
                        if len(positions_alignement) >= 3:  # Au moins trois maisons pour former une demeure
                            self.supprimer_elements_alignes(positions_alignement)
                            self.placer_element("D", x, y)  # Remplacer l'alignement par une demeure

                    elif element == "D":
                        if len(positions_alignement) >= 3:  # Au moins trois demeures pour former une villa
                            self.supprimer_elements_alignes(positions_alignement)
                            self.placer_element("V", x, y)  # Remplacer l'alignement par une villa

                    elif element == "V":
                        if len(positions_alignement) >= 3:  # Au moins trois villas pour former un château
                            self.supprimer_elements_alignes(positions_alignement)
                            self.placer_element("Ch", x, y)  # Remplacer l'alignement par un château

                    elif element == "Ch":
                        if len(positions_alignement) >= 3:  # Au moins trois châteaux pour former un château enchanté
                            self.supprimer_elements_alignes(positions_alignement)
                            self.placer_element("En", x, y)  # Remplacer l'alignement par un château enchanté
    

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

        self.piece_initiales = {
            "P": pygame.image.load("triple_town/img/pierre.png").convert_alpha(),
            "R": pygame.image.load("triple_town/img/rocher.png").convert_alpha(),
            "E": pygame.image.load("triple_town/img/eglise.png").convert_alpha(),
            "H": pygame.image.load("triple_town/img/herbe.png").convert_alpha(),
            "B": pygame.image.load("triple_town/img/buisson.png").convert_alpha(),
            "A": pygame.image.load("triple_town/img/arbre.png").convert_alpha()
        }
        """
        self.piece_secondaires = {
            "Ba": pygame.image.load("triple_town/img/basilique.png").convert_alpha()
        } """

    def liste(self,repetitions=10):
        self.liste_items = ["P", "R", "E", "H", "A"]  # Exemple avec seulement deux pièces
        self.liste_items *= repetitions
        random.shuffle(self.liste_items)
        return self.liste_items

    def suivant(self):
        return self.liste_items[0]
    

    def enlever_images_alignees(self, positions_alignement):
        for pos in positions_alignement:
            x, y = pos
            for i in range(len(self.positions_curseur)):
                if (x, y) in self.positions_curseur[i]:
                    del self.positions_curseur[i]
                    break   


#==================================================================================================================
#===============================================     GAME     =====================================================
#==================================================================================================================


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 750))
        self.running = True
        self.grille = Grille(5, 5)
        self.accueil = Accueil()
        self.items = Items()

        self.liste_items = self.items.liste()  # On initialise la liste
        self.piece_suivante = self.liste_items.pop(0)  # Première pièce que l'on prend et supprime
        self.pieces_placees = []  # Liste pour stocker les positions des pièces déjà placées

        self.btn_retour = pygame.image.load("triple_town/img/retour.png")
        self.pos_retour = self.btn_retour.get_rect(topleft=(890, 20))  # On récupère l'emplacement (le rectangle rect) du btn retour
        self.son = Son()  # Ajout du lecteur audio

    def score(self, compt):

        # Affichage du score courant
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {compt}", True, (255, 255, 0))
        self.screen.blit(score_text, (800, 120))

    def jeu(self):
        self.son.lire_audio("triple_town/sounds/aventure.mp3")
        positions_curseur = []
        self.accueil = Accueil()

        while self.running:

            curseur = self.items.piece_initiales[self.piece_suivante]
            compt = 0

            for pos in positions_curseur:
                self.screen.blit(curseur, pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Gestion des clics dans la zone grise
                    if mouse_pos[0] > 750:  # zone score etc...
                        if self.accueil.pos_retour.collidepoint(mouse_pos):
                            self.accueil.afficher()

                    # Gestion des clics dans la zone de jeu
                    else:
                        # On calcule les coordonnées de la case avec la position de la souris
                        case_x = mouse_pos[0] // (750 / self.grille.taille_x)
                        case_y = mouse_pos[1] // (750 / self.grille.taille_y)
                        self.grille.placer_element(self.piece_suivante[0], int(case_x), int(case_y))  # Placer l'élément sur la grille
                        self.grille.afficher_grille_console()  # Ajouter la pièce dans la grille de la console
                        positions_curseur.append(event.pos)
                        compt += 1
                        if self.liste_items:
                            self.pieces_placees.append(self.piece_suivante)
                            self.piece_suivante = self.liste_items.pop(0)
                        else:
                            self.piece_suivante = None


            # SUPPRIMER ALIGNEMENT 
            for y in range(self.grille.taille_y):
                for x in range(self.grille.taille_x):
                    positions_alignement = self.grille.verifier_alignement(x, y)
                    if positions_alignement:
                        self.grille.supprimer_elements_alignes(positions_alignement) # En console 
                        self.items.enlever_images_alignees(positions_alignement)  # piur enlever les images alignés affichées sur le jeu
                        self.grille.remplacer_alignement()
            
            self.grille.remplacer_alignement()

            # ------------------------------------------------------------------------------
            fond_jeu = pygame.image.load("triple_town/img/fond.jpg")
            fond_jeu_r = pygame.transform.scale(fond_jeu, (750, 750))
            self.screen.blit(fond_jeu_r, (0, 0))

            fond_score = pygame.image.load("triple_town/img/fond_score.png")
            fond_score_r = pygame.transform.scale(fond_score, (736, 750))
            self.screen.blit(fond_score_r, (750, 0))

            self.screen.blit(self.btn_retour, (890, 20))
            # ------------------------------------------------------------------------------

            self.grille.afficher()  # On affiche la grille

            # ------------------------------------------------------------------------------

            partie_grise = (750, 0)
            if pygame.mouse.get_pos() < partie_grise:
                pygame.mouse.set_visible(False)  # On rend invisible le curseur par défaut

                # Si il y a une pièce à placer
                if self.piece_suivante:
                    # Le curseur prend la forme de cette pièce
                    self.screen.blit(curseur, pygame.mouse.get_pos())

            else:
                pygame.mouse.set_visible(True)

            # Pour chaque endroit où l'on a cliqué
            for i in range(min(len(positions_curseur), len(self.pieces_placees))):
                pos = positions_curseur[i]  # On prend la position
                piece = self.pieces_placees[i]  # On récupère la pièce que l'on a souhaité déposer
                piece_surface = self.items.piece_initiales[piece]  # Récupérer la surface correspondante à partir du dictionnaire
                self.screen.blit(piece_surface, pos)  # Dessiner la surface de la pièce à la position donnée

                compt += 1

            if self.piece_suivante:
                font = pygame.font.Font(None, 36)
                texte_suivant = font.render("Item à placer :", True, (255, 255, 0))
                self.screen.blit(texte_suivant, (800, 180))
                self.screen.blit(curseur, (850, 210))
            # ------------------------------------------------------------------------------

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
