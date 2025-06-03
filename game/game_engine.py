"""
Main Game Engine - Handles game states, input, and core game loop
"""

import pygame
import math
from game.settings import *
from game.player import Player
from game.world import World
from game.renderer import Renderer
from game.hud import HUD

class GameEngine:
    def __init__(self, screen):
        self.screen = screen
        self.game_state = GAME_STATE_PLAYING  # Start directly in game for now
        
        # Initialize game components
        self.world = World()
        self.player = Player(PLAYER_START_X, PLAYER_START_Y)
        self.renderer = Renderer(screen, self.world)
        self.hud = HUD(screen)
        
        # Input handling
        self.keys_pressed = set()
        
        print("✅ Game Engine initialized")
        print(f"   Player starting at: ({PLAYER_START_X}, {PLAYER_START_Y})")
    
    def handle_key_down(self, key):
        """Handle key press events"""
        self.keys_pressed.add(key)
    
    def handle_key_up(self, key):
        """Handle key release events"""
        self.keys_pressed.discard(key)
    
    def handle_mouse_click(self, button):
        """Handle mouse click events"""
        if button == 1:  # Left click
            self.player.shoot()
    
    def handle_mouse_motion(self, rel):
        """Handle mouse movement for camera rotation"""
        if self.game_state == GAME_STATE_PLAYING:
            # Rotate player based on mouse movement
            dx, dy = rel
            self.player.rotate(dx * MOUSE_SENSITIVITY)
    
    def update(self, dt):
        """Update game logic"""
        if self.game_state == GAME_STATE_PLAYING:
            self._update_playing(dt)
    
    def _update_playing(self, dt):
        """Update game when in playing state"""
        # Handle movement input
        move_x, move_y = 0, 0
        
        if pygame.K_w in self.keys_pressed:
            move_x += math.cos(self.player.angle)
            move_y += math.sin(self.player.angle)
        if pygame.K_s in self.keys_pressed:
            move_x -= math.cos(self.player.angle)
            move_y -= math.sin(self.player.angle)
        if pygame.K_a in self.keys_pressed:
            move_x += math.cos(self.player.angle - math.pi/2)
            move_y += math.sin(self.player.angle - math.pi/2)
        if pygame.K_d in self.keys_pressed:
            move_x += math.cos(self.player.angle + math.pi/2)
            move_y += math.sin(self.player.angle + math.pi/2)
        
        # Normalize movement
        if move_x != 0 or move_y != 0:
            length = math.sqrt(move_x * move_x + move_y * move_y)
            move_x /= length
            move_y /= length
        
        # Update player
        self.player.update(dt, move_x, move_y, self.world)
        
        # Update world (zombies, bullets, etc.)
        self.world.update(dt, self.player)
    
    def render(self):
        """Render the game"""
        if self.game_state == GAME_STATE_PLAYING:
            self._render_playing()
    
    def _render_playing(self):
        """Render the game when in playing state"""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Render 3D view
        self.renderer.render_3d_view(self.player)
        
        # Render HUD
        self.hud.render(self.player, self.world)
        
        # Show debug info
        self._render_debug_info()
    
    def _render_debug_info(self):
        """Render debug information"""
        font = pygame.font.Font(None, 24)
        debug_texts = [
            f"Player Pos: ({self.player.x:.1f}, {self.player.y:.1f})",
            f"Player Angle: {math.degrees(self.player.angle):.1f}°",
            f"FPS: {pygame.time.Clock().get_fps():.1f}",
        ]
        
        for i, text in enumerate(debug_texts):
            surface = font.render(text, True, WHITE)
            self.screen.blit(surface, (10, 10 + i * 25))
