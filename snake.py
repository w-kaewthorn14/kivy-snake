import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=50, size_hint=(None, None))
        layout.size = (300, 200)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        start_button = Button(text='Start Game', font_size=24, size_hint=(None, None), size=(200, 50))
        exit_button = Button(text='Exit', font_size=24, size_hint=(None, None), size=(200, 50))
        
        start_button.bind(on_release=self.start_game)
        exit_button.bind(on_release=self.exit_game)
        
        layout.add_widget(start_button)
        layout.add_widget(exit_button)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.manager.current = 'game'
    
    def exit_game(self, instance):
        App.get_running_app().stop()

class SnakeGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = Widget()
        self.add_widget(self.game_widget)
        
        self.snake = [(10, 10)]
        self.snake_direction = (1, 0)
        self.food = (random.randint(0, 19), random.randint(0, 19))
        self.score = 0
        self.best_score = 0  # Best score tracking
        self.snake_size = 20
        self.paused = False
        
        self.best_score_label = Label(text="Best: 0", font_size=20,
                                      size_hint=(None, None), size=(100, 40),
                                      pos=(10, Window.height - 30))
        self.update_label = Label(text="Score: 0", font_size=20,
                                  size_hint=(None, None), size=(100, 40),
                                  pos=(10, Window.height - 60))
        
        self.add_widget(self.best_score_label)
        self.add_widget(self.update_label)
        
        self.eat_sound = SoundLoader.load('eat_sound.mp3')
        self.game_over_sound = SoundLoader.load('game_over.mp3')
        
        self.pause_layout = BoxLayout(orientation='vertical', spacing=10, padding=50, size_hint=(None, None))
        self.pause_layout.size = (300, 200)
        self.pause_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.pause_layout.opacity = 0
        
        resume_button = Button(text='Play Again', font_size=24, size_hint=(None, None), size=(200, 50))
        exit_button = Button(text='Exit', font_size=24, size_hint=(None, None), size=(200, 50))
        
        resume_button.bind(on_release=self.reset_game)
        exit_button.bind(on_release=lambda x: App.get_running_app().stop())
        
        self.pause_layout.add_widget(resume_button)
        self.pause_layout.add_widget(exit_button)
        self.add_widget(self.pause_layout)
        
        self.update_event = Clock.schedule_interval(self.update, 0.1)
        Window.bind(on_key_down=self.on_key_down)
    
    def on_key_down(self, instance, key, *args):
        if not self.paused:
            if key == 273 and self.snake_direction != (0, -1):
                self.snake_direction = (0, 1)
            elif key == 274 and self.snake_direction != (0, 1):
                self.snake_direction = (0, -1)
            elif key == 275 and self.snake_direction != (-1, 0):
                self.snake_direction = (1, 0)
            elif key == 276 and self.snake_direction != (1, 0):
                self.snake_direction = (-1, 0)
    
    def update(self, dt):
        if self.paused:
            return
        
        new_head = (self.snake[0][0] + self.snake_direction[0],
                    self.snake[0][1] + self.snake_direction[1])
        
        if (new_head[0] < 0 or new_head[0] >= Window.width // self.snake_size or
            new_head[1] < 0 or new_head[1] >= Window.height // self.snake_size or
            new_head in self.snake):
            if self.game_over_sound:
                self.game_over_sound.play()
            self.pause_game()
            return
        
        self.snake = [new_head] + self.snake[:-1]
        self.game_widget.canvas.clear()
        self.draw_snake()
        self.draw_food()
        
        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.score += 1
            self.update_label.text = f"Score: {self.score}"
            if self.score > self.best_score:
                self.best_score = self.score
                self.best_score_label.text = f"Best score: {self.best_score}"
            if self.eat_sound:
                self.eat_sound.play()
            self.food = self.generate_food()
    
    def generate_food(self):
        while True:
            food = (random.randint(0, 19), random.randint(0, 19))
            if food not in self.snake:
                return food
    
    def pause_game(self):
        self.paused = True
        self.pause_layout.opacity = 1
        Clock.unschedule(self.update)
    
    def reset_game(self, instance):
        self.snake = [(10, 10)]
        self.snake_direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.update_label.text = "Score: 0"
        self.game_widget.canvas.clear()
        self.paused = False
        self.pause_layout.opacity = 0
        self.update_event = Clock.schedule_interval(self.update, 0.1)
    
    def draw_snake(self):
        with self.game_widget.canvas:
            Color(0, 1, 0)
            for x, y in self.snake:
                Rectangle(pos=(x * self.snake_size, y * self.snake_size),
                          size=(self.snake_size, self.snake_size))
    
    def draw_food(self):
        with self.game_widget.canvas:
            Color(1, 0, 0)
            x, y = self.food
            Rectangle(pos=(x * self.snake_size, y * self.snake_size),
                      size=(self.snake_size, self.snake_size))

class SnakeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SnakeGame(name='game'))
        return sm

if __name__ == '__main__':
    SnakeApp().run()
