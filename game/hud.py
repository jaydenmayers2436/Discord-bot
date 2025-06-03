"""
HUD class - Handles the heads-up display (UI elements)
"""

import pygame
from game.settings import *

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        print("✅ HUD initialized")
    
    def render(self, player, world):
        """Render all HUD elements"""
        self._render_health(player)
        self._render_ammo(player)
        self._render_points(player)
        self._render_wave_info(world)
        self._render_weapon_info(player)
    
    def _render_health(self, player):
        """Render player health bar"""
        # Health bar background
        health_bg_rect = pygame.Rect(20, SCREEN_HEIGHT - 100, 200, 20)
        pygame.draw.rect(self.screen, DARK_GRAY, health_bg_rect)
        
        # Health bar fill
        health_width = int((player.health / player.max_health) * 198)
        if health_width > 0:
            health_fill_rect = pygame.Rect(21, SCREEN_HEIGHT - 99, health_width, 18)
            # Color changes based on health level
            if player.health > 70:
                health_color = GREEN
            elif player.health > 30:
                health_color = YELLOW
            else:
                health_color = RED
            pygame.draw.rect(self.screen, health_color, health_fill_rect)
        
        # Health text
        health_text = self.font_small.render(f"Health: {player.health}/{player.max_health}", True, WHITE)
        self.screen.blit(health_text, (20, SCREEN_HEIGHT - 75))
    
    def _render_ammo(self, player):
        """Render ammo counter"""
        ammo_text = self.font_large.render(f"{player.ammo}", True, WHITE)
        text_rect = ammo_text.get_rect()
        text_rect.bottomright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)
        self.screen.blit(ammo_text, text_rect)
        
        # Ammo type
        ammo_type_text = self.font_small.render(f"/{player.max_ammo}", True, GRAY)
        type_rect = ammo_type_text.get_rect()
        type_rect.topleft = (text_rect.right, text_rect.bottom - 25)
        self.screen.blit(ammo_type_text, type_rect)
    
    def _render_points(self, player):
        """Render points counter"""
        points_text = self.font_medium.render(f"Points: {player.points}", True, YELLOW)
        self.screen.blit(points_text, (20, 20))
    
    def _render_wave_info(self, world):
        """Render current wave information"""
        wave_text = self.font_medium.render(f"Wave: {world.wave}", True, WHITE)
        text_rect = wave_text.get_rect()
        text_rect.topright = (SCREEN_WIDTH - 20, 20)
        self.screen.blit(wave_text, text_rect)
        
        # Zombies remaining
        zombies_text = self.font_small.render(f"Zombies: {len(world.zombies)}", True, RED)
        zombie_rect = zombies_text.get_rect()
        zombie_rect.topright = (SCREEN_WIDTH - 20, 55)
        self.screen.blit(zombies_text, zombie_rect)
    
    def _render_weapon_info(self, player):
        """Render current weapon information"""
        weapon_text = self.font_medium.render(player.current_weapon, True, WHITE)
        text_rect = weapon_text.get_rect()
        text_rect.bottomright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 80)
        self.screen.blit(weapon_text, text_rect)
    
    def render_message(self, message, duration=3.0):
        """Render a temporary message on screen"""
        # Center message
        message_surface = self.font_large.render(message, True, WHITE)
        text_rect = message_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Background
        bg_rect = text_rect.inflate(40, 20)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
        
        # Text
        self.screen.blit(message_surface, text_rect)
    
    def render_game_over(self, player, world):
        """Render game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        self.screen.blit(game_over_text, text_rect)
        
        # Final stats
        stats = [
            f"Wave Reached: {world.wave}",
            f"Zombies Killed: {world.zombies_killed}",
            f"Final Points: {player.points}",
            "",
            "Press ESC to exit"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.font_medium.render(stat, True, WHITE)
            stat_rect = stat_text.get_rect()
            stat_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40)
            self.screen.blit(stat_text, stat_rect)
