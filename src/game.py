import pygame
import json
from src.bird import Bird
from src.pipe import Pipe
from src.background import Background
from src.config import WIDTH, HEIGHT, PIPE_GAP

class Game:
    """Main class for managing the Flappy Bird game."""

    def __init__(self):
        """Initialize the game settings, objects, and variables."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create game window
        self.clock = pygame.time.Clock()  # Initialize clock for frame rate control
        self.running = True  # Game loop condition
        self.background = Background()  # Load background
        self.bird = Bird()  # Create Bird instance
        self.pipes = [Pipe(WIDTH + 100)]  # Create initial pipe
        self.font = pygame.font.Font(None, 50)  # Set font for text display

        # Score tracking
        self.score = 0
        self.highscore = self.load_highscore()  # Load the highest score

        # Show the start screen before the game begins
        self.show_start_screen()

    def show_start_screen(self):
        """Displays the start screen and waits for the player to press a key."""
        start_font = pygame.font.Font(None, 50)
        instruction_font = pygame.font.Font(None, 35)

        # Render text
        title_text = start_font.render("Flappy Bird", True, (255, 255, 0))
        instruction_text = instruction_font.render("Press Any Key to Start", True, (0, 255, 0))

        # Get text rectangles and center them
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Display the start screen
        while True:
            self.background.draw(self.screen)  # Show background
            self.screen.blit(title_text, title_rect)  # Draw title
            self.screen.blit(instruction_text, instruction_rect)  # Draw instructions
            pygame.display.flip()  # Update the screen

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()  # Exit if the player closes the game
                if event.type == pygame.KEYDOWN:
                    return  # Exit loop when any key is pressed

    def load_highscore(self):
        """Loads the highest score from a file or initializes it if not found."""
        try:
            with open("highscore.json", "r") as file:
                return json.load(file)["highscore"]
        except FileNotFoundError:
            return 0  # If file not found, set highscore to 0

    def save_highscore(self):
        """Saves the highest score to a file."""
        with open("highscore.json", "w") as file:
            json.dump({"highscore": self.highscore}, file)

    def handle_events(self):
        """Handles user input events (key presses and quitting)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Exit game loop if quit event is detected
            if event.type == pygame.KEYDOWN:
                self.bird.jump()  # Make the bird jump on any key press

    def update(self):
        """Updates the game state including bird movement, pipes, and collision detection."""
        self.bird.update()  # Apply gravity and update bird position
        for pipe in self.pipes:
            pipe.move()  # Move pipes to the left

        # Spawn new pipes when the last pipe reaches the middle of the screen
        if self.pipes[-1].rect_top.x < WIDTH // 2:
            self.pipes.append(Pipe(WIDTH + 100))

        # Remove pipes that have moved off the screen
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

        # Collision detection
        if self.bird.rect.top <= 0 or self.bird.rect.bottom >= HEIGHT:
            self.game_over()  # End the game if bird hits the top or bottom
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect_top) or self.bird.rect.colliderect(pipe.rect_bottom):
                self.game_over()  # End the game if bird collides with a pipe

        # Update score when passing a pipe
        for pipe in self.pipes:
            if pipe.rect_top.right < self.bird.rect.left and not hasattr(pipe, 'passed'):
                self.score += 1
                pipe.passed = True  # Mark pipe as passed to avoid multiple counts

        # Update high score if the current score is greater
        if self.score > self.highscore:
            self.highscore = self.score

    def draw(self):
        """Draws all game elements on the screen."""
        self.background.draw(self.screen)  # Draw background
        self.bird.draw(self.screen)  # Draw bird
        for pipe in self.pipes:
            pipe.draw(self.screen)  # Draw pipes

        # Display current score and high score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        highscore_text = self.font.render(f"High Score: {self.highscore}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))  # Draw score on screen
        self.screen.blit(highscore_text, (10, 40))  # Draw high score on screen

        pygame.display.flip()  # Update screen with new visuals

    def game_over(self):
        """Handles the game over screen and restart logic."""
        self.save_highscore()  # Save the high score before restarting
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Create semi-transparent overlay for effect

        fade_alpha = 0
        while fade_alpha < 150:
            overlay.set_alpha(fade_alpha)
            self.background.draw(self.screen)  # Keep background visible
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            fade_alpha += 5
            pygame.time.delay(30)

        # Fonts for game over screen
        font_big = pygame.font.Font(None, 60)
        font_small = pygame.font.Font(None, 40)

        # Render text
        game_over_text = font_big.render("GAME OVER", True, (255, 0, 0))
        score_text = font_small.render(f"Score: {self.score}", True, (255, 255, 255))
        highscore_text = font_small.render(f"High Score: {self.highscore}", True, (255, 255, 255))
        restart_text = font_small.render("Press Any Key to Restart", True, (0, 255, 0))

        # Center text on screen
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3)))
        self.screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
        self.screen.blit(highscore_text, highscore_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60)))

        pygame.display.flip()  # Refresh screen
        self.wait_for_restart()

    def wait_for_restart(self):
        """Waits for any key press to restart the game."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()  # Exit the game if the user closes the window
                if event.type == pygame.KEYDOWN:
                    self.__init__()  # Reset the game state
                    self.run()  # Restart the game loop

    def run(self):
        """Runs the game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    Game().run()
