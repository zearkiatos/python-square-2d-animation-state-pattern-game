import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surface = pygame.Surface(size)
        self.surface.fill(color)

    @classmethod
    def from_surface(cls, surface: pygame.Surface) -> "CSurface":
        c_surface = cls(pygame.Vector2(0,0), pygame.Color(0, 0, 0))
        c_surface.surface = surface
        return c_surface