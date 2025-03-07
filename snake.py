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
from kivy.uix.slider import Slider
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics.texture import Texture

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.click_sound = SoundLoader.load('assets/click.mp3')
        
        # เพิ่มพื้นหลังให้กับหน้าเมนู
        with self.canvas.before:
            self.bg_texture = Image(source='assets/background.png').texture
            self.bg_rect = Rectangle(texture=self.bg_texture, pos=self.pos, size=Window.size)
        
        # ผูกการปรับขนาดหน้าจอกับพื้นหลัง
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=50, size_hint=(None, None))
        layout.size = (300, 200)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        start_button = Button(text='Start Game', font_size=24, size_hint=(None, None), size=(200, 50))
        setting_button = Button(text='Setting', font_size=24, size_hint=(None, None), size=(200, 50))
        exit_button = Button(text='Exit', font_size=24, size_hint=(None, None), size=(200, 50))
        
        start_button.bind(on_release=self.start_game)
        setting_button.bind(on_release=self.open_setting)
        exit_button.bind(on_release=self.exit_game)
        
        layout.add_widget(start_button)
        layout.add_widget(setting_button)
        layout.add_widget(exit_button)
        
        self.add_widget(layout)
    
    def _update_bg(self, *args):
        # อัปเดตขนาดและตำแหน่งของพื้นหลัง
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def play_click_sound(self):
        if self.click_sound:
            self.click_sound.volume = self.manager.get_screen('setting').volume_slider.value
            self.click_sound.play()

    def start_game(self, instance):
        self.play_click_sound()
        game_screen = self.manager.get_screen('game')
        game_screen.reset_game(None)
        game_screen.start_game()
        self.manager.current = 'game'
    
    def open_setting(self, instance):
        self.play_click_sound()
        self.manager.current = 'setting'
    
    def exit_game(self, instance):
        self.play_click_sound()
        App.get_running_app().stop()

class SettingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.click_sound = SoundLoader.load('assets/click.mp3')
        
        # เพิ่มพื้นหลังให้กับหน้าตั้งค่า
        with self.canvas.before:
            self.bg_texture = Image(source='assets/background.png').texture
            #self.bg_texture.wrap = 'repeat'
            self.bg_rect = Rectangle(texture=self.bg_texture, pos=self.pos, size=Window.size)
        
        # ผูกการปรับขนาดหน้าจอกับพื้นหลัง
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Layout หลัก
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Layout สำหรับปรับเสียง
        volume_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(400, 50), spacing=20)
        volume_label = Label(text='Volume', font_size=24, size_hint=(None, None), size=(100, 50))
        self.volume_slider = Slider(min=0, max=1, value=0.5, size_hint=(1, None), height=40)
        volume_layout.add_widget(volume_label)
        volume_layout.add_widget(self.volume_slider)

        # Layout สำหรับปุ่ม
        button_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(300, 300), spacing=15)
        button_style = {'font_size': 24, 'size_hint': (None, None), 'size': (250, 50)}

        easy_button = Button(text='Easy', **button_style)
        medium_button = Button(text='Medium', **button_style)
        hard_button = Button(text='Hard', **button_style)
        back_button = Button(text='Back to Menu', **button_style)

        easy_button.bind(on_release=lambda x: self.start_game('easy'))
        medium_button.bind(on_release=lambda x: self.start_game('medium'))
        hard_button.bind(on_release=lambda x: self.start_game('hard'))
        back_button.bind(on_release=self.go_to_menu)

        button_layout.add_widget(easy_button)
        button_layout.add_widget(medium_button)
        button_layout.add_widget(hard_button)
        button_layout.add_widget(back_button)

        # ใช้ AnchorLayout เพื่อจัดกึ่งกลางหน้าจอ
        center_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        content_layout = BoxLayout(orientation='vertical', spacing=30, size_hint=(None, None), size=(400, 400))

        content_layout.add_widget(volume_layout)
        content_layout.add_widget(button_layout)
        center_layout.add_widget(content_layout)

        main_layout.add_widget(center_layout)
        self.add_widget(main_layout)
    
    def _update_bg(self, *args):
        # อัปเดตขนาดและตำแหน่งของพื้นหลัง
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def play_click_sound(self):
        if self.click_sound:
            self.click_sound.volume = self.volume_slider.value
            self.click_sound.play()

    def start_game(self, difficulty):
        self.play_click_sound()
        game_screen = self.manager.get_screen('game')
        game_screen.reset_game(None)
        game_screen.set_difficulty(difficulty)
        game_screen.start_game()
        self.manager.current = 'game'
    
    def go_to_menu(self, instance):
        self.play_click_sound()
        self.manager.current = 'menu'

class SnakeGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # เพิ่มพื้นหลังให้กับหน้าเกม
        with self.canvas.before:
            self.bg_texture = Image(source='assets/background.png').texture
            self.bg_rect = Rectangle(texture=self.bg_texture, pos=self.pos, size=Window.size)
        
        # ผูกการปรับขนาดหน้าจอกับพื้นหลัง
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        self.game_widget = Widget()
        self.add_widget(self.game_widget)
        
        self.snake = [(10, 10)]
        self.snake_direction = (1, 0)
        self.food = (random.randint(0, 19), random.randint(0, 19))
        self.score = 0
        self.best_score = 0
        self.snake_size = 35
        self.paused = True
        self.level = 1
        self.speed = 0.1
        
        # เพิ่มตัวแปรสำหรับการเคลื่อนไหวแบบราบรื่น
        self.smooth_positions = [(10 * self.snake_size, 10 * self.snake_size)]  # ตำแหน่งจริงที่แสดงบนหน้าจอ
        self.move_speed = 5  # ความเร็วในการเคลื่อนที่ (pixel ต่อเฟรม)
        
        self.update_event = None
        self.animation_event = None  # เพิ่มตัวแปรสำหรับการอัปเดตแบบ animation
        
        # ส่วนอื่นของ __init__ คงเดิม
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
        
        Window.bind(on_key_down=self.on_key_down)
    
    def _update_bg(self, *args):
        # อัปเดตขนาดและตำแหน่งของพื้นหลัง
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def start_game(self):
        # เมธอดนี้จะถูกเรียกเมื่อกดปุ่ม Start หรือเลือกความยาก
        self.paused = False
        Clock.unschedule(self.update_event)  # ยกเลิกการอัปเดตก่อนหน้า (ถ้ามี)
        Clock.unschedule(self.animation_event)  # ยกเลิกการอัพเดทแอนิเมชั่นก่อนหน้า
        
        # แยกการอัพเดทออกเป็น 2 ส่วน:
        # 1. อัพเดทลอจิกเกม (ตำแหน่งงู, ตรวจสอบการชน, ฯลฯ)
        self.update_event = Clock.schedule_interval(self.update_game_logic, self.speed)
        
        # 2. อัพเดทแอนิเมชั่น (การเคลื่อนที่ราบรื่น)
        self.animation_event = Clock.schedule_interval(self.update_animation, 1/60)  # 60 FPS
    
    def set_difficulty(self, difficulty):
        if difficulty == 'easy':
            self.speed = 0.2
            self.move_speed = 3
        elif difficulty == 'medium':
            self.speed = 0.1
            self.move_speed = 5
        elif difficulty == 'hard':
            self.speed = 0.05
            self.move_speed = 10
    
    def generate_food(self):
        # สร้างตำแหน่งอาหารใหม่ที่ไม่อยู่ในตำแหน่งงู
        max_x = (Window.width // self.snake_size) - 1
        max_y = (Window.height // self.snake_size) - 1
        
        # สร้างตำแหน่งสุ่ม และตรวจสอบว่าไม่ซ้อนทับกับงู
        while True:
            food = (random.randint(0, max_x), random.randint(0, max_y))
            if food not in self.snake:
                return food
    
    def game_over_screen(self):
        self.paused = True
        
        # แสดงข้อความ GAME OVER
        game_over_label = Label(text="GAME OVER", font_size=40,
                                size_hint=(None, None), size=(300, 100),
                                pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.add_widget(game_over_label)
        
        # แสดง pause layout สำหรับ Play Again และ Go to Menu
        self.pause_layout.opacity = 1
        
        # หยุดการอัปเดต
        Clock.unschedule(self.update_event)
        Clock.unschedule(self.animation_event)
    
    def go_to_menu(self, instance):
        # กลับไปหน้าเมนู
        if hasattr(self.manager.get_screen('menu'), 'play_click_sound'):
            self.manager.get_screen('menu').play_click_sound()
        
        # ลบ "GAME OVER" label ถ้ามี
        for widget in self.children:
            if isinstance(widget, Label) and widget.text == "GAME OVER":
                self.remove_widget(widget)
                
        self.pause_layout.opacity = 0
        self.manager.current = 'menu'
    
    def on_key_down(self, window, key, *args):
        if self.paused:
            return
        
        # รับการควบคุมจาก keyboard
        from kivy.core.window import Keyboard
        
        # ทิศทางปัจจุบัน
        current_direction = self.snake_direction
        volume = self.manager.get_screen('setting').volume_slider.value
        
        # ตรวจสอบปุ่มที่กด และอัปเดตทิศทาง (ป้องกันไม่ให้กลับทิศทางตรงข้าม)
        if key == Keyboard.keycodes['up'] and current_direction != (0, -1):
            self.snake_direction = (0, 1)
            if self.up_sound:
                self.up_sound.volume = volume
                self.up_sound.play()
        elif key == Keyboard.keycodes['down'] and current_direction != (0, 1):
            self.snake_direction = (0, -1)
            if self.down_sound:
                self.down_sound.volume = volume
                self.down_sound.play()
        elif key == Keyboard.keycodes['left'] and current_direction != (1, 0):
            self.snake_direction = (-1, 0)
            if self.left_sound:
                self.left_sound.volume = volume
                self.left_sound.play()
        elif key == Keyboard.keycodes['right'] and current_direction != (-1, 0):
            self.snake_direction = (1, 0)
            if self.right_sound:
                self.right_sound.volume = volume
                self.right_sound.play()
        elif key == Keyboard.keycodes['p']:  # พักเกม
            if not self.paused:
                self.paused = True
                self.pause_layout.opacity = 1
            else:
                self.paused = False
                self.pause_layout.opacity = 0
                self.start_game()
        elif key == Keyboard.keycodes['escape']:  # กลับไปเมนูหลัก
            self.go_to_menu(None)
    
    def update_game_logic(self, dt):
        # อัพเดทลอจิกเกมเหมือนเดิม แต่ไม่วาดงูที่นี่
        if self.paused:
            return
        
        self.timer += 1
        self.timer_label.text = f"Time: {self.timer // 10}"
        
        new_head = (self.snake[0][0] + self.snake_direction[0],
                    self.snake[0][1] + self.snake_direction[1])
        
        # ตรวจสอบว่างูชนขอบหรือตัวเองหรือไม่
        if (new_head[0] < 0 or new_head[0] >= Window.width // self.snake_size or
            new_head[1] < 0 or new_head[1] >= Window.height // self.snake_size or
            new_head in self.snake):
            if self.game_over_sound:
                self.game_over_sound.volume = self.manager.get_screen('setting').volume_slider.value
                self.game_over_sound.play()
            self.game_over_screen()
            return
        
        # อัพเดทตำแหน่งงูใน grid
        self.snake = [new_head] + self.snake[:-1]
        
        # เพิ่มตำแหน่งเป้าหมายใหม่ที่งูจะเคลื่อนที่ไป
        target_x = new_head[0] * self.snake_size
        target_y = new_head[1] * self.snake_size
        
        # เพิ่มตำแหน่งเป้าหมายใหม่ไปยัง smooth_positions
        if len(self.smooth_positions) < len(self.snake):
            self.smooth_positions.append(self.smooth_positions[-1])
        
        # ตรวจสอบว่างูกินอาหารหรือไม่
        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.smooth_positions.append(self.smooth_positions[-1])  # เพิ่มตำแหน่งสำหรับส่วนที่เพิ่ม
            
            self.score += 1
            self.update_label.text = f"Score: {self.score}"
            if self.score > self.best_score:
                self.best_score = self.score
                self.best_score_label.text = f"Best score: {self.best_score}"
            if self.eat_sound:
                self.eat_sound.volume = self.manager.get_screen('setting').volume_slider.value
                self.eat_sound.play()
            self.food = self.generate_food()
            
            # Increase level every 5 points
            if self.score % 5 == 0:
                self.level += 1
                self.level_label.text = f"Level: {self.level}"
                self.speed = max(self.speed - 0.01, 0.02)  # Increase speed, but not less than 0.02
                Clock.unschedule(self.update_event)
                self.update_event = Clock.schedule_interval(self.update_game_logic, self.speed)
    
    def update_animation(self, dt):
        # อัพเดทการเคลื่อนที่แบบราบรื่น
        if self.paused:
            return
        
        # อัพเดทตำแหน่งหัวงู
        target_x = self.snake[0][0] * self.snake_size
        target_y = self.snake[0][1] * self.snake_size
        curr_x, curr_y = self.smooth_positions[0]
        
        # คำนวณตำแหน่งใหม่ให้เคลื่อนที่เข้าหาตำแหน่งเป้าหมาย
        dx = target_x - curr_x
        dy = target_y - curr_y
        
        # หากตำแหน่งปัจจุบันใกล้เคียงกับเป้าหมายแล้ว ให้เท่ากับเป้าหมายเลย
        if abs(dx) < self.move_speed and abs(dy) < self.move_speed:
            new_x, new_y = target_x, target_y
        else:
            # คำนวณทิศทางและระยะทางในการเคลื่อนที่
            distance = (dx**2 + dy**2)**0.5
            if distance > 0:  # ป้องกันการหารด้วยศูนย์
                move_x = dx / distance * self.move_speed
                move_y = dy / distance * self.move_speed
            else:
                move_x, move_y = 0, 0
            
            new_x = curr_x + move_x
            new_y = curr_y + move_y
        
        self.smooth_positions[0] = (new_x, new_y)
        
        # อัพเดทตำแหน่งส่วนอื่นๆ ของงู (แต่ละส่วนจะตามส่วนหน้า)
        for i in range(1, len(self.smooth_positions)):
            target_x, target_y = self.smooth_positions[i-1]
            curr_x, curr_y = self.smooth_positions[i]
            
            dx = target_x - curr_x
            dy = target_y - curr_y
            
            # เงื่อนไขเช่นเดียวกับส่วนหัว
            if abs(dx) < self.move_speed and abs(dy) < self.move_speed:
                new_x, new_y = target_x, target_y
            else:
                distance = (dx**2 + dy**2)**0.5
                if distance > 0:
                    move_x = dx / distance * self.move_speed
                    move_y = dy / distance * self.move_speed
                else:
                    move_x, move_y = 0, 0
                
                new_x = curr_x + move_x
                new_y = curr_y + move_y
            
            self.smooth_positions[i] = (new_x, new_y)
        
        # วาดงูและอาหาร
        self.game_widget.canvas.clear()
        self.draw_snake()
        self.draw_food()
        
    def draw_snake(self):
        with self.game_widget.canvas:
            try:
                # โหลด texture หัวงู
                head_texture = Image(source="assets/snake_head.png").texture
                x, y = self.smooth_positions[0]  # ใช้ตำแหน่งแบบราบรื่น
                Rectangle(texture=head_texture, pos=(x, y), size=(self.snake_size, self.snake_size))

                # โหลด texture ตัวงู
                body_texture = Image(source="assets/snake_body.png").texture
                for i in range(1, len(self.smooth_positions)):  # ใช้ตำแหน่งแบบราบรื่นสำหรับทุกส่วน
                    x, y = self.smooth_positions[i]
                    Rectangle(texture=body_texture, pos=(x, y), size=(self.snake_size, self.snake_size))

            except Exception as e:
                print(f"Error loading snake texture: {e}")
                # ใช้สีแทนถ้าไม่สามารถโหลดรูปได้
                Color(0, 1, 0, 1)  # สีเขียว
                x, y = self.smooth_positions[0]
                Rectangle(pos=(x, y), size=(self.snake_size, self.snake_size))
                
                Color(0, 0.8, 0, 1)  # สีเขียวเข้ม
                for i in range(1, len(self.smooth_positions)):
                    x, y = self.smooth_positions[i]
                    Rectangle(pos=(x, y), size=(self.snake_size, self.snake_size))

    def draw_food(self):
        with self.game_widget.canvas:
            try:
                # โหลด texture ของอาหาร (แอปเปิล)
                food_texture = Image(source="assets/Apple.webp").texture
                x, y = self.food
                Rectangle(texture=food_texture, 
                      pos=(x * self.snake_size, y * self.snake_size),   
                      size=(self.snake_size, self.snake_size))
            except Exception as e:
                print(f"Error loading food texture: {e}")
                # ใช้สีแทนถ้าไม่สามารถโหลดรูปได้
                Color(1, 0, 0, 1)  # สีแดง
                x, y = self.food
                Rectangle(pos=(x * self.snake_size, y * self.snake_size),
                      size=(self.snake_size, self.snake_size))
    
    def reset_game(self, instance):
        self.snake = [(10, 10)]
        self.snake_direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.level = 1
        self.update_label.text = "Score: 0"
        self.level_label.text = "Level: 1"
        
        # รีเซ็ตตำแหน่งแบบราบรื่น
        self.smooth_positions = [(10 * self.snake_size, 10 * self.snake_size)]
    
        # Clear both the main canvas and the background canvas
        self.game_widget.canvas.clear()
        self.game_widget.canvas.before.clear()
    
        self.paused = True
        self.pause_layout.opacity = 0
        self.timer = 0
        self.timer_label.text = "Time: 0"
        Clock.unschedule(self.update_event)
        Clock.unschedule(self.animation_event)
    
        self.start_game()
        # ลบ "GAME OVER" label ถ้ามี
        for widget in self.children:
            if isinstance(widget, Label) and widget.text == "GAME OVER":
                self.remove_widget(widget)

# เพิ่ม SnakeApp เพื่อรัน application
class SnakeApp(App):
    def build(self):
        # สร้าง screen manager
        sm = ScreenManager()
        
        # สร้างหน้าจอต่างๆ
        menu_screen = MenuScreen(name='menu')
        setting_screen = SettingScreen(name='setting')
        game_screen = SnakeGame(name='game')
        
        # เพิ่มหน้าจอเข้า screen manager
        sm.add_widget(menu_screen)
        sm.add_widget(setting_screen)
        sm.add_widget(game_screen)
        
        # เริ่มที่หน้าเมนู
        sm.current = 'menu'
        
        return sm

if __name__ == '__main__':
    SnakeApp().run()