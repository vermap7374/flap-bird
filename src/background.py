import pygame  # Import the Pygame library for graphics rendering
from src.config import WIDTH, HEIGHT  # Import screen width and height from config

class Background:
    def __init__(self):
        """Initialize the background images for smooth scrolling effect."""
        
        # Load the background image and optimize it using convert()
        self.image = pygame.image.load("assets/background.webp").convert()

        # Scale the background image to match the screen size
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        # Create two background images side-by-side to create a scrolling effect
        self.rect1 = self.image.get_rect(topleft=(0, 0))      # First background starts at (0,0)
        self.rect2 = self.image.get_rect(topleft=(WIDTH, 0))  # Second background starts right after the first

    def move(self, speed=2):
        """Moves the background images leftwards to create a continuous scrolling effect."""

        # Move both background images to the left by the specified speed
        self.rect1.x -= speed
        self.rect2.x -= speed

        # If the first background moves completely off-screen, reposition it to the right of the second background
        if self.rect1.right <= 0:
            self.rect1.x = self.rect2.right

        # If the second background moves completely off-screen, reposition it to the right of the first background
        if self.rect2.right <= 0:
            self.rect2.x = self.rect1.right

    def draw(self, screen):
        """Draws the scrolling background images on the screen."""
        
        # Draw both background images on the screen
        screen.blit(self.image, self.rect1)
        screen.blit(self.image, self.rect2)
