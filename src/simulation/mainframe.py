import pygame
from pygame import Surface

CINZA = (100, 120, 200)
MARROM = (170, 95, 30)


class Mainframe:
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 24)
        self.main_rect = pygame.Rect(800, 250, 150, 250)
        self.so_rect = pygame.Rect(805, 405, 140, 90)

    def draw(self, screen: Surface):
        pygame.draw.rect(screen, CINZA, self.main_rect)
        pygame.draw.rect(screen, MARROM, self.so_rect)
        label1 = self.font.render("Sistema", True, (0, 0, 0))
        label2 = self.font.render("Operacional", True, (0, 0, 0))

        screen.blit(label1, (self.main_rect.x + 40, self.main_rect.y + 180))
        screen.blit(label2, (self.main_rect.x + 25, self.main_rect.y + 200))
