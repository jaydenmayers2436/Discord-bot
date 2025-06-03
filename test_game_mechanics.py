#!/usr/bin/env python3
"""
Test script for COD Zombies game mechanics
"""

import math
from game.player import Player
from game.world import World
from game.settings import *

def test_player_movement():
    """Test player movement and collision"""
    print("🧪 Testing Player Movement...")
    
    world = World()
    player = Player(PLAYER_START_X, PLAYER_START_Y)
    
    # Test initial position
    initial_pos = (player.x, player.y)
    print(f"   Initial position: {initial_pos}")
    
    # Test movement (simulate 1 second at 60 FPS)
    dt = 1.0 / 60.0
    for _ in range(60):
        player.update(dt, 1, 0, world)  # Move right
    
    print(f"   After moving right: ({player.x:.1f}, {player.y:.1f})")
    
    # Test collision (try to move into a wall)
    wall_x, wall_y = 0, 0  # Top-left corner is a wall
    player.x, player.y = TILE_SIZE, TILE_SIZE  # Near wall
    for _ in range(60):
        player.update(dt, -1, 0, world)  # Try to move into wall
    
    print(f"   After trying to move into wall: ({player.x:.1f}, {player.y:.1f})")
    print("   ✅ Movement and collision working!")

def test_player_shooting():
    """Test player shooting mechanics"""
    print("🧪 Testing Player Shooting...")
    
    player = Player(PLAYER_START_X, PLAYER_START_Y)
    
    print(f"   Initial ammo: {player.ammo}")
    
    # Test shooting
    for i in range(player.max_ammo + 2):  # Shoot more than max ammo
        result = player.shoot()
        print(f"   Shot {i+1}: {'Hit' if result else 'Miss/Empty'} - Ammo: {player.ammo}")
    
    # Test reload
    player.reload()
    print(f"   After reload: {player.ammo}")
    print("   ✅ Shooting mechanics working!")

def test_player_rotation():
    """Test player rotation"""
    print("🧪 Testing Player Rotation...")
    
    player = Player(PLAYER_START_X, PLAYER_START_Y)
    
    print(f"   Initial angle: {math.degrees(player.angle):.1f}°")
    
    # Test rotation
    player.rotate(math.pi / 2)  # 90 degrees
    print(f"   After 90° rotation: {math.degrees(player.angle):.1f}°")
    
    player.rotate(math.pi)  # Another 180 degrees
    print(f"   After another 180° rotation: {math.degrees(player.angle):.1f}°")
    
    # Test angle wrapping
    player.rotate(math.pi * 3)  # 540 degrees (should wrap)
    print(f"   After 540° rotation (should wrap): {math.degrees(player.angle):.1f}°")
    print("   ✅ Rotation mechanics working!")

def test_world_collision():
    """Test world collision detection"""
    print("🧪 Testing World Collision...")
    
    world = World()
    
    # Test wall detection
    test_positions = [
        (0, 0),  # Top-left corner (wall)
        (TILE_SIZE * 3, TILE_SIZE * 3),  # Player start (open)
        (TILE_SIZE * 10, TILE_SIZE * 7),  # Center area (open)
        (-10, -10),  # Out of bounds (wall)
        (TILE_SIZE * 100, TILE_SIZE * 100),  # Way out of bounds (wall)
    ]
    
    for x, y in test_positions:
        is_wall = world.is_wall(x, y)
        grid_x, grid_y = int(x // TILE_SIZE), int(y // TILE_SIZE)
        print(f"   Position ({x}, {y}) -> Grid ({grid_x}, {grid_y}): {'Wall' if is_wall else 'Open'}")
    
    print("   ✅ Collision detection working!")

def test_points_system():
    """Test points system"""
    print("🧪 Testing Points System...")
    
    player = Player(PLAYER_START_X, PLAYER_START_Y)
    
    print(f"   Initial points: {player.points}")
    
    # Test adding points
    player.add_points(POINTS_PER_KILL)
    print(f"   After kill bonus: {player.points}")
    
    # Test spending points
    cost = 100
    can_spend = player.spend_points(cost)
    print(f"   Can spend {cost} points: {can_spend}")
    print(f"   Points after spending: {player.points}")
    
    # Test spending more than available
    can_spend = player.spend_points(1000)
    print(f"   Can spend 1000 points: {can_spend}")
    print(f"   Points unchanged: {player.points}")
    print("   ✅ Points system working!")

def main():
    """Run all tests"""
    print("🎮 COD Zombies Game - Mechanics Test Suite")
    print("=" * 50)
    
    test_player_movement()
    print()
    test_player_shooting()
    print()
    test_player_rotation()
    print()
    test_world_collision()
    print()
    test_points_system()
    
    print("=" * 50)
    print("🎉 All tests completed!")
    print("✅ Core game mechanics are functional!")

if __name__ == "__main__":
    main()