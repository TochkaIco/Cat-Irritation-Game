import pytest
import pygame
import Classes
import CatGame_BasicLogics as Log
from AssetManager import AssetManager

# Initialize pygame for some of the classes to work
pygame.init()
# Set up a dummy screen for convert/convert_alpha to work if needed
pygame.display.set_mode((1, 1), pygame.HIDDEN)

def test_player_health():
    # Mocking surface for player
    dummy_surface = pygame.Surface((32, 32))
    player = Classes.Player(0, 0, 0, dummy_surface)
    
    initial_health = player.Health
    assert initial_health == 100
    
    # Create an attacker
    attacker = Classes.Slime(10, 10, 0, dummy_surface)
    attacker.Damage = 20
    
    # Test Damage function
    Log.Damage(player, attacker)
    
    assert player.Health == 80
    assert len(attacker.IFrame_Trackers) == 1

def test_iframe_tracker():
    dummy_surface = pygame.Surface((32, 32))
    player = Classes.Player(0, 0, 0, dummy_surface)
    attacker = Classes.Slime(10, 10, 0, dummy_surface)
    attacker.Damage = 20
    
    # Apply damage
    Log.Damage(player, attacker)
    
    # Damage again immediately - should be blocked by i-frames
    Log.Damage(player, attacker)
    assert player.Health == 80
    
    # Advance time manually in trackers
    tracker = attacker.IFrame_Trackers[0]
    # Set DeltaTime for Log
    Log.DeltaTime = 1.0 # 1 second delta
    
    tracker.Update_time()
    
    # Now damage should work again as player.I_frames = 0.7
    # Note: the tracker might have been removed, let's check
    assert len(attacker.IFrame_Trackers) == 0
    
    Log.Damage(player, attacker)
    assert player.Health == 60

def test_obb_collision():
    dummy_surface = pygame.Surface((100, 100))
    # Create two rectangles that should collide
    obj1 = Classes.Default_Object(0, 0, 0, dummy_surface, 100, 100, 0, 0, 0, "test", False)
    obj2 = Classes.Default_Object(50, 50, 0, dummy_surface, 100, 100, 0, 0, 0, "test", False)
    
    # Check simple rect collision first
    assert obj1.Hitbox.colliderect(obj2.Hitbox)
    
    # Check OBB collision
    collided = Log.CheckObbCollisions(obj1, obj2)
    assert collided == True
    
    # Move obj2 away
    obj2.x = 400
    obj2.y = 400
    obj2.Update_Hitbox()
    
    print(f"Obj1 points: {obj1.Points}")
    print(f"Obj2 points: {obj2.Points}")
    print(f"Obj1 rect: {obj1.Hitbox}")
    print(f"Obj2 rect: {obj2.Hitbox}")
    
    collided = Log.CheckObbCollisions(obj1, obj2)
    assert collided == False
