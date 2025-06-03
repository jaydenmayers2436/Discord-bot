"""
World class - Handles the game map, collision detection, and world objects
"""

from game.settings import *

class World:
    def __init__(self):
        # Simple Kino der Toten inspired map
        # 0 = empty space, 1 = wall
        self.map_data = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
        
        # World objects
        self.zombies = []
        self.bullets = []
        self.pickups = []
        
        # Game state
        self.wave = 1
        self.zombies_remaining = 0
        self.zombies_killed = 0
        
        print("✅ World initialized")
        print(f"   Map size: {len(self.map_data[0])}x{len(self.map_data)}")
    
    def is_wall(self, x, y):
        """Check if position (x, y) is a wall"""
        # Convert world coordinates to grid coordinates
        grid_x = int(x // TILE_SIZE)
        grid_y = int(y // TILE_SIZE)
        
        # Check bounds
        if (grid_x < 0 or grid_x >= len(self.map_data[0]) or 
            grid_y < 0 or grid_y >= len(self.map_data)):
            return True  # Out of bounds is considered a wall
        
        return self.map_data[grid_y][grid_x] == 1
    
    def get_wall_at(self, grid_x, grid_y):
        """Get wall value at grid position"""
        if (grid_x < 0 or grid_x >= len(self.map_data[0]) or 
            grid_y < 0 or grid_y >= len(self.map_data)):
            return 1  # Out of bounds
        return self.map_data[grid_y][grid_x]
    
    def update(self, dt, player):
        """Update world objects"""
        # Update zombies
        for zombie in self.zombies[:]:  # Copy list to avoid modification issues
            zombie.update(dt, player, self)
            if zombie.health <= 0:
                self.zombies.remove(zombie)
                self.zombies_killed += 1
                player.add_points(POINTS_PER_KILL)
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update(dt, self)
            if bullet.should_remove:
                self.bullets.remove(bullet)
        
        # Check if wave is complete
        if len(self.zombies) == 0 and self.zombies_remaining == 0:
            self._start_next_wave()
    
    def _start_next_wave(self):
        """Start the next wave of zombies"""
        self.wave += 1
        self.zombies_remaining = self.wave * 6  # More zombies each wave
        print(f"🌊 Wave {self.wave} starting! {self.zombies_remaining} zombies incoming!")
    
    def spawn_zombie(self, x, y):
        """Spawn a zombie at position (x, y)"""
        # TODO: Implement zombie class and spawning
        pass
    
    def add_bullet(self, bullet):
        """Add a bullet to the world"""
        self.bullets.append(bullet)
    
    def get_map_width(self):
        """Get map width in tiles"""
        return len(self.map_data[0])
    
    def get_map_height(self):
        """Get map height in tiles"""
        return len(self.map_data)
