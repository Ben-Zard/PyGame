# //*******************************************************************
# In this project i used the library called PyGame to mimic the game breakout.
# In this project there will be classes like Game that sets up the environment
# also Overlay that will display the score and number of lives. There will be a Paddle
# that the player controls to break the blocks and will hold information like size and movement speed.
# the ball will be a circle and will bounce off the paddle and walls to deal damage 25. The brick will
# be a random color and based on this color it will determine its health. In my project i used
# https://realpython.com/pygame-a-primer/. This helped me to understand the basics of what pygame offers
# and how to create a basic function of game logic. This website also helped when using update methods to
# be able to keep game logic smooth.
# https://coderslegacy.com/python/python-pygame-tutorial/. This website was used to help me create my shapes.
# It helped me to be able to create the bricks and using the random library assign a color to them. It also helped
# with creating a paddle and allowing for player input from a console be abel to control the movement of the paddle.
# I was also able to use this to create the basic ball and be able to make it bounce and move on the screen.
#
# @author Ben Zardus
# @version CIS 343 Winter 2022
# *****************************************************************//

# Required libraries
import random
import pygame.sprite

# /*****************************************************************
############### SETTINGS ####################
# I am creating the intial settings of the game. This is where
# i define my number of lives, and the game functions that determine
# the interaction with in the game. I also Calculate brick and paddle
# size according to the screen size and number of bricks
# *****************************************************************/
window_title = "My Brick Breaker Game"
number_of_lives = 3
screen_width = 500
screen_height = 500
number_of_bricks = [5, 8]  # rows and columns
paddle_speed = 5
hidden_key = pygame.K_s
font_size = 80
font_name = "Arial"

brick_size = [screen_width / number_of_bricks[1],
              screen_height / 2 / number_of_bricks[1]]
paddle_size = [screen_height // 4, screen_height // 30]

# /*****************************************************************
# Set the image of the paddle as a black rectangle
# Set the position of the paddle
# Paddle initial speed of 0
#     @param type_size number of bytes for a single element of the type
#                      to be stored in the vector.
#     @return the vector, or null if fails
# *****************************************************************/
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Set the image of the paddle as a black rectangle
        self.image = pygame.Surface(paddle_size)
        self.image.fill((0, 0, 0))
        # Set the position of the paddle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Paddle initial speed of 0
        self.speed = 0

    # /*****************************************************************
    # Change speed according to the pressed key (Right or left arrow)
    # Update paddles horizontal position according to its current speed
    # If the paddle position is out of the screen, then it gets fixed to that border
    #     @param self instance of paddle class
    # *****************************************************************/
    def update(self):
        # (Right or left arrow)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.speed = -paddle_speed
        if pressed_keys[pygame.K_RIGHT]:
            self.speed = paddle_speed
        #horizontal position
        self.rect.x += self.speed
        # position fixed to that border
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
        if self.rect.left <= 0:
            self.rect.left = 0

# /*****************************************************************
#     Sets up the environment of the game. This involves creating all of
#     the balls, bricks, paddle, and contains the game loop.
# *****************************************************************/
class Game:
    # /*****************************************************************
    #     special method to start pygame module and set the window title and size
    #     also takes varaibles created eairler for the game playability
    #     @param self instance of Game
    # *****************************************************************/
    def __init__(self):
        # Start pygame module
        pygame.init()
        # Set window title and size
        pygame.display.set_caption(window_title)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        # Set initial variables
        self.score = 0
        self.lives = number_of_lives
        # Pygame clock for each cycle
        self.clock = pygame.time.Clock()
        # Game objects
        self.elements = self.bricks = self.balls = self.paddle = self.overlay = None
        # Set initial state of the game with the paddle, ball and bricks
        self.initial_state()

    # /*****************************************************************
    #     sets up the intial playability of the game with the ball
    #     and paddle
    #     @param self instance of Game
    # *****************************************************************/
    def initial_state(self):
        # For new games, the bricks are spawned
        if self.lives == number_of_lives:
            # Variables to store game elements
            self.elements = pygame.sprite.Group()
            self.bricks = pygame.sprite.Group()
            # Create each brick with 2 loops
            for i in range(number_of_bricks[0]):
                for j in range(number_of_bricks[1]):
                    x = j * brick_size[0]
                    y = i * brick_size[1]
                    # Create brick and add it to their corresponding groups
                    brick = Brick(x, y, self)
                    self.bricks.add(brick)
                    self.elements.add(brick)
        # Create sprite group for balls
        self.balls = pygame.sprite.Group()
        # Creates the paddle and ball and adds them to the sprite groups
        self.paddle = Paddle(screen_width // 2 - paddle_size[0] // 2,
                             screen_height - paddle_size[1] - font_size // 2 * 1.3)
        self.ball = Ball(self)
        self.elements.add(self.paddle)
        self.balls.add(self.ball)
        self.elements.add(self.ball)
        # creates overlay object to show score and lives
        self.overlay = Overlay(self)

    # /*****************************************************************
    #     starts the game, it tracks the game cycle and also checks for
    #     what is happening in the game. Also allows for a second ball
    #     and tracks the lives and score of the player based on bricks broken
    #     @param self instance of Game
    # *****************************************************************/
    def start(self):
        second_ball_spawned = False
        # game cycle
        running = True
        while running:
            self.clock.tick(60)
            # checks for events
            for event in pygame.event.get():
                # In case window is closed
                if event.type == pygame.QUIT:
                    running = False
                # Hidden keystroke to spawn second ball once
                if event.type == pygame.KEYDOWN and not second_ball_spawned:
                    if event.key == hidden_key:
                        # Creates second ball and adds it to the sprite groups
                        ball2 = Ball(self)
                        self.balls.add(ball2)
                        self.elements.add(ball2)
                        # Changes flag so no more extra balls are spawned
                        second_ball_spawned = True
            # Update all elements, mainly movement
            self.elements.update()
            # draw elements
            self.screen.fill((255, 255, 255))
            # If a ball gets out of the screen it gets killed
            for ball in self.balls:
                if ball.rect.bottom >= screen_height:
                    ball.kill()
            # If there are no more balls left, one life is lost and the ball and paddle respawned
            if len(self.balls) == 0:
                self.lives -= 1
                self.paddle.kill()
                self.initial_state()
            # If there are no more lives left, the game is over
            if self.lives == 0:
                # Kill all remaining elements
                self.paddle.kill()
                for ball in self.balls:
                    ball.kill()
                self.elements.remove(self.bricks)
                # Draws game over screen
                self.screen.fill((255, 255, 255))
                # Uses overlay class to draw the message of game over and final score
                self.overlay.write_message("Game Over!", (0, 0, 0), font_size, screen_width // 2,
                                           screen_height // 2 - font_size * 1.1)
                self.overlay.write_message(f"Score: {self.score}", (0, 0, 0), font_size, screen_width // 2,
                                           screen_height // 2)
                # Show drawn elements in the screen
                pygame.display.flip()
                # Waits until the user close the window
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
            # If there are no more bricks left, then the user wins
            if len(self.bricks) == 0:
                # Remove remaining elements
                self.paddle.kill()
                for ball in self.balls:
                    ball.kill()
                # Draws win screen and waits for the user to close the window
                self.screen.fill((255, 255, 255))
                self.overlay.write_message("You Won!", (0, 0, 0), font_size, font_size, screen_width // 2)
                pygame.display.flip()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
            # Draw elements
            self.elements.draw(self.screen)
            # Draw the overlay object, with the score and lives
            self.overlay.draw()
            # Shows drawn objects in screen
            pygame.display.flip()


# /*****************************************************************
#     special method to display the current game status on the screen
#     @param self instance of Game
# *****************************************************************/
class Overlay:
    def __init__(self, game):
        self.game = game

    # /*****************************************************************
    # Draws the current game score and remaining lives on screen
    # to be stored in the vector.
    # @param self instance of Game
    # *****************************************************************/
    def draw(self):
        self.write_message(f"Score: {self.game.score} | Lives: {self.game.lives}", (0, 0, 0), font_size // 2,
                           screen_width // 2, screen_height - font_size // 4 * 1.3)

    # /*****************************************************************
    # Method to draw text on screen
    # *****************************************************************/
    def write_message(self, text, color, size, x, y):
        # Sets text font
        font = pygame.font.SysFont(font_name, size)
        # Renders the string message into an screen element
        message = font.render(text, True, color)
        # Sets text position
        rect = message.get_rect()
        rect.center = x, y
        # Draws message on the game screen
        self.game.screen.blit(message, rect)

# /*****************************************************************
#     create a ball that is used during the game to break blocks
#     its intial size, color and speed are created and applies it
#     to the game logic
# *****************************************************************/
class Ball(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        # Calculates the diameter with the screen dimensions
        diameter = screen_width // 25
        # Creates the circle image
        self.image = pygame.Surface((diameter, diameter))
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, (0, 255, 0), (diameter // 2, diameter // 2), diameter // 2)
        # Set position of the circle
        self.rect = self.image.get_rect()
        self.rect.x = screen_width // 2 - diameter // 2
        self.rect.y = screen_height // 2
        # Initial ball vertical and horizontal speed
        self.y_speed = 3
        self.x_speed = 0
        self.game = game

    # /*****************************************************************
    # Determines if there has been any collision between the ball and the game bricks
    # *****************************************************************/
    def hit_brick(self):
        collisions = pygame.sprite.groupcollide(pygame.sprite.Group(self), self.game.bricks, False, False)
        #If there's any collition, it executes the hit method for each brick and returns True
        if collisions:
            for balls, bricks in collisions.items():
                for brick in bricks:
                    brick.hit()
            return True
        #If there's no collisions, it returns false
        else:
            return False

    # /*****************************************************************
    # Determines if there has been any collision between the ball and the paddle
    # *****************************************************************/

    def hit_paddle(self):
        collisions = pygame.sprite.spritecollide(self.game.paddle, pygame.sprite.Group(self), False)
        if collisions:
            return True
        else:
            return False

    # /*****************************************************************
    #     Helps to track the paddle and the ball and uses the update method to
    #     be able to determine if the speed needs to be adjusted.
    # *****************************************************************/
    def update(self):
        #In each update, it determines if the ball has reached a screen border and modifies the speed accordingly
        if self.rect.left <= 0:
            self.x_speed = - self.x_speed
        elif self.rect.top <= 0:
            self.y_speed = - self.y_speed
        elif self.rect.right >= screen_width:
            self.x_speed = - self.x_speed
        #Same thing in case it has hit the paddle or any brick but adds a random x speed to make the game less predictable
        elif self.hit_paddle():
            self.x_speed = random.randrange(-3, 3)
            self.y_speed = - abs(self.y_speed)
        elif self.hit_brick():
            self.x_speed = random.randrange(-3, 3)
            self.y_speed = - self.y_speed
        #Updated the ball position according to the speed
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

# /*****************************************************************
#     create the brick class, this sets the blocks to random colors
#     based on the color it determins the health of that brick.
#     it also sets the placment of the bricks and the borders around them
# *****************************************************************/
class Brick(pygame.sprite.Sprite):
    # /*****************************************************************
    #     special method to be able to create multiple bricks based of
    #     the set values in the init
    # *****************************************************************/
    def __init__(self, x, y, game):
        super().__init__()
        # Sets the brick rectangle with a random color
        self.image = pygame.Surface(brick_size)
        self.color = [random.randint(0, 255) for i in range(3)]
        self.image.fill(self.color)
        # Sets the rectangle of the sprite in the x and y position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Sets the initial health according to the color of the brick
        self.health = 766 - sum(self.color)
        self.game = game

        self.font = self.text_surface = None
        self.hit_sound_effect = pygame.mixer.Sound("hit.wav")

    # /*****************************************************************
    #     the update method modify the bricks as the game is played
    #     this involves changing the health that is displayed and remove
    #     a brick if it is destroyed
    # *****************************************************************/
    def update(self):
        #The update method modifies the text displaying the brick's health so that the user knows the actual remaining health of it
        self.image.fill(self.color)
        self.font = pygame.font.SysFont(font_name, 10)
        self.text_surface = self.font.render(str(self.health), True, (0, 0, 0))
        text_width = self.text_surface.get_width()
        text_height = self.text_surface.get_height()
        self.image.blit(self.text_surface, [brick_size[0] / 2 - text_width / 2, brick_size[1] / 2 - text_height / 2])


    # /*****************************************************************
    #Method to decrease the bricks health in case it has been hit and in case the health reaches 0, it kills it
    # *****************************************************************/
    def hit(self):
        pygame.mixer.Sound.play(self.hit_sound_effect)
        pygame.mixer.music.stop()
        self.health -= 25
        if self.health <= 0:
            self.game.score += 1
            self.kill()

    # /*****************************************************************
    # Draws initial health in the brick
    # *****************************************************************/
    def draw(self):
        font = pygame.font.SysFont(font_name, int(brick_size[1] // 2))
        message = font.render(str(self.health), True, (255, 255, 255))
        rect = message.get_rect()
        rect.center = 0, 0
        self.game.screen.blit(message, rect)

#Creates a new game and starts it
my_game = Game()
my_game.start()
