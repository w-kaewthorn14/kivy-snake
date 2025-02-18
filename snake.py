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

        Clock.schedule_interval(self.update, 0.1)  # Update the game every 0.1 second

    def update(self, dt):
        new_head = (self.snake[0][0] + self.snake_direction[0], self.snake[0][1] + self.snake_direction[1])
        self.snake = [new_head] + self.snake[:-1]  # Move the snake forward

class SnakeApp(App):
    def build(self):
        return SnakeGame()

if __name__ == '__main__':
    SnakeApp().run()
