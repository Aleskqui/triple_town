


import pygame
import random
import numpy as np
import pygame.mixer
import webbrowser  # Pour accéder au site internet

pygame.display.set_caption("Triple Town")


# ==================================================================================================================
# ===============================================     ACCUEIL     ==================================================
# ==================================================================================================================


class Accueil:

    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 750))  # Ajustez la taille de la fenêtre ici
        # Ecran d'accueil
        self.lancement = pygame.image.load("triple_town/img/home.png")
        self.lancement = pygame.transform.scale(self.lancement, (1000, 750))

        # Bouton Play
        self.btn_play = pygame.image.load("triple_town/img/play.png")
        self.pos_play = self.btn_play.get_rect(topleft=(400, 300))  # On récupère l'emplacement (le rectangle rect) du btn play

        # Bouton Règles
        self.btn_regles = pygame.image.load("triple_town/img/btn_regles.png")
        self.pos_regles = self.btn_regles.get_rect(topleft=(350, 425))  # On récupère l'emplacement (le rectangle rect) du btn règles

        # Bouton Site Web
        self.btn_site = pygame.image.load("triple_town/img/btn-site.png")
        self.pos_site = self.btn_site.get_rect(topleft=(520, 425))  # On récupère l'emplacement (le rectangle rect) du btn site web

        # Bouton Retour
        self.btn_retour = pygame.image.load("triple_town/img/retour.png")
        self.pos_retour = self.btn_retour.get_rect(topleft=(890, 20))  # On récupère l'emplacement (le rectangle rect) du btn retour

        # Règles
        self.regles = pygame.image.load("triple_town/img/regles.png")
        self.regles = pygame.transform.scale(self.regles, (1000, 750))

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
                    webbrowser.open("https://leria-etud.univ-angers.fr/~ggascoin/projet/site/")  # On ouvre notre site web (lien à changer en fonction de la machine)

                elif self.pos_retour.collidepoint(mouse_pos):
                    self.afficher()

        return True  # L'écran d'accueil reste affiché


# ==================================================================================================================
# ===============================================     SONS    ===================================================
# ==================================================================================================================


class Son:
    def __init__(self):
        pygame.mixer.init()

    def lire_audio(self, nom_fichier):
        pygame.mixer.music.load(nom_fichier)
        pygame.mixer.music.play(-1)

    def fermer_audio(self, nom_fichier):
        pygame.mixer.music.stop()


# ==================================================================================================================
# ===============================================     GRILLE     ===================================================
# ==================================================================================================================


class Grille:
    def __init__(self, taille_x, taille_y):

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
    
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.screen = pygame.display.set_mode((1000, 750))
        self.cases = []
        self.grille = np.full((taille_x, taille_y),None, dtype=object)
        self.panier = None
        self.taille_case = 670 / taille_x
        for y in range(taille_y):  # nombre de lignes
            for x in range(taille_x):  # nombre de colonnes
                case_x = x * self.taille_case + 25
                case_y = y * self.taille_case + 25
                case = ((case_x, case_y), (case_x + self.taille_case, case_y), (case_x + self.taille_case, case_y + self.taille_case),
                        (case_x, case_y + self.taille_case))
                self.cases.append(case)
        self.derniere_position_cliquee = (0, 0)  # Initialisation de la dernière position cliquée

    def afficher(self):
        for i in range(len(self.cases)):
            pygame.draw.polygon(self.screen, (101,130,69), self.cases[i], 2)

        # Parcourir la grille pour afficher les éléments
        for y in range(self.taille_y):
            for x in range(self.taille_x):
                element = self.grille[x, y]
                if element is not None:
                    # Dessiner l'image de l'élément à sa position
                    position_x = x * self.taille_case + self.taille_case // 2
                    position_y = y * self.taille_case + self.taille_case // 2
                    image_element = self.get_image_element(element)  # Fonction à créer pour obtenir l'image correspondant à l'élément
                    if image_element is not None :
                        self.screen.blit(image_element, (position_x, position_y))
        pygame.display.flip()
        

    def case(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                position_souris = pygame.mouse.get_pos()
                case_x = (position_souris[0] -25) // self.taille_case
                case_y = (position_souris[1] -25) // self.taille_case
                if case_x < 5.0:
                    print(f"Vous avez choisi la case ({case_x}, {case_y})")

    # Place un élément à une position donnée dans la grille
    def placer_element(self, element, x, y):
        if x < self.taille_x and y < self.taille_y:
            self.grille[x, y] = element
            self.derniere_position_cliquee = (x, y)  # Enregistrer la position cliquée


    # Vérifie s'il y a un alignement de 3 éléments identiques (horizontalement ou verticalement) à partir de la position (x, y).
    # Elle renvoie les positions des éléments alignés s'il y a un alignement de 3, sinon renvoie None.

    def verifier_alignement(self, x, y):

        # Liste de toutes les directions
        coordonnées = [
            # Aligement de base
            [(0, 0), (0, 1), (0, 2)],   # Horizontal
            [(0, 0), (1, 0), (2, 0)],     # Veritcal
            [(0, 0), (1, 1), (2, 2)],    # Diagonale descendante
            [(0, 0), (1, -1), (2, -2)],      # diagonal ascendante
        
            # Alignements en L
            [(0, 0), (0, 1), (1, 0)],   # L1
            [(0, 0), (0, 1), (-1, 0)],   # L2
            [(0, 0), (-1, 0), (0, -1)],  # L3
            [(0, 0), (1, 0), (0, -1)]  # L4
        ]
        
        for directions in coordonnées:
            positions = []
            alignement = True
            for abcisses, ordonnées in directions:
                nouveau_x, nouveau_y = x + abcisses, y + ordonnées

                # on vérifie si le nouvel abcsice est >0 et est dans la grille (idem pour l'ordonné)  ET que l'élément à cette position est bien celui de la pos initial
                if 0 <= nouveau_x < self.taille_x and 0 <= nouveau_y < self.taille_y and self.grille[nouveau_x, nouveau_y] == self.grille[x, y]:
                    positions.append((nouveau_x, nouveau_y))
                else:
                    alignement = False
            if alignement:
                return positions
            
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
                    self.supprimer_elements_alignes(positions_alignement)
                    
                    dernier_x, dernier_y = self.derniere_position_cliquee  # Utilisez la dernière position cliquée

                    if element == "P" and len(positions_alignement) >= 2:
                        self.placer_element("R", dernier_x, dernier_y)  # Remplacer l'alignement par un rocher
                        game.score += 20  # Ajouter 20 points au score

                    elif element == "E" and len(positions_alignement) >= 3:
                        self.placer_element("Ba", dernier_x, dernier_y)  # Remplacer l'alignement par une basilique
                        game.score += 3000  # Ajouter 3000 points au score

                    elif element == "H" and len(positions_alignement) >= 3:
                        self.placer_element("B", dernier_x, dernier_y)  # Remplacer l'alignement par un buisson
                        game.score += 25  # Ajouter 25 points au score

                    elif element == "B" and len(positions_alignement) >= 3:
                        self.placer_element("A", dernier_x, dernier_y)  # Remplacer l'alignement par un arbre
                        game.score += 30  # Ajouter 30 points au score

                    elif element == "A" and len(positions_alignement) >= 3:
                        self.placer_element("M", dernier_x, dernier_y)  # Remplacer l'alignement par une maison
                        game.score += 600  # Ajouter 600 points au score

                    elif element == "M" and len(positions_alignement) >= 3:
                        self.placer_element("D", dernier_x, dernier_y)  # Remplacer l'alignement par une demeure
                        game.score += 2000  # Ajouter 000 points au score

                    elif element == "D" and len(positions_alignement) >= 3:
                        self.placer_element("V", dernier_x, dernier_y)  # Remplacer l'alignement par une villa
                        game.score += 3000  # Ajouter 3000 points au score

                    elif element == "V" and len(positions_alignement) >= 3:
                        self.placer_element("Ch", dernier_x, dernier_y)  # Remplacer l'alignement par un château
                        game.score += 5000  # Ajouter 5000 points au score

                    elif element == "Ch" and len(positions_alignement) >= 3:
                        self.placer_element("En", dernier_x, dernier_y)  # Remplacer l'alignement par un château enchanté
                        game.score += 10000  # Ajouter 10000 points au score

        pygame.display.flip()

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

    
    def get_image_element(self, element):
        if element == "P":
            return self.pierre
        elif element == "R":
            return self.rocher
        elif element == "E":
            return self.eglise
        elif element == "Ba":
            return self.cathedrale
        elif element == "H":
            return self.herbe
        elif element == "B":
            return self.buisson
        elif element == "A":
            return self.arbre
        elif element == "M":
            return self.cabane
        elif element == "D":
            return self.maison
        elif element == "V":
            return self.villa
        elif element == "Ch":
            return self.chateau
        elif element == "ChM":
            return self.chateaumagique
        else:
            return None
        

    def toutes_les_cases_occupees(self):
        for y in range(self.taille_y):
            for x in range(self.taille_x):
                if (x, y) != (0, 0) and self.grille[x, y] is None:
                    return False
        return True



# ==================================================================================================================
# ===============================================     ITEMS     ====================================================
# ==================================================================================================================


class Items:

    def __init__(self):


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
 

    def liste(self, repetitions=100):
        self.liste_items = ["P", "R", "E", "H", "A"]  # Exemple avec seulement deux pièces
        self.liste_items *= repetitions
        random.shuffle(self.liste_items)
        return self.liste_items

    def suivant(self):
        return self.liste_items[0]



# ==================================================================================================================
# ===============================================     GAME     =====================================================
# ==================================================================================================================


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
        self.score = 0  # Initialisation du score

        self.btn_retour = pygame.image.load("triple_town/img/retour.png")
        self.pos_retour = self.btn_retour.get_rect(topleft=(890, 20))  # On récupère l'emplacement (le rectangle rect) du btn retour
        self.son = Son()  # Ajout du lecteur audio
        self.retour_accueil_demande = False  # Nouvelle variable pour suivre si le retour à l'écran d'accueil est demandé
        self.game_over = False  # Variable pour suivre l'état du jeu
        self.record = 0  # Initialisation du record


    def afficher_score(self, compt):
        font1 = pygame.font.Font(None, 35)
        score_text = font1.render(f"{compt}", True, (108, 135, 76))
        self.screen.blit(score_text, (890, 257))
    
        # Affichage du record
        font2 = pygame.font.Font(None, 23)
        record_text = font2.render(f"{self.record}", True, (108, 135, 76))
        self.screen.blit(record_text, (889, 296))

    def bouton_retour(self, mouse_pos):
        if self.pos_retour.collidepoint(mouse_pos):
            self.retour_accueil_demande = True  # Définir la variable à True lorsque le bouton "Retour" est cliqué
    

    def reinitialiser(self):
        self.grille = Grille(5, 5)
        self.score = 0
        self.game_over = False
    
    def afficher_game_over(self):
        game_over = pygame.image.load("triple_town/img/gameover.png")
        self.screen.blit(game_over, (180, 200))
    
        # Affichage du score final
        font = pygame.font.Font(None, 50)
        final_score_text = font.render(f"Score final: {self.score}", True, (255, 0, 0))
        self.screen.blit(final_score_text, (300, 400))

        # Affichage du record
        record_text = font.render(f"Record: {self.record}", True, (255, 255, 0))
        self.screen.blit(record_text, (300, 450))

        pygame.display.flip()
        pygame.time.wait(5000)  # Attendre 5 secondes avant de fermer le jeu

    def jeu(self):
        self.son.lire_audio("triple_town/sounds/aventure.mp3")

        self.accueil = Accueil()

        while self.running:
            curseur = self.items.piece_initiales[self.piece_suivante]
            



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Gestion des clics dans la zone grise
                    if mouse_pos[0] > 670:  # zone score etc...
                        self.bouton_retour(mouse_pos)  # Gestion du clic sur le bouton "Retour"

                    # Gestion des clics dans la zone de jeu
                    else:
                        # On calcule les coordonnées de la case avec la position de la souris
                        case_x = mouse_pos[0] // (670 / self.grille.taille_x)
                        case_y = mouse_pos[1] // (670 / self.grille.taille_y)
                        # Vérifier si une pièce est déjà placée à cet emplacement
                        if (case_x, case_y) not in self.pieces_placees:
                            self.grille.placer_element(self.piece_suivante[0], int(case_x), int(case_y))  # Placer l'élément sur la grille
                            self.grille.afficher_grille_console()  # Ajouter la pièce dans la grille de la console

                            self.pieces_placees.append((case_x, case_y))  # Ajouter l'emplacement de la pièce à la liste des pièces placées
                            if self.liste_items:
                                self.piece_suivante = self.liste_items.pop(0)
                            else:
                                self.piece_suivante = None

                            if self.grille.toutes_les_cases_occupees():
                                self.afficher_game_over()
                                #self.running = False
                                self.reinitialiser()
                                self.jeu()


                            if self.score > self.record:
                                self.record = self.score
                                print(f"Nouveau record : {self.record}")  # Pour vérifier dans la console


            # SUPPRIMER ALIGNEMENT 
            for y in range(self.grille.taille_y):
                for x in range(self.grille.taille_x):
                    positions_alignement = self.grille.verifier_alignement(x, y)
                    if positions_alignement:
                        self.grille.supprimer_elements_alignes(positions_alignement) 
                        for pos in positions_alignement:
                            if pos in self.pieces_placees:
                                self.pieces_placees.remove(pos)
                        self.grille.remplacer_alignement()
                        self.grille.afficher()  # <-- Mettre à jour l'affichage de la grille dans la fenêtre graphique
            

            fond_jeu = pygame.image.load("triple_town/img/fond.png")
            self.screen.blit(fond_jeu, (0, 0))

            self.screen.blit(self.btn_retour, (890, 20))


            self.grille.afficher()  # On affiche la grille



            partie_grise = (750, 0)
            if pygame.mouse.get_pos() < partie_grise:
                pygame.mouse.set_visible(False)  # On rend invisible le curseur par défaut

                # Si il y a une pièce à placer
                if self.piece_suivante:
                    # Le curseur prend la forme de cette pièce
                    self.screen.blit(curseur, pygame.mouse.get_pos())

            else:
                pygame.mouse.set_visible(True)

           
                # Récupérer la surface correspondante à partir du dictionnaire
                if self.piece_suivante in self.items.piece_initiales:
                    surface_suivante = self.items.piece_initiales[self.piece_suivante] # Dictionnaire piece initiale (voir classe Items)
                else:
                    surface_suivante = None


            if self.piece_suivante:

                surface_suivante = self.items.piece_initiales[self.piece_suivante]  # Surface de la pièce suivante
                surface_suivante = pygame.transform.scale(surface_suivante, (35, 35))
                self.screen.blit(surface_suivante, (955, 205))

            self.afficher_score(self.score)  # Afficher le score et le record
                

            

            pygame.display.flip()

            if self.retour_accueil_demande:
                self.retour_accueil_demande = False  # Réinitialiser la variable après le retour à l'accueil
                self.son.fermer_audio("triple_town/sounds/aventure.mp3")  # Arrêter la musique de fond
                self.accueil.afficher()  # Revenir à l'écran d'accueil
                while self.accueil.en_cours():
                    pygame.time.Clock().tick(60)  # Limiter le taux de rafraîchissement pour économiser les ressources

        pygame.quit()

# ==================================================================================================================
# ===============================================     MAIN     =====================================================
# ==================================================================================================================

if __name__ == "__main__":
    pygame.init()
    game = Game()
    while True:
        # Effacer le contenu de l'écran avant d'afficher l'écran d'accueil
        game.screen.fill((0, 0, 0))  # Remplir l'écran avec une couleur noire
        
        game.accueil.afficher()
        while game.accueil.en_cours():
            pygame.time.Clock().tick(60)  # Limiter le taux de rafraîchissement pour économiser les ressources
        
        # Si le retour à l'accueil est demandé, arrêter la musique de fond
        if game.retour_accueil_demande:
            game.son.fermer_audio("triple_town/sounds/aventure.mp3")  
            game.retour_accueil_demande = False  # Réinitialiser la variable après le retour à l'accueil
        game.jeu()  # Lancer le jeu
        
