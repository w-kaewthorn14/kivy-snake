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
        
        self.snake = [(10, 10)]  # หัวและลำตัวงู
        self.snake_direction = (1, 0)  # ทิศทางเริ่มต้น (ไปทางขวา)
        self.food = (random.randint(0, 19), random.randint(0, 19))  # ตำแหน่งอาหารแบบสุ่ม
        self.score = 0
        self.snake_size = 20  # ขนาดของแต่ละบล็อกของงูและอาหาร
        
        self.update_label = Label(text="Score: 0", pos=(10, Window.height - 30))
        self.add_widget(self.update_label)
        
        # สร้างป้ายแสดงข้อความหยุดเกม
        self.pause_label = Label(text="Paused", pos=(Window.width/2 - 50, Window.height/2), font_size=32)
        self.pause_label.opacity = 0  # ซ่อนป้ายเมื่อไม่ได้หยุดเกม
        self.add_widget(self.pause_label)
        
        # โหลดเสียง (ตรวจสอบว่ามีไฟล์เสียงตามที่ระบุ)
        self.eat_sound = SoundLoader.load('eat_sound.mp3')
        self.game_over_sound = SoundLoader.load('game_over.mp3')
        
        self.paused = False  # ตัวแปรเช็คสถานะหยุดเกม
        self.update_event = Clock.schedule_interval(self.update, 0.1)  # เรียกฟังก์ชัน update ทุก 0.1 วินาที
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, instance, key, *args):
        # กดปุ่ม P (key code 112) เพื่อหยุด/เล่นต่อ
        if key == 112:  # 'p' key
            if self.paused:
                # เล่นต่อ
                self.paused = False
                self.pause_label.opacity = 0  # ซ่อนป้ายหยุดเกม
                self.update_event = Clock.schedule_interval(self.update, 0.1)
            else:
                # หยุดเกม
                self.paused = True
                self.pause_label.opacity = 1  # แสดงป้ายหยุดเกม
                if self.update_event is not None:
                    self.update_event.cancel()
                    self.update_event = None
            return

        # กดลูกศรเพื่อเปลี่ยนทิศทาง (สามารถเปลี่ยนแม้ในขณะหยุดได้ หากต้องการให้เปลี่ยนเฉพาะตอนเล่นต่อ ให้เช็ค if not self.paused)
        if key == 273:  # ลูกศรขึ้น
            if self.snake_direction != (0, -1):
                self.snake_direction = (0, 1)
        elif key == 274:  # ลูกศรลง
            if self.snake_direction != (0, 1):
                self.snake_direction = (0, -1)
        elif key == 275:  # ลูกศรขวา
            if self.snake_direction != (-1, 0):
                self.snake_direction = (1, 0)
        elif key == 276:  # ลูกศรซ้าย
            if self.snake_direction != (1, 0):
                self.snake_direction = (-1, 0)

    def update(self, dt):
        new_head = (self.snake[0][0] + self.snake_direction[0],
                    self.snake[0][1] + self.snake_direction[1])
        
        # ตรวจสอบว่าแทงผนังหรือชนตัวเอง
        if (new_head[0] < 0 or new_head[0] >= Window.width // self.snake_size or
            new_head[1] < 0 or new_head[1] >= Window.height // self.snake_size or
            new_head in self.snake):
            if self.game_over_sound:
                self.game_over_sound.play()  # เล่นเสียง game over
            self.reset_game()  # รีเซ็ตเกมเมื่อชน
            return
        
        self.snake = [new_head] + self.snake[:-1]  # เคลื่อนงูไปข้างหน้า
        
        self.canvas.clear()  # เคลียร์ภาพเก่า
        
        self.draw_snake()  # วาดงู
        self.draw_food()   # วาดอาหาร
        
        # ตรวจสอบว่ากินอาหารหรือไม่
        if new_head == self.food:
            self.snake.append(self.snake[-1])  # เพิ่มส่วนของงู
            self.score += 1
            self.update_label.text = f"Score: {self.score}"
            if self.eat_sound:
                self.eat_sound.play()  # เล่นเสียงกินอาหาร
            self.food = self.generate_food()  # สร้างอาหารตำแหน่งใหม่

    def generate_food(self):
        """สุ่มตำแหน่งอาหารใหม่ที่ไม่ซ้อนกับงู"""
        while True:
            food = (random.randint(0, 19), random.randint(0, 19))
            if food not in self.snake:
                return food

    def reset_game(self):
        """รีเซ็ตเกมเมื่อชน"""
        self.snake = [(10, 10)]
        self.snake_direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.update_label.text = "Score: 0"
        self.canvas.clear()
        # เมื่อ game over ให้แน่ใจว่าเกมเล่นต่อ (ไม่อยู่ในโหมด paused)
        if self.paused:
            self.paused = False
            self.pause_label.opacity = 0
            if self.update_event is None:
                self.update_event = Clock.schedule_interval(self.update, 0.1)

    def draw_snake(self):
        """วาดงู"""
        with self.canvas:
            Color(0, 1, 0)  # สีเขียว
            for x, y in self.snake:
                Rectangle(pos=(x * self.snake_size, y * self.snake_size),
                          size=(self.snake_size, self.snake_size))

    def draw_food(self):
        """วาดอาหาร"""
        with self.canvas:
            Color(1, 0, 0)  # สีแดง
            x, y = self.food
            Rectangle(pos=(x * self.snake_size, y * self.snake_size),
                      size=(self.snake_size, self.snake_size))

class SnakeApp(App):
    def build(self):
        return SnakeGame()

if __name__ == '__main__':
    SnakeApp().run()
