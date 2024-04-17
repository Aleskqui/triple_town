import pygame
pygame.display.set_caption("Triple Town")

class Grille:

    def __init__(self,screen):
        self.screen = screen
        self.lignes = [((150, 0), (150, 750)),
                       ((300, 0), (300, 750)),
                       ((450, 0), (450, 750)),
                       ((600, 0), (600, 750)),
                       ((750, 0), (750, 750)),
                       ((0, 150), (750, 150)),
                       ((0, 300), (750, 300)),
                       ((0, 450), (750, 450)),
                       ((0, 600), (750, 600))]
        
    def afficher(self):

        for line in self.lignes :
            pygame.draw.line(self.screen,(0,0,0),line[0],line[1],2)

class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((1000,750))
        self.running = True
        self.grille = Grille(self.screen)

    def jeu(self):

        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        


            # Chargement et affichage des images
            fond_jeu = pygame.image.load("triple_town/img/fond.jpg")
            fond_jeu_r = pygame.transform.scale(fond_jeu,(750,750))
            self.screen.blit(fond_jeu_r,(0,0))

            fond_score = pygame.image.load("triple_town/img/fond_score.png")
            fond_score_r = pygame.transform.scale(fond_score,(736,750))
            self.screen.blit(fond_score_r,(750,0))
                

            self.grille.afficher()
            
            pygame.display.flip() # mise à jour de la page 
        

        pygame.quit




if __name__ == '__main__':
    pygame.init()
    Game().jeu()
    pygame.quit