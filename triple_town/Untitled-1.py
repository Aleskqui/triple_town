
import pygame
pygame.init()
pygame.display.set_mode((1, 1))
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


    def suivant(self):

        return self.liste_items[0]

items = Items()
items.liste()
print(items.suivant())