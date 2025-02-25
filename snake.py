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
from kivy.animation import Animation
from kivy.uix.image import Image

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=50, size_hint=(None, None))
        layout.size = (300, 200)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        start_button = Button(text='Start Game', font_size=24, size_hint=(None, None), size=(200, 50))
        level_button = Button(text='Setting', font_size=24, size_hint=(None, None), size=(200, 50))
        exit_button = Button(text='Exit', font_size=24, size_hint=(None, None), size=(200, 50))
        
        start_button.bind(on_release=self.start_game)
        level_button.bind(on_release=self.select_level)
        exit_button.bind(on_release=self.exit_game)
        
        layout.add_widget(start_button)
        layout.add_widget(level_button)
        layout.add_widget(exit_button)
        
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'game'
    
    def select_level(self, instance):
        self.manager.current = 'level_selection'
    
    def exit_game(self, instance):
        App.get_running_app().stop()

class LevelSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=50, size_hint=(None, None))
        layout.size = (300, 200)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        easy_button = Button(text='Easy', font_size=24, size_hint=(None, None), size=(200, 50))
        medium_button = Button(text='Medium', font_size=24, size_hint=(None, None), size=(200, 50))
        hard_button = Button(text='Hard', font_size=24, size_hint=(None, None), size=(200, 50))
        back_button = Button(text='Back to Menu', font_size=24, size_hint=(None, None), size=(200, 50))
        
        easy_button.bind(on_release=lambda x: self.start_game('easy'))
        medium_button.bind(on_release=lambda x: self.start_game('medium'))
        hard_button.bind(on_release=lambda x: self.start_game('hard'))
        back_button.bind(on_release=self.go_to_menu)
        
        layout.add_widget(easy_button)
        layout.add_widget(medium_button)
        layout.add_widget(hard_button)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def start_game(self, difficulty):
        self.manager.current = 'game'
        game_screen = self.manager.get_screen('game')
    
    def go_to_menu(self, instance):
        self.manager.current = 'menu'

class SnakeGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = Widget()
        self.add_widget(self.game_widget)
        
        self.snake = [(10, 10)]
        self.snake_direction = (1, 0)
        self.food = (random.randint(0, 19), random.randint(0, 19))
        self.score = 0
        self.best_score = 0
        self.snake_size = 20
        self.paused = False
        self.level = 1
        self.speed = 0.1
        
        self.best_score_label = Label(text="Best: 0", font_size=20,
                                      size_hint=(None, None), size=(100, 40),
                                      pos=(10, Window.height - 30))
        self.update_label = Label(text="Score: 0", font_size=20,
                                  size_hint=(None, None), size=(100, 40),
                                  pos=(10, Window.height - 60))
        
        self.timer = 0
        self.timer_label = Label(text="Time: 0", font_size=20,
                                 size_hint=(None, None), size=(100, 40),
                                 pos=(Window.width - 110, Window.height - 30))
        
        self.level_label = Label(text="Level: 1", font_size=20,
                                 size_hint=(None, None), size=(100, 40),
                                 pos=(Window.width - 110, Window.height - 60))
        
        self.add_widget(self.best_score_label)
        self.add_widget(self.update_label)
        self.add_widget(self.timer_label)
        self.add_widget(self.level_label)
        
        self.eat_sound = SoundLoader.load('assets/eat_sound.mp3')
        self.game_over_sound = SoundLoader.load('assets/game_over.mp3')
        self.up_sound = SoundLoader.load('assets/up.mp3')
        self.right_sound = SoundLoader.load('assets/right.mp3')
        self.down_sound = SoundLoader.load('assets/down.mp3')
        self.left_sound = SoundLoader.load('assets/left.mp3')

        self.pause_layout = BoxLayout(orientation='vertical', spacing=10, padding=50, size_hint=(None, None))
        self.pause_layout.size = (300, 200)
        self.pause_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.pause_layout.opacity = 0
        
        resume_button = Button(text='Play Again', font_size=24, size_hint=(None, None), size=(200, 50))
        menu_button = Button(text='Go to Menu', font_size=24, size_hint=(None, None), size=(200, 50))
        
        resume_button.bind(on_release=self.reset_game)
        menu_button.bind(on_release=self.go_to_menu)
        
        self.pause_layout.add_widget(resume_button)
        self.pause_layout.add_widget(menu_button)
        self.add_widget(self.pause_layout)
        
        self.update_event = Clock.schedule_interval(self.update, self.speed)
        Window.bind(on_key_down=self.on_key_down)
    
    def update(self, dt):
        if self.paused:
            return
        
        self.timer += 1
        self.timer_label.text = f"Time: {self.timer // 10}"
        
        new_head = (self.snake[0][0] + self.snake_direction[0],
                    self.snake[0][1] + self.snake_direction[1])
        
        if (new_head[0] < 0 or new_head[0] >= Window.width // self.snake_size or
            new_head[1] < 0 or new_head[1] >= Window.height // self.snake_size or
            new_head in self.snake):
            if self.game_over_sound:
                self.game_over_sound.play()
            self.game_over_screen()
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
            
            # Increase level every 5 points
            if self.score % 5 == 0:
                self.level += 1
                self.level_label.text = f"Level: {self.level}"
                self.speed -= 0.01  # Increase speed
                Clock.unschedule(self.update)
                self.update_event = Clock.schedule_interval(self.update, self.speed)
        
    def game_over_screen(self):
        self.paused = True
        self.pause_layout.opacity = 1
        Clock.unschedule(self.update)
        
        # Create "Game Over" label and animate it
        game_over_label = Label(text="GAME OVER", font_size=50, color=(1, 0, 0, 1),
                                size_hint=(None, None), size=(300, 100),
                                pos=(Window.width / 2 - 150, Window.height / 2+65))
        
        self.add_widget(game_over_label)
        
        # Animation to make the text scale up
        anim = Animation(font_size=80, duration=1.5) + Animation(font_size=50, duration=1.5)
        anim.start(game_over_label)
    
    def reset_game(self, instance):
        self.snake = [(10, 10)]
        self.snake_direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.level = 1
        self.update_label.text = "Score: 0"
        self.level_label.text = "Level: 1"
        self.game_widget.canvas.clear()
        self.paused = False
        self.pause_layout.opacity = 0
        self.timer = 0
        self.timer_label.text = "Time: 0"
        self.update_event = Clock.schedule_interval(self.update, self.speed)
        
        # ลบ "GAME OVER" label ถ้ามี
        for widget in self.children:
            if isinstance(widget, Label) and widget.text == "GAME OVER":
                self.remove_widget(widget)

    def go_to_menu(self, instance):
        self.manager.current = 'menu'
    
    def draw_snake(self):
        self.game_widget.canvas.clear()  # เคลียร์ Canvas ก่อนวาดใหม่
        with self.game_widget.canvas:
            try:
                # โหลด texture หัวงู
                head_texture = Image(source="assets/snake_head.png").texture
                x, y = self.snake[0]
                Rectangle(texture=head_texture, pos=(x * self.snake_size, y * self.snake_size),
                          size=(self.snake_size, self.snake_size))

                # โหลด texture ตัวงู
                body_texture = Image(source="assets/snake_body.png").texture
                for x, y in self.snake[1:]:
                    Rectangle(texture=body_texture, pos=(x * self.snake_size, y * self.snake_size),
                              size=(self.snake_size, self.snake_size))

            except Exception as e:
                print(f"Error loading snake texture: {e}")  # แสดงข้อผิดพลาดถ้ามีปัญหา

    def draw_food(self):
        with self.game_widget.canvas:
            Color(1, 0, 0)
            x, y = self.food
            Rectangle(pos=(x * self.snake_size, y * self.snake_size),
                      size=(self.snake_size, self.snake_size))

    def on_key_down(self, instance, key, *args):
        if key == 112:  # 112 คือรหัสของปุ่ม P
            self.paused = not self.paused
        if not self.paused:
            if key == 273 and self.snake_direction != (0, -1):
                self.snake_direction = (0, 1)
                self.up_sound.play()
            elif key == 274 and self.snake_direction != (0, 1):
                self.snake_direction = (0, -1)
                self.down_sound.play()
            elif key == 275 and self.snake_direction != (-1, 0):
                self.snake_direction = (1, 0)
                self.right_sound.play()
            elif key == 276 and self.snake_direction != (1, 0):
                self.snake_direction = (-1, 0)
                self.left_sound.play()

    def generate_food(self):
        return (random.randint(0, 19), random.randint(0, 19))

class SnakeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LevelSelectionScreen(name='level_selection'))
        sm.add_widget(SnakeGame(name='game'))
        return sm

if __name__ == '__main__':
    SnakeApp().run()