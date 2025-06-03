"""
Player class - Handles player movement, rotation, health, and weapons
"""

import math
from game.settings import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # Rotation angle in radians
        
        # Player stats
        self.health = PLAYER_START_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.points = 500  # Starting points
        
        # Weapon system
        self.current_weapon = "M1911"
        self.ammo = 8  # Starting pistol ammo
        self.max_ammo = 8
        
        # Movement
        self.speed = PLAYER_SPEED
        
        print(f"✅ Player created at ({x}, {y})")
    
    def update(self, dt, move_x, move_y, world):
        """Update player position and state"""
        if move_x != 0 or move_y != 0:
            # Calculate new position
            new_x = self.x + move_x * self.speed * dt * TILE_SIZE
            new_y = self.y + move_y * self.speed * dt * TILE_SIZE
            
            # Check collision with walls
            if not world.is_wall(new_x, self.y):
                self.x = new_x
            if not world.is_wall(self.x, new_y):
                self.y = new_y
    
    def rotate(self, angle_delta):
        """Rotate player by angle_delta radians"""
        self.angle += angle_delta
        # Keep angle in 0-2π range
        while self.angle < 0:
            self.angle += 2 * math.pi
        while self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
    
    def shoot(self):
        """Handle shooting"""
        if self.ammo > 0:
            self.ammo -= 1
            print(f"🔫 Shot fired! Ammo remaining: {self.ammo}")
            # TODO: Create bullet object and add to world
            return True
        else:
            print("🔫 Click! Out of ammo!")
            return False
    
    def reload(self):
        """Reload current weapon"""
        if self.ammo < self.max_ammo:
            self.ammo = self.max_ammo
            print(f"🔄 Reloaded {self.current_weapon}")
    
    def take_damage(self, damage):
        """Take damage from zombies"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print("💀 Player down!")
            return True  # Player is down
        return False
    
    def add_points(self, points):
        """Add points to player score"""
        self.points += points
        print(f"💰 +{points} points! Total: {self.points}")
    
    def spend_points(self, cost):
        """Spend points if player has enough"""
        if self.points >= cost:
            self.points -= cost
            return True
        return False
    
    def get_grid_pos(self):
        """Get player position in grid coordinates"""
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
