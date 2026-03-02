import pygame
import os

class AssetManager:
    _cache = {}

    @staticmethod
    def get_image(path, alpha=True):
        """Loads and caches an image.
        
        Args:
            path (str): The relative path to the image file.
            alpha (bool): Whether to use convert_alpha() or convert().
            
        Returns:
            pygame.Surface: The loaded image surface.
        """
        if path in AssetManager._cache:
            return AssetManager._cache[path]

        if not os.path.exists(path):
            print(f"Warning: Asset not found at {path}")
            # Return a small magenta surface as a placeholder
            surface = pygame.Surface((32, 32))
            surface.fill((255, 0, 255))
            return surface

        try:
            surface = pygame.image.load(path)
            if alpha:
                surface = surface.convert_alpha()
            else:
                surface = surface.convert()
            AssetManager._cache[path] = surface
            return surface
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            surface = pygame.Surface((32, 32))
            surface.fill((255, 0, 255))
            return surface

    @staticmethod
    def clear_cache():
        AssetManager._cache.clear()
