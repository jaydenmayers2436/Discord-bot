"""
Renderer class - Handles 3D raycasting and rendering
"""

import pygame
import math
from game.settings import *

class Renderer:
    def __init__(self, screen, world):
        self.screen = screen
        self.world = world
        
        # Precompute some values for optimization
        self.fov_rad = math.radians(FOV)
        self.half_fov = self.fov_rad / 2
        self.angle_step = self.fov_rad / RAY_COUNT
        
        # Wall textures (simple colored rectangles for now)
        self.wall_colors = {
            1: GRAY,      # Basic wall
            2: DARK_GRAY, # Different wall type
        }
        
        print("✅ Renderer initialized")
        print(f"   FOV: {FOV}°, Ray count: {RAY_COUNT}")
    
    def render_3d_view(self, player):
        """Render the 3D first-person view using raycasting"""
        # Calculate starting angle for rays
        start_angle = player.angle - self.half_fov
        
        for ray_index in range(RAY_COUNT):
            # Calculate ray angle
            ray_angle = start_angle + ray_index * self.angle_step
            
            # Cast ray and get distance to wall
            distance, wall_type = self._cast_ray(player.x, player.y, ray_angle)
            
            # Calculate wall height on screen
            if distance > 0:
                wall_height = (TILE_SIZE / distance) * SCREEN_HEIGHT
                wall_height = min(wall_height, SCREEN_HEIGHT)  # Cap wall height
            else:
                wall_height = SCREEN_HEIGHT
            
            # Calculate wall top and bottom
            wall_top = (SCREEN_HEIGHT - wall_height) // 2
            wall_bottom = wall_top + wall_height
            
            # Get wall color
            wall_color = self.wall_colors.get(wall_type, GRAY)
            
            # Apply distance-based shading (darker = farther)
            shade_factor = max(0.1, 1.0 - (distance / RENDER_DISTANCE))
            shaded_color = tuple(int(c * shade_factor) for c in wall_color)
            
            # Calculate screen x position
            screen_x = ray_index * (SCREEN_WIDTH // RAY_COUNT)
            strip_width = SCREEN_WIDTH // RAY_COUNT
            
            # Draw ceiling (above wall)
            if wall_top > 0:
                ceiling_rect = pygame.Rect(screen_x, 0, strip_width, wall_top)
                pygame.draw.rect(self.screen, (64, 64, 128), ceiling_rect)  # Dark blue ceiling
            
            # Draw wall
            if wall_height > 0:
                wall_rect = pygame.Rect(screen_x, wall_top, strip_width, wall_height)
                pygame.draw.rect(self.screen, shaded_color, wall_rect)
            
            # Draw floor (below wall)
            if wall_bottom < SCREEN_HEIGHT:
                floor_rect = pygame.Rect(screen_x, wall_bottom, strip_width, SCREEN_HEIGHT - wall_bottom)
                pygame.draw.rect(self.screen, (32, 32, 32), floor_rect)  # Dark gray floor
        
        # Draw crosshair
        self._draw_crosshair()
    
    def _cast_ray(self, start_x, start_y, angle):
        """Cast a ray and return distance to nearest wall"""
        # Ray direction
        dx = math.cos(angle)
        dy = math.sin(angle)
        
        # Current position
        x, y = start_x, start_y
        
        # Step size for ray marching
        step_size = 4
        
        # March the ray
        distance = 0
        while distance < RENDER_DISTANCE * TILE_SIZE:
            # Move ray forward
            x += dx * step_size
            y += dy * step_size
            distance += step_size
            
            # Check if we hit a wall
            if self.world.is_wall(x, y):
                # Get wall type
                grid_x = int(x // TILE_SIZE)
                grid_y = int(y // TILE_SIZE)
                wall_type = self.world.get_wall_at(grid_x, grid_y)
                return distance, wall_type
        
        # No wall hit within render distance
        return RENDER_DISTANCE * TILE_SIZE, 0
    
    def _draw_crosshair(self):
        """Draw crosshair in center of screen"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        size = 10
        
        # Draw crosshair lines
        pygame.draw.line(self.screen, WHITE, 
                        (center_x - size, center_y), 
                        (center_x + size, center_y), 2)
        pygame.draw.line(self.screen, WHITE, 
                        (center_x, center_y - size), 
                        (center_x, center_y + size), 2)
    
    def render_minimap(self, player):
        """Render a small minimap (optional debug feature)"""
        minimap_size = 200
        minimap_scale = minimap_size / (self.world.get_map_width() * TILE_SIZE)
        
        # Create minimap surface
        minimap = pygame.Surface((minimap_size, minimap_size))
        minimap.fill(BLACK)
        
        # Draw map
        for y in range(self.world.get_map_height()):
            for x in range(self.world.get_map_width()):
                if self.world.get_wall_at(x, y) == 1:
                    rect = pygame.Rect(x * TILE_SIZE * minimap_scale, 
                                     y * TILE_SIZE * minimap_scale,
                                     TILE_SIZE * minimap_scale, 
                                     TILE_SIZE * minimap_scale)
                    pygame.draw.rect(minimap, WHITE, rect)
        
        # Draw player
        player_x = player.x * minimap_scale
        player_y = player.y * minimap_scale
        pygame.draw.circle(minimap, RED, (int(player_x), int(player_y)), 3)
        
        # Draw player direction
        end_x = player_x + math.cos(player.angle) * 10
        end_y = player_y + math.sin(player.angle) * 10
        pygame.draw.line(minimap, RED, (player_x, player_y), (end_x, end_y), 2)
        
        # Blit minimap to screen
        self.screen.blit(minimap, (SCREEN_WIDTH - minimap_size - 10, 10))
