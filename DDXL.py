import arcade
import random

SPRITE_SCALING = 1
OBSTACLE_SCALING = 0.7

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Better Move Sprite with Keyboard Example"

MOVEMENT_SPEED = 7


class Player(arcade.Sprite):

    def update(self):
        self.center_y += self.change_y

        if self.bottom < 10:
            self.bottom = 10

            # self.center_y = 29
        elif self.top > SCREEN_HEIGHT - 10:
            self.top = SCREEN_HEIGHT - 10
            # self.center_y = 570


# starts on the left
class ObstacleLeft(arcade.Sprite):

    def update(self):

        self.center_x += self.change_x


# starts on the right
class ObstacleRight(arcade.Sprite):

    def update(self):
        self.center_x -= self.change_x


class DDXL(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None
        self.obstacle_list = None

        self.health = None
        self.score = None

        self.shapes_list = None

        self.time_obstacle = 0

        self.new_obstacle_sprite_left = None
        self.new_obstacle_sprite_right = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed

        self.up_pressed = False
        self.down_pressed = False
        self.space_pressed = 0

        self.at_bottom = False
        self.at_top = False

        # Set the background color
        arcade.set_background_color(arcade.color.PURPLE)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.shapes_list = ["C:/Users/yboy2/OneDrive/Desktop/weirdBox.png",
                            "C:/Users/yboy2/OneDrive/Desktop/weirdRectangle.png",
                            "C:/Users/yboy2/OneDrive/Desktop/weirdRectangle2.png"]

        self.health = 3
        self.score = 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("C:/Users/yboy2/OneDrive/Desktop/ball.png", 1.2)
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT - 30

        self.new_obstacle_sprite_left = ObstacleLeft(self.shapes_list[random.randint(0, 2)], 0.1)
        self.new_obstacle_sprite_left.center_y = random.randrange(80, SCREEN_HEIGHT - 80, 20)
        self.new_obstacle_sprite_left.center_x = 15

        self.new_obstacle_sprite_right = ObstacleLeft(self.shapes_list[random.randint(0, 2)], 0.1)
        self.new_obstacle_sprite_right.center_y = random.randrange(80, SCREEN_HEIGHT - 80, 20)
        self.new_obstacle_sprite_right.center_x = SCREEN_WIDTH-15

        self.player_list.append(self.player_sprite)
        self.obstacle_list.append(self.new_obstacle_sprite_left)
        self.obstacle_list.append(self.new_obstacle_sprite_right)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        output = str(self.score)
        arcade.draw_text(output, 300, 200, arcade.color.AMETHYST, 200, 200, 'center', 'Calibri')

        # Draw all the sprites.
        self.player_list.draw()
        self.obstacle_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_y = 1
        self.new_obstacle_sprite_left.change_x = random.randint(4, 8)
        self.new_obstacle_sprite_right.change_x = -random.randint(4, 8)

        if self.space_pressed == 0:
            self.player_sprite.change_y = MOVEMENT_SPEED
        if self.space_pressed == 1:
            self.player_sprite.change_y = -MOVEMENT_SPEED

        if self.player_sprite.bottom < 15:
            self.at_bottom = True
            self.at_top = False
        if self.player_sprite.top > SCREEN_HEIGHT - 15:
            self.at_top = True
            self.at_bottom = False

        if self.time_obstacle % 100 == 0:
            self.new_obstacle_sprite_left = ObstacleLeft(self.shapes_list[random.randint(0, 2)], 0.1)
            self.new_obstacle_sprite_left.center_y = random.randrange(80, SCREEN_HEIGHT-80, 20)
            self.new_obstacle_sprite_left.center_x = 15
            self.obstacle_list.append(self.new_obstacle_sprite_left)

        if (self.time_obstacle + 50) % 100 == 0:
            self.new_obstacle_sprite_right = ObstacleLeft(self.shapes_list[random.randint(0, 2)], 0.1)
            self.new_obstacle_sprite_right.center_y = random.randrange(80, SCREEN_HEIGHT - 80, 20)
            self.new_obstacle_sprite_right.center_x = SCREEN_WIDTH - 15
            self.obstacle_list.append(self.new_obstacle_sprite_right)

        self.time_obstacle += 1

        # Call update to move the sprite
        # If using a physics engine, call update on it instead of the sprite
        # list.
        self.player_list.update()
        self.obstacle_list.update()

        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.obstacle_list)

        for obstacle in hit_list:
            self.health -= 1
            obstacle.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if self.at_bottom or self.at_top:
            if key == arcade.key.SPACE:
                if self.space_pressed == 0:
                    self.space_pressed = 1
                    self.score += 1
                else:
                    self.space_pressed = 0
                    self.score += 1


def main():
    """ Main method """
    window = DDXL(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()