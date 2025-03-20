import pygame  # Import Pygame for rendering graphics
import random  # Import random to generate different pipe heights
from src.config import WIDTH, HEIGHT, PIPE_SPEED, PIPE_GAP, PIPE_WIDTH  # Import game configuration constants

class Pipe:
    """Represents a pair of pipes in the Flappy Bird game."""

    def __init__(self, x):
        """Initializes a pipe pair at a given x position."""
        
        # Load pipe images (top and bottom)
        self.image_top = pygame.image.load("assets/pipe_top.png")
        self.image_bottom = pygame.image.load("assets/pipe_bottom.png")

        # Generate a random height for the top pipe (between 100 and 300 pixels)
        top_pipe_height = random.randint(100, 300)

        # Scale pipe images to fit their positions dynamically
        self.image_top = pygame.transform.scale(self.image_top, (PIPE_WIDTH, top_pipe_height))
        self.image_bottom = pygame.transform.scale(
            self.image_bottom, 
            (PIPE_WIDTH, HEIGHT - top_pipe_height - PIPE_GAP)  # Adjust bottom pipe height
        )

        # Position the pipes:
        # - The top pipe's bottom aligns with its randomized height
        # - The bottom pipe's top starts after a fixed gap from the top pipe
        self.rect_top = self.image_top.get_rect(midbottom=(x, top_pipe_height))
        self.rect_bottom = self.image_bottom.get_rect(midtop=(x, top_pipe_height + PIPE_GAP))

    def move(self):
        """Moves the pipes leftward at a constant speed."""
        self.rect_top.x -= PIPE_SPEED  # Move top pipe to the left
        self.rect_bottom.x -= PIPE_SPEED  # Move bottom pipe to the left

    def draw(self, screen):
        """Draws the pipes on the screen."""
        screen.blit(self.image_top, self.rect_top)  # Draw top pipe
        screen.blit(self.image_bottom, self.rect_bottom)  # Draw bottom pipe

    def is_off_screen(self):
        """Checks if the pipes have completely moved off the screen."""
        return self.rect_top.right < 0  # Return True if pipe has exited the left boundary
