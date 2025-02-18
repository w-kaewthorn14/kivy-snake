import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        
        self.snake = [(10, 10), (9, 10), (8, 10)]  # snake head + body
        self.snake_direction = (1, 0)  # Initial direction (right)
        self.apple = (random.randint(0, 19), random.randint(0, 19))  # Random apple position
        self.score = 0
        
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
        self.snake = [new_head] + self.snake[:-1]  # Move the snake forward
        
        self.canvas.clear()  # Clear previous frame
        self.snake_color = Color(0, 1, 0)  # Set snake color to green
        for segment in self.snake:
            x, y = segment
            with self.canvas:
                Rectangle(pos=(x * 20, y * 20), size=(20, 20))

        # Draw the apple
        self.apple_color = Color(1, 0, 0)  # Set apple color to red
        x, y = self.apple
        with self.canvas:
            Rectangle(pos=(x * 20, y * 20), size=(20, 20))

class SnakeApp(App):
    def build(self):
        return SnakeGame()

if __name__ == '__main__':
    SnakeApp().run()
