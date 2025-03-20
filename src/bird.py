import pygame  # Import the Pygame library for game rendering
from src.config import GRAVITY, JUMP_STRENGTH, BIRD_X_POS, HEIGHT  # Import game constants

class Bird:
    def __init__(self):
        """Initialize the bird's properties and starting position."""
        
        # Load the bird image and enable transparency with convert_alpha()
        self.image = pygame.image.load("assets/bird.png").convert_alpha()

        # Scale the bird image to a proper size (width=50, height=35)
        self.image = pygame.transform.scale(self.image, (50, 35))

        # Get the rectangle (hitbox) for positioning, starting at the center of the screen
        self.rect = self.image.get_rect(center=(BIRD_X_POS, HEIGHT // 2))

        # Bird's vertical velocity (used for jumping and gravity effect)
        self.velocity = 0

    def jump(self):
        """Makes the bird jump by applying an upward velocity."""
        self.velocity = JUMP_STRENGTH  # Set velocity to a negative value for an upward jump

    def update(self):
        """Updates the bird's position by applying gravity."""
        self.velocity += GRAVITY  # Increase velocity due to gravity
        self.rect.y += self.velocity  # Move the bird downwards or upwards based on velocity

    def draw(self, screen):
        """Draws the bird on the screen at its current position."""
        screen.blit(self.image, self.rect)  # Render the bird image at its updated position

    def is_colliding(self, pipes):
        """Checks if the bird has collided with pipes or the screen boundaries."""
        
        # Check if the bird has hit the top or bottom of the screen
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            return True  # Collision detected

        # Check if the bird collides with any of the pipes
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect_top) or self.rect.colliderect(pipe.rect_bottom):
                return True  # Collision detected
        
        return False  # No collision detected
