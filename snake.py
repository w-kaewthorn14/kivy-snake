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
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.vector import Vector

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
    snake_head = ListProperty([0, 0])
    food_pos = ListProperty([0, 0])
    snake_body = ListProperty([])
    direction = Vector(0, 0)
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = Widget()
        self.add_widget(self.game_widget)
        
        self.snake_head = [10 * 20, 10 * 20]
        self.snake_body = []
        self.snake_direction = Vector(1, 0)
        self.food_pos = [random.randint(0, 19) * 20, random.randint(0, 19) * 20]
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

        self.move_time = 0
        self.move_duration = 0.15  # ระยะเวลาในการเคลื่อนที่ระหว่างบล็อก
        self.target_head = self.snake_head[:]
        self.start_head = self.snake_head[:]
        self.moving = False
        self.next_direction = Vector(0, 0)  # เพิ่มตัวแปรเก็บทิศทางถัดไป
        
        # เพิ่มตัวแปรสำหรับการเคลื่อนที่ของลำตัว
        self.body_positions = []  # เก็บตำแหน่งจริงของลำตัว
        self.target_body = []    # เก็บตำแหน่งเป้าหมายของลำตัว
        self.start_body = []     # เก็บตำแหน่งเริ่มต้นของลำตัว
    
    def reset_game(self, instance=None):
        self.snake_head = [
            int(Window.width/2),
            int(Window.height/2)
        ]
        self.snake_body = []
        self.body_positions = []
        self.target_body = []
        self.start_body = []
        self.snake_direction = Vector(1, 0)
        self.next_direction = Vector(0, 0)  # รีเซ็ตทิศทางถัดไปด้วย
        self.score = 0
        self.spawn_food()
        self.paused = False
        self.pause_layout.opacity = 0
        self.timer = 0
        self.timer_label.text = "Time: 0"
        self.update_label.text = "Score: 0"
        self.level_label.text = "Level: 1"
        self.best_score_label.text = f"Best: {self.best_score}"
        self.update_event = Clock.schedule_interval(self.update, self.speed)
        
        # ลบ "GAME OVER" label ถ้ามี
        for widget in self.children:
            if isinstance(widget, Label) and widget.text == "GAME OVER":
                self.remove_widget(widget)

    def spawn_food(self):
        # สร้างอาหารในตำแหน่งสุ่ม
        while True:
            x = random.randint(0, (Window.width - self.snake_size) // self.snake_size) * self.snake_size
            y = random.randint(0, (Window.height - self.snake_size) // self.snake_size) * self.snake_size
            self.food_pos = [x, y]
            if self.food_pos not in self.snake_body and self.food_pos != self.snake_head:
                break
    
    def update(self, dt):
        if self.paused:
            return
        
        self.timer += dt
        self.timer_label.text = f"Time: {int(self.timer)}"
        
        if not self.moving:
            if self.next_direction != Vector(0, 0):
                self.snake_direction = self.next_direction
                self.next_direction = Vector(0, 0)
            
            if self.snake_direction != Vector(0, 0):
                self.start_head = self.snake_head[:]
                self.target_head = [
                    self.snake_head[0] + self.snake_direction[0] * self.snake_size,
                    self.snake_head[1] + self.snake_direction[1] * self.snake_size
                ]
                
                # ตรวจสอบการชนขอบ
                if (self.target_head[0] < 0 or self.target_head[0] >= Window.width or
                    self.target_head[1] < 0 or self.target_head[1] >= Window.height):
                    self.game_over_screen()
                    return
                    
                # แก้ไขการตรวจสอบการชนตัวเอง
                for body_pos in self.body_positions:
                    if (abs(self.target_head[0] - body_pos[0]) < self.snake_size and 
                        abs(self.target_head[1] - body_pos[1]) < self.snake_size):
                        self.game_over_screen()
                        return
                    
                # เก็บตำแหน่งเริ่มต้นและเป้าหมายของลำตัว
                self.start_body = self.body_positions[:] if self.body_positions else []
                self.target_body = [self.start_head]
                if self.start_body:
                    self.target_body.extend(self.start_body[:-1])
                
                self.moving = True
                self.move_time = 0
                
        if self.moving:
            self.move_time += dt
            progress = min(1, self.move_time / self.move_duration)
            
            # อัพเดทตำแหน่งหัว
            self.snake_head = [
                self.start_head[0] + (self.target_head[0] - self.start_head[0]) * progress,
                self.start_head[1] + (self.target_head[1] - self.start_head[1]) * progress
            ]
            
            # อัพเดทตำแหน่งลำตัว
            self.body_positions = []
            for i in range(len(self.target_body)):
                if i < len(self.start_body):
                    pos = [
                        self.start_body[i][0] + (self.target_body[i][0] - self.start_body[i][0]) * progress,
                        self.start_body[i][1] + (self.target_body[i][1] - self.start_body[i][1]) * progress
                    ]
                else:
                    pos = self.target_body[i][:]
                self.body_positions.append(pos)
            
            if progress >= 1:
                self.moving = False
                self.snake_head = self.target_head[:]
                
                if self.snake_head == self.food_pos:
                    self.score += 1
                    if self.body_positions:
                        self.body_positions.append(self.body_positions[-1][:])
                    else:
                        self.body_positions.append(self.start_head[:])
                    self.spawn_food()
                    self.update_label.text = f"Score: {self.score}"
                    if self.score > self.best_score:
                        self.best_score = self.score
                        self.best_score_label.text = f"Best: {self.best_score}"
                    if self.eat_sound:
                        self.eat_sound.play()
                    
                    # Increase level every 5 points
                    if self.score % 5 == 0:
                        self.level += 1
                        self.level_label.text = f"Level: {self.level}"
                        self.speed -= 0.01  # Increase speed
                        Clock.unschedule(self.update)
                        self.update_event = Clock.schedule_interval(self.update, self.speed)

        # วาดกราฟิก
        self.draw_snake()
        self.draw_food()
    
    def game_over_screen(self):
        self.paused = True
        self.pause_layout.opacity = 1
        Clock.unschedule(self.update)
        
        # Create "Game Over" label and animate it
        game_over_label = Label(text="GAME OVER", font_size=50, color=(1, 0, 0, 1),
                                size_hint=(None, None), size=(300, 100),
                                pos=(Window.width / 2 - 150, Window.height / 2 + 65))
        
        self.add_widget(game_over_label)
        
        # Animation to make the text scale up
        anim = Animation(font_size=80, duration=1.5) + Animation(font_size=50, duration=1.5)
        anim.start(game_over_label)

    def go_to_menu(self, instance):
        self.manager.current = 'menu'
    
    def draw_snake(self):
        self.game_widget.canvas.clear()  # เคลียร์ Canvas ก่อนวาดใหม่
        with self.game_widget.canvas:
            try:
            # โหลด texture หัวงู
                head_texture = Image(source="assets/snake_head.png").texture
                x, y = self.snake_head
                Rectangle(texture=head_texture, pos=(x, y),
                      size=(self.snake_size, self.snake_size))

            # โหลด texture ตัวงู
                body_texture = Image(source="assets/snake_body.png").texture
                for x, y in self.body_positions:
                    Rectangle(texture=body_texture, pos=(x, y),
                          size=(self.snake_size, self.snake_size))

            except Exception as e:
                print(f"Error loading snake texture: {e}")  # แสดงข้อผิดพลาดถ้ามีปัญหา


    def draw_food(self):
        with self.game_widget.canvas:
            Color(1, 0, 0)
            x, y = self.food_pos
            Rectangle(pos=(x, y),
                      size=(self.snake_size, self.snake_size))

    def on_key_down(self, instance, key, *args):
        if key == 112:  # 112 คือรหัสของปุ่ม P
            self.paused = not self.paused
        if not self.paused:
            if key == 273 and self.snake_direction != Vector(0, -1):
                self.snake_direction = Vector(0, 1)
                self.up_sound.play()
            elif key == 274 and self.snake_direction != Vector(0, 1):
                self.snake_direction = Vector(0, -1)
                self.down_sound.play()
            elif key == 275 and self.snake_direction != Vector(-1, 0):
                self.snake_direction = Vector(1, 0)
                self.right_sound.play()
            elif key == 276 and self.snake_direction != Vector(1, 0):
                self.snake_direction = Vector(-1, 0)
                self.left_sound.play()

    def generate_food(self):
        return [random.randint(0, 19) * self.snake_size, random.randint(0, 19) * self.snake_size]

class SnakeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SnakeGame(name='game'))
        return sm

if __name__ == '__main__':
    SnakeApp().run()