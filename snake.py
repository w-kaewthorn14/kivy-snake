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
        
        with self.canvas.before:
            self.bg_texture = Image(source='assets/background.png').texture
            self.bg_rect = Rectangle(texture=self.bg_texture, pos=self.pos, size=Window.size)
        
 
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        main_layout = BoxLayout(orientation='vertical', spacing=20, padding=50, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        title_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4), pos_hint={'center_x': 0.5})
        
        title_label = Label(
            text="Kivy Snake",
            font_size=60,
            bold=True,
            color=(0.2, 0.4, 1.0, 1),  
            size_hint=(1, 0.7),
            halign='center'  
        )
        title_label.bind(size=lambda *x: setattr(title_label, 'text_size', (title_label.width, None)))
        
        subtitle_label = Label(
            text="Game made by 6710110246 and 6710110391",
            font_size=24,
            italic=True,
            color=(0.2, 0.4, 1.0, 1),  
            size_hint=(1, 0.3),
            halign='center'  
        )
        subtitle_label.bind(size=lambda *x: setattr(subtitle_label, 'text_size', (subtitle_label.width, None)))
        
        title_layout.add_widget(title_label)
        title_layout.add_widget(subtitle_label)
        
        # Layout สำหรับปุ่มเมนู - ใช้ AnchorLayout แทน BoxLayout เพื่อให้จัดกลางได้ดีขึ้น
        button_layout = BoxLayout(orientation='vertical', spacing=15, size_hint=(None, None))
        button_layout.size = (300, 200)
        button_layout.pos_hint = {'center_x': 0.5}
        
        # ปรับขนาดปุ่มให้เท่ากันและให้อยู่ตรงกลาง
        start_button = Button(
            text='Start Game', 
            font_size=24, 
            size_hint=(None, None), 
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        
        setting_button = Button(
            text='Setting', 
            font_size=24, 
            size_hint=(None, None), 
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        
        exit_button = Button(
            text='Exit', 
            font_size=24, 
            size_hint=(None, None), 
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        
        start_button.bind(on_release=self.start_game)
        setting_button.bind(on_release=self.open_setting)
        exit_button.bind(on_release=self.exit_game)
        
        button_layout.add_widget(start_button)
        button_layout.add_widget(setting_button)
        button_layout.add_widget(exit_button)
        
        # เพิ่ม AnchorLayout สำหรับปุ่มให้อยู่ตรงกลาง
        button_container = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.6))
        button_container.add_widget(button_layout)
        
        main_layout.add_widget(title_layout)
        main_layout.add_widget(button_container)
        
        # ใช้ AnchorLayout เป็น root widget เพื่อให้ main_layout อยู่ตรงกลางหน้าจอ
        root_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        root_layout.add_widget(main_layout)
        
        self.add_widget(root_layout)
    
    # Missing method needed for background update - add this
    def _update_bg(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
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
        game_screen.reset_game(None)  # แก้ไขปัญหา reset_game
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

        easy_button.bind(on_release=lambda x: self.set_difficulty('easy'))
        medium_button.bind(on_release=lambda x: self.set_difficulty('medium'))
        hard_button.bind(on_release=lambda x: self.set_difficulty('hard'))
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
    def set_difficulty(self, difficulty):
        # เปลี่ยนจาก start_game เป็น set_difficulty
        self.play_click_sound()
        game_screen = self.manager.get_screen('game')
        # เก็บค่าความยากไว้โดยไม่เริ่มเกมทันที
        game_screen.set_difficulty(difficulty)
        # แสดงข้อความแจ้งให้กับผู้เล่น
        self.show_confirmation(difficulty)
    
    def show_confirmation(self, difficulty):
        # สร้างและแสดงข้อความยืนยันการตั้งค่า
        if hasattr(self, 'confirm_label'):
            self.remove_widget(self.confirm_label)
        
        self.confirm_label = Label(
            text=f"Difficulty set to {difficulty}! Press 'Start Game' on Menu to play.",
            font_size=20,
            size_hint=(None, None),
            size=(500, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.add_widget(self.confirm_label)
        
        # ตั้งเวลาให้ข้อความหายไปหลังจาก 3 วินาที
        Clock.schedule_once(self.remove_confirmation, 3)
    
    def remove_confirmation(self, dt):
        if hasattr(self, 'confirm_label'):
            self.remove_widget(self.confirm_label)
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
        self.food_items = []
        self.food_count = 1
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
        
        self.stats_box = BoxLayout(
        orientation='vertical',
        size_hint=(None, None),
        size=(150, 120),
        pos=(0, 0),  # Bottom-left position
        padding=5
        )

        # Add a background to the stats box
        with self.stats_box.canvas.before:
            Color(0, 0, 0, 1)  # Semi-transparent black
            self.stats_bg = Rectangle(pos=self.stats_box.pos, size=self.stats_box.size)

        # Bind the position and size of the box to the background
        self.stats_box.bind(pos=self._update_stats_bg, size=self._update_stats_bg)

        # Create the labels with consistent styling
        self.best_score_label = Label(
            text="Best Score: 0", 
            font_size=18,
            halign='left',
            valign='middle',
            size_hint=(1, 1)
        )

        self.update_label = Label(
            text="Score: 0", 
            font_size=18,
            halign='left',
            valign='middle',
            size_hint=(1, 1)
        )

        self.timer_label = Label(
            text="Time: 0", 
            font_size=18,
            halign='left',
            valign='middle',
            size_hint=(1, 1)
        )

        self.level_label = Label(
            text="Level: 1", 
            font_size=18,
            halign='left',
            valign='middle',
            size_hint=(1, 1)
        )

        # Add labels to the box
        self.stats_box.add_widget(self.best_score_label)
        self.stats_box.add_widget(self.update_label)
        self.stats_box.add_widget(self.timer_label)
        self.stats_box.add_widget(self.level_label)

        # Add the stats box to the game screen
        self.add_widget(self.stats_box)

        # Add this method to update the background of the stats box

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
        
        resume_button.bind(on_release=self.reset_game)  # Fixed this line to connect to reset_game
        menu_button.bind(on_release=self.go_to_menu)
        
        self.pause_layout.add_widget(resume_button)
        self.pause_layout.add_widget(menu_button)
        self.add_widget(self.pause_layout)
        
        Window.bind(on_key_down=self.on_key_down)

    def _update_stats_bg(self, instance, value):
        self.stats_bg.pos = instance.pos
        self.stats_bg.size = instance.size
        

    
    def _update_bg(self, *args):
        # อัปเดตขนาดและตำแหน่งของพื้นหลัง
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def start_game(self):
        # เมธอดนี้จะถูกเรียกเมื่อกดปุ่ม Start หรือเลือกความยาก
        self.paused = False
        Clock.unschedule(self.update_event)  # ยกเลิกการอัปเดตก่อนหน้า (ถ้ามี)
        Clock.unschedule(self.animation_event)  # ยกเลิกการอัพเดทแอนิเมชั่นก่อนหน้า
        
        self.generate_food_items()
        # แยกการอัพเดทออกเป็น 2 ส่วน:
        # 1. อัพเดทลอจิกเกม (ตำแหน่งงู, ตรวจสอบการชน, ฯลฯ)
        self.update_event = Clock.schedule_interval(self.update_game_logic, self.speed)
        
        # 2. อัพเดทแอนิเมชั่น (การเคลื่อนที่ราบรื่น)
        self.animation_event = Clock.schedule_interval(self.update_animation, 1/60)  # 60 FPS
    
    def set_difficulty(self, difficulty):
        if difficulty == 'easy':
            self.speed = 0.15
            self.move_speed = 3
            self.food_count = 1
        elif difficulty == 'medium':
            self.speed = 0.1
            self.move_speed = 5
            self.food_count = 3
        elif difficulty == 'hard':
            self.speed = 0.05
            self.move_speed = 10
            self.food_count = 5
    
    def generate_food(self):
        # สร้างตำแหน่งอาหารใหม่ที่ไม่อยู่ในตำแหน่งงูและไม่ทับกับ stats box
        max_x = (Window.width // self.snake_size) - 1
        max_y = (Window.height // self.snake_size) - 1
        
        # คำนวณพื้นที่ของ stats box (แปลงเป็นหน่วย grid)
        stats_width = self.stats_box.size[0] // self.snake_size + 1  # +1 เพื่อความปลอดภัย
        stats_height = self.stats_box.size[1] // self.snake_size + 1  # +1 เพื่อความปลอดภัย
        
        # สร้างตำแหน่งสุ่ม และตรวจสอบว่าไม่ซ้อนทับกับงูและไม่อยู่ใน stats box
        while True:
            food_x = random.randint(0, max_x)
            food_y = random.randint(0, max_y)
            food = (food_x, food_y)
            
            # ตรวจสอบว่าไม่อยู่ใน stats box (ซ้ายล่าง)
            if food_x < stats_width and food_y < stats_height:
                continue  # อยู่ใน stats box, ลองใหม่
                
            # ตรวจสอบว่าไม่ทับซ้อนกับงูและอาหารอื่น
            if food not in self.snake and food not in self.food_items:
                return food
    def generate_food_items(self):
        # ล้างรายการอาหารเดิม
        self.food_items = []
        
        # สร้างอาหารใหม่ตามจำนวนที่กำหนด
        for _ in range(self.food_count):
            self.food_items.append(self.generate_food())
            
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
        # อัพเดทลอจิกเกมเหมือนเดิม 
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
        
        # ตรวจสอบว่างูกินอาหารหรือไม่
        if new_head in self.food_items:  # เปลี่ยนจาก new_head == self.food_items เป็น new_head in self.food_items
            food_index = self.food_items.index(new_head)
            # เพิ่มส่วนท้ายสุดที่จะมีต่อกับส่วนที่มีอยู่
            last_segment = self.snake[-1]
        
            # อัพเดทตำแหน่งงูใน grid โดยยังไม่ตัดหางออก
            self.snake = [new_head] + self.snake
            
            # คำนวณตำแหน่งที่เหมาะสมสำหรับส่วนใหม่ (ถัดจากส่วนสุดท้าย)
            if len(self.smooth_positions) >= 2:
                # คำนวณทิศทางจากส่วนก่อนสุดท้ายไปยังส่วนสุดท้าย
                last_x, last_y = self.smooth_positions[-1]
                second_last_x, second_last_y = self.smooth_positions[-2]
                
                dx = last_x - second_last_x
                dy = last_y - second_last_y
                distance = (dx**2 + dy**2)**0.5
                
                if distance > 0:
                    # ต่อส่วนใหม่ในทิศทางเดียวกัน
                    new_segment_x = last_x + (dx / distance * self.snake_size)
                    new_segment_y = last_y + (dy / distance * self.snake_size)
                else:
                    # ถ้าไม่มีทิศทางชัดเจน ให้ต่อไปด้านหลัง
                    new_segment_x = last_x
                    new_segment_y = last_y - self.snake_size
            else:
                # กรณีที่มีเพียงส่วนเดียว
                new_segment_x = last_segment[0] * self.snake_size
                new_segment_y = last_segment[1] * self.snake_size
            
            # เพิ่มตำแหน่งใหม่ในลิสต์
            self.smooth_positions.append((new_segment_x, new_segment_y))
            
            self.score += 1
            self.update_label.text = f"Score: {self.score}"
            if self.score > self.best_score:
                self.best_score = self.score
                self.best_score_label.text = f"Best score: {self.best_score}"
            if self.eat_sound:
                self.eat_sound.volume = self.manager.get_screen('setting').volume_slider.value
                self.eat_sound.play()
            
            # ลบอาหารที่กินแล้วและสร้างอาหารใหม่แทน
            self.food_items.pop(food_index)
            self.food_items.append(self.generate_food())
            
            # Increase level every 5 points
            if self.score % 5 == 0:
                self.level += 1
                self.level_label.text = f"Level: {self.level}"
                self.speed = max(self.speed - 0.01, 0.02)  # Increase speed, but not less than 0.02
                Clock.unschedule(self.update_event)
                self.update_event = Clock.schedule_interval(self.update_game_logic, self.speed)
        else:
            # อัพเดทตำแหน่งงูใน grid (เลื่อนงูตามปกติ)
            self.snake = [new_head] + self.snake[:-1]
            
            # ปรับให้ smooth_positions มีจำนวนเท่ากับ snake
            if len(self.smooth_positions) > len(self.snake):
                self.smooth_positions = self.smooth_positions[:len(self.snake)]
    
    def update_animation(self, dt):
        # อัพเดทการเคลื่อนที่แบบราบรื่น
        if self.paused:
            return
        
        # กำหนดระยะห่างระหว่างส่วนต่างๆ ของงู
        segment_distance = self.snake_size * 0.95  # ระยะห่างที่เหมาะสมระหว่างส่วนของงู
        
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
        
        # ตรวจสอบว่าจำนวนของ smooth_positions ตรงกับจำนวนของ snake
        while len(self.smooth_positions) < len(self.snake):
            # ถ้า smooth_positions มีน้อยกว่า snake ให้เพิ่มตำแหน่ง
            last_pos = self.smooth_positions[-1]
            self.smooth_positions.append(last_pos)
        
        # ปรับ smooth_positions ให้มีจำนวนเท่ากับ snake (กรณีมีมากเกินไป)
        while len(self.smooth_positions) > len(self.snake):
            self.smooth_positions.pop()
        
        # อัพเดทตำแหน่งส่วนอื่นๆ ของงู (body segments) ให้เคลื่อนที่ตาม grid
        for i in range(1, len(self.snake)):
            # เป้าหมายคือตำแหน่ง grid ของส่วนนี้
            target_x = self.snake[i][0] * self.snake_size
            target_y = self.snake[i][1] * self.snake_size
            curr_x, curr_y = self.smooth_positions[i]
            
            # คำนวณระยะทางจากตำแหน่งปัจจุบันไปยังตำแหน่งเป้าหมาย
            dx = target_x - curr_x
            dy = target_y - curr_y
            distance = (dx**2 + dy**2)**0.5
            
            # กำหนดความเร็วในการเคลื่อนที่ (อาจจะเร็วกว่าหัวงูเล็กน้อยเพื่อให้ไม่ล้าหลัง)
            body_speed = self.move_speed * 1.2  # เร็วกว่าหัวงูเล็กน้อย
            
            # หากตำแหน่งปัจจุบันใกล้เคียงกับเป้าหมายแล้ว ให้เท่ากับเป้าหมายเลย
            if distance < body_speed:
                new_x, new_y = target_x, target_y
            else:
                # คำนวณทิศทางและระยะทางในการเคลื่อนที่
                if distance > 0:  # ป้องกันการหารด้วยศูนย์
                    move_x = dx / distance * body_speed
                    move_y = dy / distance * body_speed
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
                for food_pos in self.food_items:
                    x, y = food_pos
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
        self.food_items = []  # เคลียร์รายการอาหารเดิม
        self.generate_food_items()
        self.score = 0
        self.level = 1
        self.update_label.text = "Score: 0"
        self.level_label.text = "Level: 1"
        
        # รีเซ็ตความเร็วตามระดับความยากที่เลือกไว้
        if hasattr(self, 'current_difficulty'):
            self.set_difficulty(self.current_difficulty)
        else:
        # ค่าเริ่มต้นถ้าไม่มีการเลือกความยาก
            self.speed = 0.1
            self.move_speed = 5
            
        # รีเซ็ตตำแหน่งแบบราบรื่น
        self.smooth_positions = [(10 * self.snake_size, 10 * self.snake_size)]
    
        # Clear both the main canvas and the background canvas
        self.game_widget.canvas.clear()
        self.game_widget.canvas.before.clear()
        
        # Re-add the background
        with self.canvas.before:
            self.bg_texture = Image(source='assets/background.png').texture
            self.bg_rect = Rectangle(texture=self.bg_texture, pos=self.pos, size=Window.size)
    
        self.paused = False  # Changed from True to False
        self.pause_layout.opacity = 0
        self.timer = 0
        self.timer_label.text = "Time: 0"
        Clock.unschedule(self.update_event)
        Clock.unschedule(self.animation_event)
    
        # ลบ "GAME OVER" label ถ้ามี
        for widget in self.children:
            if isinstance(widget, Label) and widget.text == "GAME OVER":
                self.remove_widget(widget)
        self.start_game()        
class SnakeApp(App):
        def build(self):
                # สร้าง ScreenManager สำหรับจัดการหน้าจอต่างๆ
            sm = ScreenManager()
        
                # เพิ่มหน้าจอต่างๆ เข้าไปใน ScreenManager
            menu_screen = MenuScreen(name='menu')
            setting_screen = SettingScreen(name='setting')
            game_screen = SnakeGame(name='game')
        
            sm.add_widget(menu_screen)
            sm.add_widget(setting_screen)
            sm.add_widget(game_screen)
        
                # ตั้งค่าให้เริ่มต้นที่หน้า menu
            sm.current = 'menu'
        
            return sm

if __name__ == '__main__':
    SnakeApp().run()