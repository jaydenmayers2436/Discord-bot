#!/usr/bin/env python3
"""
COD Zombies FPS Game - Main Entry Point
A Python implementation of Call of Duty Zombies mechanics
"""

import pygame
import sys
import math
from game.game_engine import GameEngine
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    """Main entry point for the COD Zombies game"""
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("COD Zombies - Kino der Toten")
    
    # Hide mouse cursor and capture it
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    # Create game engine
    game_engine = GameEngine(screen)
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    print("🎮 COD Zombies Game Starting...")
    print("Controls:")
    print("  WASD - Move")
    print("  Mouse - Look around")
    print("  Mouse Click - Shoot")
    print("  ESC - Exit")
    print("-" * 40)
    
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    game_engine.handle_key_down(event.key)
            elif event.type == pygame.KEYUP:
                game_engine.handle_key_up(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_engine.handle_mouse_click(event.button)
            elif event.type == pygame.MOUSEMOTION:
                game_engine.handle_mouse_motion(event.rel)
        
        # Update game
        game_engine.update(dt)
        
        # Render game
        game_engine.render()
        
        # Update display
        pygame.display.flip()
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
