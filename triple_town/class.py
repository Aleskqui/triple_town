import pygame
import random
pygame.display.set_caption("Triple Town")

class Grille:

    def __init__(self, screen):

        self.screen = screen
        self.cases = []
        taille_case = 150
        for y in range(5): # nombre de lignes
            for x in range(5):  # nombre de colonnes

                case_x = x * taille_case 
                case_y = y * taille_case

                # Coordonnées de chaques coins de la case
                case = ((case_x, case_y), (case_x + taille_case, case_y), (case_x + taille_case, case_y + taille_case), (case_x, case_y + taille_case))

                # On ajoute chaque cases dans une liste
                self.cases.append(case)

    def afficher(self):

        # Pour toutes les cases de la liste, on les dessine
        for i in range (len(self.cases)) :
            pygame.draw.polygon(self.screen, (0, 0, 0), self.cases[i], 2)
          # pygame.draw.polygon(taille écran, couleur, cotés du polygone, épaisseur traits dessin)

    
    def case(self):

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                 
                position_souris = pygame.mouse.get_pos()
                case_x = position_souris[0] // 150
                case_y = position_souris[1] // 150
                if case_x < 5.0:
                    print(f"Vous avez choisi la case ({case_x}, {case_y})")


class Items:

    def __init__(self):
        
        self.pierre=pygame.image.load("triple_town/img/pierre.png").convert_alpha()
        self.rocher=pygame.image.load("triple_town/img/rocher.png").convert_alpha()
        self.eglise=pygame.image.load("triple_town/img/eglise.png").convert_alpha()
        self.cathedrale=pygame.image.load("triple_town/img/cathedrale.png").convert_alpha()
        self.herbe=pygame.image.load("triple_town/img/herbe.png").convert_alpha()
        self.buisson=pygame.image.load("triple_town/img/buisson.png").convert_alpha()
        self.arbre=pygame.image.load("triple_town/img/arbre.png").convert_alpha()
        self.cabane=pygame.image.load("triple_town/img/cabane.png").convert_alpha()
        self.maison=pygame.image.load("triple_town/img/maison.png").convert_alpha()
        self.villa=pygame.image.load("triple_town/img/villa.png").convert_alpha()
        self.chateau=pygame.image.load("triple_town/img/chateau.png").convert_alpha()
        self.chateaumagique=pygame.image.load("triple_town/img/chateaumagique.png").convert_alpha()

        self.liste_items = []

    def liste(self):

        for i in range (20):
            self.liste_items.append(self.herbe)

        for i in range (15):
            self.liste_items.append(self.pierre)

        for i in range (10):
            self.liste_items.append(self.buisson)

        return random.shuffle(self.liste_items)

    
    def suivant(self):

        return self.liste_items[0]


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((1000,750))
        self.running = True
        self.grille = Grille(self.screen)
        self.items = Items()

    def jeu(self):

        # Chargement et affichage des images
        fond_jeu = pygame.image.load("triple_town/img/fond.jpg")
        fond_jeu_r = pygame.transform.scale(fond_jeu,(750,750))
        self.screen.blit(fond_jeu_r,(0,0))

        fond_score = pygame.image.load("triple_town/img/fond_score.png")
        fond_score_r = pygame.transform.scale(fond_score,(736,750))
        self.screen.blit(fond_score_r,(750,0))       

        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    

            self.grille.afficher()
            self.grille.case()

            self.items.liste()
            self.screen.blit(self.items.suivant(),(850,110))
                
            pygame.display.flip() # mise à jour de la page 
        

        pygame.quit()




if __name__ == '__main__': 
    pygame.init()
    Game().jeu()
    pygame.quit()