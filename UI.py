import pygame
from AssetManager import AssetManager

class HealthBar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base_image = AssetManager.get_image("Images/Cat_health_bar.png")
        self.inner_image = AssetManager.get_image("Images/Cat_health_bar_Insides.png")

    def draw(self, screen, current_health, max_health):
        if current_health > 0:
            # Calculate the width of the health portion
            health_percentage = current_health / max_health
            # The original code used 334 as the width for the inner bar
            inner_width = int(334 * health_percentage)
            if inner_width > 0:
                cropped_health_inner = pygame.Surface((inner_width, 99), pygame.SRCALPHA)
                cropped_health_inner.blit(self.inner_image, (0, 0))
                screen.blit(cropped_health_inner, (self.x, self.y))
        
        screen.blit(self.base_image, (self.x, self.y))

class UIManager:
    def __init__(self):
        self.health_bar = HealthBar(20, 20)

    def draw_player_ui(self, screen, player):
        self.health_bar.draw(screen, player.Health, player.MaxHealth)
