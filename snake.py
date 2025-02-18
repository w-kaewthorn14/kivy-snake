import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        
        self.snake = [(10, 10)]  # snake head + body
        self.snake_direction = (1, 0)  # Initial direction (right)
        self.food = (random.randint(0, 19), random.randint(0, 19))  # Random food position
        self.score = 0
        self.snake_size = 20  # Size of the snake and food block
        
        self.update_label = Label(text="Score: 0", pos=(10, Window.height - 30))
        self.add_widget(self.update_label)
        
        # Load sound effects
        self.eat_sound = SoundLoader.load('eat_sound.mp3')  # Assuming you have an eat_sound.mp3 file
        self.game_over_sound = SoundLoader.load('game_over.mp3')  # Assuming you have a game_over.mp3 file

        Clock.schedule_interval(self.update, 0.1)  # Update the game every 0.1 second
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, instance, key, *args):
        if key == 273:  # Up arrow
            if self.snake_direction != (0, -1):
                self.snake_direction = (0, 1)
        elif key == 274:  # Down arrow
            if self.snake_direction != (0, 1):
                self.snake_direction = (0, -1)
        elif key == 275:  # Right arrow
            if self.snake_direction != (-1, 0):
                self.snake_direction = (1, 0)
        elif key == 276:  # Left arrow
            if self.snake_direction != (1, 0):
                self.snake_direction = (-1, 0)

    def update(self, dt):
        new_head = (self.snake[0][0] + self.snake_direction[0], self.snake[0][1] + self.snake_direction[1])
        
        # Check if snake hits the wall or itself
        if (new_head[0] < 0 or new_head[0] >= Window.width // self.snake_size or
            new_head[1] < 0 or new_head[1] >= Window.height // self.snake_size or
            new_head in self.snake):
            self.game_over_sound.play()  # Play game over sound
            self.reset_game()  # Reset the game if snake dies
            return
        
        self.snake = [new_head] + self.snake[:-1]  # Move the snake forward
        
        self.canvas.clear()  # Clear previous frame
        
        self.draw_snake()  # Draw the snake
        self.draw_food()   # Draw the food
        
        # Check if snake eats the food
        if new_head == self.food:
            self.snake.append(self.snake[-1])  # Add new segment to snake
            self.score += 1
            self.update_label.text = f"Score: {self.score}"
            self.eat_sound.play()  # Play eat food sound
            self.food = self.generate_food()  # Generate new food position

    def generate_food(self):
        """Generate new food position that does not overlap with the snake"""
        while True:
            food = (random.randint(0, 19), random.randint(0, 19))
            if food not in self.snake:
                return food

    def reset_game(self):
        """Reset the game when the snake dies"""
        self.snake = [(10, 10)]  # Reset snake position
        self.snake_direction = (1, 0)  # Reset direction to right
        self.food = self.generate_food()  # New random food
        self.score = 0
        self.update_label.text = "Score: 0"  # Reset score
        self.canvas.clear()  # Clear the canvas

    def draw_snake(self):
        """Draw the snake"""
        with self.canvas:
            Color(0, 1, 0)  # Snake color is green
            for x, y in self.snake:
                Rectangle(pos=(x * self.snake_size, y * self.snake_size),
                          size=(self.snake_size, self.snake_size))

    def draw_food(self):
        """Draw the food"""
        with self.canvas:
            Color(1, 0, 0)  # Food color is red
            x, y = self.food
            Rectangle(pos=(x * self.snake_size, y * self.snake_size),
                      size=(self.snake_size, self.snake_size))

class SnakeApp(App):
    def build(self):
        return SnakeGame()

if __name__ == '__main__':
    SnakeApp().run()
