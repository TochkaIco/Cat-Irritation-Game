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
        self.death_font = pygame.font.Font(None, 120)
        self.sub_font = pygame.font.Font(None, 50)

    def draw_player_ui(self, screen, player):
        self.health_bar.draw(screen, player.Health, player.MaxHealth)

    def draw_death_screen(self, screen):
        # Semi-transparent red overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((100, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # "YOU DIED" text
        death_text = self.death_font.render("YOU DIED", True, (255, 0, 0))
        death_rect = death_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(death_text, death_rect)

        # Restart instruction
        restart_text = self.sub_font.render("Press 'R' to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
        screen.blit(restart_text, restart_rect)
